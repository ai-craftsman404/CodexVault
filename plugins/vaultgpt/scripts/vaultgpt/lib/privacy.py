"""Local heuristic privacy scanner for VaultGPT."""

from __future__ import annotations

import re
from typing import Any

PATTERNS = [
    ("high", "openai_api_key", re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}\b")),
    ("high", "generic_token", re.compile(r"\b(?:api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.I)),
    ("medium", "email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("medium", "windows_path", re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+\\[^\n\r]+")),
    ("medium", "private_url", re.compile(r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)[^\s]*", re.I)),
]


def scan_text(text: str) -> list[dict[str, Any]]:
    """Return heuristic sensitive-content findings."""
    findings = []
    for severity, kind, pattern in PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                {
                    "severity": severity,
                    "kind": kind,
                    "start": match.start(),
                    "end": match.end(),
                    "preview": _redacted_preview(match.group(0), kind),
                }
            )
    return findings


def scan_record(record: dict[str, Any]) -> dict[str, Any]:
    """Scan a conversation or prompt record and return privacy status."""
    chunks = [record.get("title", ""), record.get("body", "")]
    for message in record.get("messages", []):
        chunks.append(str(message.get("content", "")))
    findings = scan_text("\n".join(chunks))
    status = "passed"
    if any(finding["severity"] == "high" for finding in findings):
        status = "warning"
    elif findings:
        status = "warning"
    return {"status": status, "findings": findings}


def redact_text(text: str) -> str:
    """Return a deterministic redaction preview."""
    redacted = text
    replacements = {
        "openai_api_key": "[REDACTED_API_KEY]",
        "generic_token": "[REDACTED_TOKEN]",
        "email": "[REDACTED_EMAIL]",
        "windows_path": "[REDACTED_LOCAL_PATH]",
        "private_url": "[REDACTED_PRIVATE_URL]",
    }
    for _, kind, pattern in PATTERNS:
        redacted = pattern.sub(replacements[kind], redacted)
    return redacted


def _redacted_preview(value: str, kind: str) -> str:
    if kind == "email":
        return "[REDACTED_EMAIL]"
    if kind == "windows_path":
        return "[REDACTED_LOCAL_PATH]"
    if kind == "private_url":
        return "[REDACTED_PRIVATE_URL]"
    return value[:4] + "..." if len(value) > 4 else "[REDACTED]"

