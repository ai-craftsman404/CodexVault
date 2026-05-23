"""Organization helpers for VaultGPT."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .audit import append_event
from .vault import initialize_vault, safe_record_id


def update_conversation_metadata(
    root: str | Path,
    conversation_id: str,
    folder: str | None = None,
    tags: list[str] | None = None,
    pinned: bool | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    """Update metadata for one conversation without changing message content."""
    root_path = initialize_vault(root)
    path = root_path / "conversations" / f"{safe_record_id(conversation_id)}.json"
    if not path.exists():
        raise FileNotFoundError(f"Conversation not found: {conversation_id}")

    record = json.loads(path.read_text(encoding="utf-8"))
    original_messages = record.get("messages", [])
    if folder is not None:
        record["folder"] = folder
    if tags is not None:
        record["tags"] = sorted(set(tags))
    if pinned is not None:
        record["pins"] = ["pinned"] if pinned else []
    if status is not None:
        record["status"] = status

    if record.get("messages", []) != original_messages:
        raise RuntimeError("Metadata update attempted to alter messages")

    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_event(root_path, "conversation.metadata_updated", {"item_id": conversation_id})
    return record


def save_search(root: str | Path, name: str, query: str, filters: dict[str, Any] | None = None) -> Path:
    """Save a named search query."""
    root_path = initialize_vault(root)
    searches_dir = root_path / "saved_searches"
    searches_dir.mkdir(exist_ok=True)
    record = {
        "schema_version": "0.1",
        "id": safe_record_id(name),
        "name": name,
        "query": query,
        "filters": filters or {},
    }
    path = searches_dir / f"{record['id']}.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_event(root_path, "search.saved", {"item_id": record["id"], "query": query})
    return path


def bulk_plan(item_ids: list[str], action: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a dry-run plan for bulk operations."""
    return {
        "dry_run": True,
        "action": action,
        "item_count": len(item_ids),
        "item_ids": item_ids,
        "details": details or {},
        "requires_confirmation": action in {"delete", "archive", "move", "tag"},
    }

