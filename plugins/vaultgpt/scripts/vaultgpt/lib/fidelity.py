"""Lightweight fidelity review helpers for VaultGPT."""

from __future__ import annotations

from typing import Any


RISKY_CONFIDENCE = {"dom_partial", "screenshot_fallback", "manual_review_needed"}


def review_capture(record: dict[str, Any], expected_message_count: int | None = None) -> dict[str, Any]:
    """Return a fast pass/warn/block capture fidelity summary."""
    reasons = []
    messages = record.get("messages", [])
    confidence = record.get("capture", {}).get("confidence", "manual_review_needed")
    privacy_status = record.get("privacy", {}).get("status", "not_checked")

    if not messages:
        return _summary("block", ["no messages captured"], checked_count=0)
    if expected_message_count is not None and len(messages) != expected_message_count:
        reasons.append(f"message count mismatch: expected {expected_message_count}, got {len(messages)}")
    if confidence in RISKY_CONFIDENCE:
        reasons.append(f"capture confidence is {confidence}")
    if record.get("capture", {}).get("limitations"):
        reasons.append("capture limitations are present")
    if privacy_status == "warning":
        reasons.append("privacy review has warnings")

    return _summary("warn" if reasons else "pass", reasons, checked_count=len(messages))


def review_export_manifest(manifest: dict[str, Any], sample_size: int = 5) -> dict[str, Any]:
    """Return a fast pass/warn/block export fidelity summary."""
    reasons = []
    records = manifest.get("records", [])
    declared_count = manifest.get("conversation_count")
    failed = manifest.get("failed", [])
    privacy_summary = manifest.get("privacy_summary", {})

    if declared_count != len(records):
        reasons.append(f"manifest count mismatch: declared {declared_count}, records {len(records)}")
    if failed:
        reasons.append(f"export reported {len(failed)} failed item(s)")
    if privacy_summary.get("warning_count", 0):
        reasons.append(f"privacy warnings present: {privacy_summary['warning_count']}")
    missing_hashes = [record.get("id", "unknown") for record in records[:sample_size] if not record.get("content_sha256")]
    if missing_hashes:
        reasons.append(f"sample records missing hashes: {', '.join(missing_hashes)}")

    status = "block" if failed else "warn" if reasons else "pass"
    return _summary(status, reasons, checked_count=min(len(records), sample_size), total_count=len(records))


def _summary(status: str, reasons: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "status": status,
        "reasons": reasons[:3],
        "reviewers": ["capture", "privacy", "export"],
        **extra,
    }
