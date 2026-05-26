"""Selective async export job helpers for VaultGPT."""

from __future__ import annotations

import csv
import json
import os
import re
import hashlib
import importlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

from .audit import append_event
from .import_export import normalize_capture, load_conversations
from .privacy import scan_record
from .vault import initialize_vault, write_record

CHATGPT_URL_RE = re.compile(r"https://chatgpt\.com/(?:g/[^/\s]+/)?c/[A-Za-z0-9-]+|https://chat\.openai\.com/c/[A-Za-z0-9-]+")
MAX_URLS = 25
SCHEMA_VERSION = "0.1"


@dataclass
class ParsedUrls:
    raw_lines: list[str]
    urls: list[str]
    invalid_lines: list[str]
    duplicates: list[str]
    unsupported: list[str]


def parse_url_input(text_or_path: str) -> ParsedUrls:
    if text_or_path == "-":
        text = os.environ.get("VAULTGPT_STDIN", "")
    else:
        path = Path(text_or_path)
        text = path.read_text(encoding="utf-8") if path.exists() else text_or_path
    return parse_url_text(text)


def parse_url_text(text: str) -> ParsedUrls:
    raw_lines = []
    urls = []
    invalid_lines = []
    duplicates = []
    unsupported = []
    seen = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        raw_lines.append(line)
        found = CHATGPT_URL_RE.search(line)
        if not found:
            invalid_lines.append(line)
            continue
        url = _canonicalize_url(found.group(0))
        if url in seen:
            duplicates.append(url)
            continue
        seen.add(url)
        urls.append(url)
        if "chatgpt.com" not in url and "chat.openai.com" not in url:
            unsupported.append(url)
    return ParsedUrls(raw_lines=raw_lines, urls=urls, invalid_lines=invalid_lines, duplicates=duplicates, unsupported=unsupported)


def build_url_input(payload: str | Path) -> ParsedUrls:
    source = Path(payload)
    if source.exists():
        suffix = source.suffix.lower()
        if suffix == ".csv":
            rows = []
            with source.open(newline="", encoding="utf-8") as handle:
                reader = csv.reader(handle)
                for row in reader:
                    rows.extend(row)
            return parse_url_text("\n".join(rows))
        return parse_url_text(source.read_text(encoding="utf-8"))
    return parse_url_text(str(payload))


def create_job(root: str | Path, requested_scope: dict[str, Any], url_input: ParsedUrls) -> dict[str, Any]:
    if len(url_input.urls) > MAX_URLS:
        raise ValueError(f"Maximum {MAX_URLS} URLs per job")
    root_path = initialize_vault(root)
    job_id = f"job_{uuid4().hex[:12]}"
    job_path = root_path / "jobs" / job_id
    job_path.mkdir(parents=True, exist_ok=True)
    job = {
        "job_id": job_id,
        "schema_version": SCHEMA_VERSION,
        "type": "selective_chatgpt_export",
        "created_at": _now(),
        "updated_at": _now(),
        "status": "planned",
        "requested_scope": requested_scope,
        "url_inputs": {
            "raw_lines": url_input.raw_lines,
            "invalid_lines": url_input.invalid_lines,
            "duplicates": url_input.duplicates,
            "unsupported": url_input.unsupported,
        },
        "validated_urls": url_input.urls,
        "items": [
            {
                "source_url": url,
                "canonical_url": url,
                "title": None,
                "status": "queued",
                "messages": [],
                "visible_message_count": 0,
                "role_counts": {},
                "capture_confidence": None,
                "limitations": [],
                "privacy": {"status": "not_checked", "findings": []},
                "fidelity": {"status": "not_checked", "findings": []},
            }
            for url in url_input.urls
        ],
        "privacy": {"status": "not_checked", "findings": []},
        "fidelity": {"status": "not_checked", "findings": []},
        "output": {},
        "errors": [],
        "artifacts": [],
    }
    _write_job(job_path, job)
    append_event(root_path, "selective_export.job_created", {"item_id": job_id, "item_count": len(url_input.urls)})
    return job


