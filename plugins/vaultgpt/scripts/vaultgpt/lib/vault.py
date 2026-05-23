"""VaultGPT local vault initialization and record storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1"
VAULT_NAME = "VaultGPT"
COLLECTIONS = ("conversations", "prompts", "chains", "exports", "indexes")


def initialize_vault(root: str | Path) -> Path:
    """Create an empty VaultGPT vault if needed and return its root path."""
    root_path = Path(root).expanduser().resolve()
    root_path.mkdir(parents=True, exist_ok=True)

    for collection in COLLECTIONS:
        (root_path / collection).mkdir(exist_ok=True)

    metadata_path = root_path / "vault.json"
    if not metadata_path.exists():
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "name": VAULT_NAME,
            "collections": list(COLLECTIONS),
        }
        metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit_path = root_path / "audit.jsonl"
    audit_path.touch(exist_ok=True)

    return root_path


def write_record(root: str | Path, collection: str, record: dict[str, Any]) -> Path:
    """Write one JSON record into a vault collection."""
    if collection not in COLLECTIONS:
        raise ValueError(f"Unsupported collection: {collection}")
    if not record.get("id"):
        raise ValueError("Record must include an id")

    root_path = initialize_vault(root)
    output = dict(record)
    output.setdefault("schema_version", SCHEMA_VERSION)

    record_path = root_path / collection / f"{safe_record_id(str(output['id']))}.json"
    record_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record_path


def safe_record_id(record_id: str) -> str:
    """Return a conservative filesystem-safe record id."""
    allowed = []
    for char in record_id:
        if char.isalnum() or char in ("-", "_", "."):
            allowed.append(char)
        else:
            allowed.append("_")
    safe = "".join(allowed).strip("._ ")
    if not safe:
        raise ValueError("Record id is empty after sanitization")
    return safe

