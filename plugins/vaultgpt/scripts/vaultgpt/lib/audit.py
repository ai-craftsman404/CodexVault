"""Append-only audit log helpers for VaultGPT."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .vault import initialize_vault


def append_event(root: str | Path, action: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Append one audit event and return the stored event."""
    root_path = initialize_vault(root)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "action": action,
        "actor": "local-user",
    }
    if details:
        event.update(details)

    with (root_path / "audit.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")

    return event


def read_events(root: str | Path) -> list[dict[str, Any]]:
    """Read audit events from the vault."""
    root_path = initialize_vault(root)
    events = []
    for line in (root_path / "audit.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events