def load_job(root: str | Path, job_id: str) -> dict[str, Any]:
    job_path = initialize_vault(root) / "jobs" / job_id / "job.json"
    return json.loads(job_path.read_text(encoding="utf-8"))


def list_job_ids(root: str | Path) -> list[str]:
    jobs_dir = initialize_vault(root) / "jobs"
    if not jobs_dir.exists():
        return []
    return sorted(p.name for p in jobs_dir.iterdir() if p.is_dir())


def ingest_capture_payloads(root: str | Path, job_id: str, payloads: list[dict[str, Any]]) -> dict[str, Any]:
    root_path = initialize_vault(root)
    job_path = root_path / "jobs" / job_id
    job = json.loads((job_path / "job.json").read_text(encoding="utf-8"))
    lookup = {item["source_url"]: item for item in job["items"]}
    for payload in payloads:
        normalized = _normalize_capture_payload(payload)
        item = lookup.get(normalized["source"]["source_id"]) or lookup.get(normalized["source"]["source_url"])
        if not item:
            continue
        item.update(
            {
                "title": normalized["title"],
                "canonical_url": normalized["source"]["url"],
                "messages": normalized["messages"],
                "visible_message_count": len(normalized["messages"]),
                "role_counts": normalized["role_counts"],
                "capture_confidence": normalized["capture_confidence"],
                "limitations": normalized["limitations"],
                "privacy": normalized["privacy"],
                "fidelity": normalized["fidelity"],
                "status": "warning" if normalized["privacy"]["status"] != "passed" or normalized["fidelity"]["status"] != "pass" else "previewed",
            }
        )
        append_event(root_path, "selective_export.item_ingested", {"item_id": normalized["source"]["source_id"], "status": item["status"]})
    job["status"] = "previewed"
    job["updated_at"] = _now()
    _write_job(job_path, job)
    append_event(root_path, "selective_export.job_previewed", {"item_id": job_id, "item_count": len(payloads)})
    return job


def finalize_export(root: str | Path, job_id: str, output_path: str | Path) -> dict[str, Any]:
    root_path = initialize_vault(root)
    job_path = root_path / "jobs" / job_id
    job = json.loads((job_path / "job.json").read_text(encoding="utf-8"))
    records = []
    failures = []
    for item in job["items"]:
        if item["visible_message_count"] == 0:
            failures.append({"source_url": item["source_url"], "reason": "unreadable_or_failed"})
            continue
        records.append(
            normalize_capture(
                {
                    "id": _stable_id(item["title"] or item["source_url"], item["messages"]),
                    "title": item["title"] or "Untitled chat",
                    "source": {
                        "type": "assistant_capture",
                        "source_id": item["source_url"],
                        "url": item["source_url"],
                    },
                    "messages": item["messages"],
                    "privacy": item["privacy"],
                    "capture": {
                        "confidence": item["capture_confidence"],
                        "limitations": item["limitations"],
                    },
                    "model": {"label": "unknown", "raw": {"label": "unknown"}},
                }
            )
        )
    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "job_id": job_id,
        "type": "vaultgpt.selective_export",
        "conversation_count": len(records),
        "selected_urls": [item["source_url"] for item in job["items"]],
        "privacy_summary": {"warning_count": sum(1 for r in records if r["privacy"]["status"] != "passed")},
        "fidelity_summary": {
            "status": "warn" if failures else "pass",
            "reasons": [f"export reported {len(failures)} failed item(s)"] if failures else [],
            "reviewers": ["capture", "privacy", "export"],
            "checked_count": len(records),
            "total_count": len(records),
        },
        "records": [
            {
                "id": record["id"],
                "title": record["title"],
                "source_url": record["source"].get("url"),
                "content_sha256": record["hashes"]["content_sha256"],
                "hashes": record.get("hashes", {}),
            }
            for record in records
        ],
        "failed": failures,
    }
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        archive.writestr("status.json", json.dumps(job, indent=2, sort_keys=True) + "\n")
        archive.writestr("capture-report.md", _records_to_markdown(records, manifest))
        archive.writestr("privacy-report.json", json.dumps([item["privacy"] for item in job["items"]], indent=2, sort_keys=True) + "\n")
        archive.writestr("fidelity-report.json", json.dumps([item["fidelity"] for item in job["items"]], indent=2, sort_keys=True) + "\n")
        archive.writestr("conversations.json", json.dumps(records, indent=2, sort_keys=True) + "\n")
        archive.writestr("conversations.md", _records_to_markdown(records, manifest))
        archive.writestr("events.jsonl", _events_as_jsonl(root_path))
        archive.writestr("failures.json", json.dumps(failures, indent=2, sort_keys=True) + "\n")
    job["status"] = "complete"
    job["updated_at"] = _now()
    job["output"] = {"zip": str(destination)}
    _write_job(job_path, job)
    append_event(root_path, "selective_export.job_exported", {"item_id": job_id, "destination": str(destination)})
    return {"job": job, "manifest": manifest, "output": str(destination), "failures": failures}


