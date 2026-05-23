"""Selected-chat capture boundary for VaultGPT."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .audit import append_event
from .import_export import normalize_capture
from .privacy import scan_record
from .vault import initialize_vault, write_record


def prepare_selected_chat_capture(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a user-approved selected-chat capture."""
    if not payload.get("user_approved"):
        raise ValueError("Selected-chat capture requires explicit user approval")
    messages = payload.get("messages") or []
    if not messages:
        raise ValueError("Selected-chat capture must include at least one message")

    record = normalize_capture(
        {
            **payload,
            "source": {
                **payload.get("source", {}),
                "type": "codex_chrome_selected_chat",
            },
            "status": payload.get("status", "unfiled"),
            "folder": payload.get("folder", "Inbox"),
        }
    )
    record["privacy"] = scan_record(record)
    confidence = payload.get("capture_confidence", "chrome_accessibility_snapshot")
    if confidence not in {
        "official_export",
        "chrome_accessibility_snapshot",
        "dom_complete",
        "dom_partial",
        "screenshot_fallback",
        "manual_review_needed",
    }:
        raise ValueError(f"Unsupported capture confidence: {confidence}")

    record["capture"] = {
        "method": "selected-chat",
        "user_approved": True,
        "scope": payload.get("scope", "selected conversation"),
        "confidence": confidence,
        "limitations": payload.get("capture_limitations", []),
    }
    return record


def save_selected_chat_capture(root: str | Path, payload: dict[str, Any]) -> Path:
    """Save an approved selected-chat capture and record provenance."""
    root_path = initialize_vault(root)
    record = prepare_selected_chat_capture(payload)
    path = write_record(root_path, "conversations", record)
    append_event(
        root_path,
        "conversation.captured",
        {
            "item_id": record["id"],
            "source_type": record["source"]["type"],
            "privacy_status": record["privacy"]["status"],
            "capture_confidence": record["capture"]["confidence"],
        },
    )
    return path
