"""Import and export helpers for VaultGPT conversations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from .audit import append_event
from .fidelity import review_export_manifest
from .privacy import scan_record
from .vault import SCHEMA_VERSION, initialize_vault, write_record


def normalize_capture(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a selected-chat or export conversation payload."""
    source = payload.get("source", {})
    messages = payload.get("messages", [])
    model = payload.get("model") or {}
    if isinstance(model, str):
        model = {"label": model, "source_field": "model", "raw": {"model": model}}

    record_id = payload.get("id") or _stable_id(payload.get("title", ""), messages)
    return {
        "id": record_id,
        "schema_version": SCHEMA_VERSION,
        "source": {
            "type": source.get("type", payload.get("source_type", "manual_import")),
            "source_id": source.get("source_id", payload.get("source_id", record_id)),
            "captured_at": source.get("captured_at", payload.get("captured_at")),
            "url": source.get("url", payload.get("source_url")),
        },
        "title": payload.get("title") or "Untitled chat",
        "model": {
            "label": model.get("label", "unknown"),
            "source_field": model.get("source_field", "model"),
            "raw": model.get("raw", model),
        },
        "folder": payload.get("folder", "Inbox"),
        "tags": payload.get("tags", []),
        "pins": payload.get("pins", []),
        "status": payload.get("status", "unfiled"),
        "messages": messages,
        "privacy": payload.get("privacy", {"status": "not_checked", "findings": []}),
        "hashes": {"content_sha256": _content_hash(messages)},
    }


def import_conversation_payloads(root: str | Path, payloads: list[dict[str, Any]]) -> list[Path]:
    """Normalize and import conversation payloads."""
    root_path = initialize_vault(root)
    written = []
    for payload in payloads:
        record = normalize_capture(payload)
        written.append(write_record(root_path, "conversations", record))
    append_event(root_path, "conversations.imported", {"item_count": len(written)})
    return written


def import_official_export_file(root: str | Path, input_path: str | Path) -> list[Path]:
    """Import a synthetic-compatible official ChatGPT export conversations JSON file."""
    source = Path(input_path).expanduser().resolve()
    data = json.loads(source.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "conversations" in data:
        conversations = data["conversations"]
    elif isinstance(data, list):
        conversations = data
    else:
        raise ValueError("Unsupported ChatGPT export format")

    payloads = [_normalize_official_conversation(item) for item in conversations]
    return import_conversation_payloads(root, payloads)


def load_conversations(root: str | Path) -> list[dict[str, Any]]:
    """Load all conversation records."""
    root_path = initialize_vault(root)
    records = []
    for path in sorted((root_path / "conversations").glob("*.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    return records


def export_conversations(root: str | Path, output_path: str | Path, fmt: str = "json") -> dict[str, Any]:
    """Export all conversations to JSON, Markdown, or ZIP with a manifest."""
    root_path = initialize_vault(root)
    records = load_conversations(root_path)
    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    privacy_results = [scan_record(record) for record in records]
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "type": "vaultgpt.export",
        "format": fmt,
        "conversation_count": len(records),
        "privacy_summary": {
            "checked": True,
            "warning_count": sum(1 for result in privacy_results if result["status"] == "warning"),
            "finding_count": sum(len(result["findings"]) for result in privacy_results),
        },
        "skipped": [],
        "failed": [],
        "records": [
            {
                "id": record["id"],
                "title": record.get("title", ""),
                "model_label": record.get("model", {}).get("label", "unknown"),
                "content_sha256": record.get("hashes", {}).get("content_sha256", ""),
            }
            for record in records
        ],
    }
    manifest["fidelity_summary"] = review_export_manifest(manifest)

    if fmt == "json":
        payload = {"manifest": manifest, "conversations": records}
        destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    elif fmt == "markdown":
        destination.write_text(_records_to_markdown(records, manifest), encoding="utf-8")
    elif fmt == "zip":
        with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            archive.writestr("conversations.json", json.dumps(records, indent=2, sort_keys=True) + "\n")
            archive.writestr("conversations.md", _records_to_markdown(records, manifest))
    else:
        raise ValueError(f"Unsupported export format: {fmt}")

    append_event(
        root_path,
        "conversations.exported",
        {"item_count": len(records), "format": fmt, "destination": str(destination), "failed_count": 0},
    )
    return manifest


def _stable_id(title: str, messages: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256(json.dumps({"title": title, "messages": messages}, sort_keys=True).encode("utf-8")).hexdigest()
    return f"chat_{digest[:16]}"


def _content_hash(messages: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(messages, sort_keys=True).encode("utf-8")).hexdigest()


def _normalize_official_conversation(item: dict[str, Any]) -> dict[str, Any]:
    messages = item.get("messages")
    if messages is None and "mapping" in item:
        messages = []
        for node in item.get("mapping", {}).values():
            message = node.get("message") or {}
            author = message.get("author", {})
            content = message.get("content", {})
            text = _content_to_text(content)
            if text:
                messages.append({"role": author.get("role", "unknown"), "content": text})
    messages = messages or []
    return {
        "id": item.get("id") or item.get("conversation_id"),
        "title": item.get("title") or "Untitled chat",
        "model": item.get("model") or item.get("default_model_slug") or "unknown",
        "messages": messages,
        "source": {
            "type": "official_export",
            "source_id": item.get("id") or item.get("conversation_id"),
            "captured_at": item.get("update_time") or item.get("create_time"),
        },
    }


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, dict):
        return str(content) if content is not None else ""

    parts = content.get("parts")
    if parts is None:
        if "text" in content:
            return str(content["text"])
        if "result" in content:
            return str(content["result"])
        return ""

    text_parts = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, str):
            text_parts.append(part)
        elif isinstance(part, dict):
            if "text" in part:
                text_parts.append(str(part["text"]))
            elif "content" in part:
                text_parts.append(str(part["content"]))
            else:
                text_parts.append(json.dumps(part, sort_keys=True))
        else:
            text_parts.append(str(part))
    return "\n".join(text_parts)


def _records_to_markdown(records: list[dict[str, Any]], manifest: dict[str, Any]) -> str:
    lines = [
        "---",
        f"schema_version: {manifest['schema_version']}",
        f"conversation_count: {manifest['conversation_count']}",
        "---",
        "",
    ]
    for record in records:
        lines.extend(
            [
                f"# {record.get('title', 'Untitled chat')}",
                "",
                f"- id: `{record['id']}`",
                f"- model: `{record.get('model', {}).get('label', 'unknown')}`",
                f"- status: `{record.get('status', 'unknown')}`",
                "",
            ]
        )
        for message in record.get("messages", []):
            lines.extend([f"## {message.get('role', 'message')}", "", str(message.get("content", "")), ""])
    return "\n".join(lines).rstrip() + "\n"