def dry_run_preview(root: str | Path, job_id: str) -> dict[str, Any]:
    job = load_job(root, job_id)
    return {
        "job_id": job_id,
        "status": job["status"],
        "items": [
            {
                "source_url": item["source_url"],
                "title": item["title"],
                "visible_message_count": item["visible_message_count"],
                "role_counts": item["role_counts"],
                "privacy": item["privacy"],
                "fidelity": item["fidelity"],
                "capture_confidence": item["capture_confidence"],
            }
            for item in job["items"]
        ],
    }


def _normalize_capture_payload(payload: dict[str, Any]) -> dict[str, Any]:
    messages = payload.get("messages") or []
    role_counts = payload.get("role_counts") or {}
    source_url = payload.get("source_url") or payload.get("canonical_url") or payload.get("source", {}).get("url")
    canonical_url = payload.get("canonical_url") or source_url
    title = payload.get("title") or "Untitled chat"
    return {
        "id": payload.get("id") or _stable_id(title, messages),
        "title": title,
        "messages": messages,
        "role_counts": role_counts,
        "capture_confidence": payload.get("capture_confidence", "unknown"),
        "limitations": payload.get("limitations", []),
        "privacy": payload.get("privacy", {"status": "not_checked", "findings": []}),
        "fidelity": payload.get("fidelity", {"status": "not_checked", "findings": []}),
        "source": {"type": "assistant_capture", "source_id": source_url, "url": canonical_url, "source_url": source_url},
    }


def _records_to_markdown(records: list[dict[str, Any]], manifest: dict[str, Any]) -> str:
    lines = ["# VaultGPT Selective Export", "", f"- job_id: `{manifest['job_id']}`", f"- conversations: {manifest['conversation_count']}", ""]
    for record in records:
        lines.extend([f"## {record['title']}", f"- source: `{record['source']['url']}`", f"- id: `{record['id']}`", ""])
        for message in record.get("messages", []):
            lines.extend([f"### {message.get('role', 'message')}", "", str(message.get("content", "")), ""])
    return "\n".join(lines).rstrip() + "\n"


def _events_as_jsonl(root: Path) -> str:
    audit = root / "audit.jsonl"
    return audit.read_text(encoding="utf-8") if audit.is_file() else ""


def _stable_id(title: str, messages: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256(json.dumps({"title": title, "messages": messages}, sort_keys=True).encode("utf-8")).hexdigest()
    return f"chat_{digest[:16]}"


def _canonicalize_url(url: str) -> str:
    return url.rstrip("/")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_job(job_path: Path, job: dict[str, Any]) -> None:
    job_path.mkdir(parents=True, exist_ok=True)
    (job_path / "job.json").write_text(json.dumps(job, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (job_path / "status.json").write_text(json.dumps({"job_id": job["job_id"], "status": job["status"], "updated_at": job["updated_at"]}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (job_path / "status.md").write_text(f"# {job['job_id']}\n\n- status: {job['status']}\n", encoding="utf-8")
    (job_path / "events.jsonl").write_text("", encoding="utf-8")
