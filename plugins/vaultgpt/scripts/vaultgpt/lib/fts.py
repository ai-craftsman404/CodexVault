"""SQLite FTS5 derived index for VaultGPT."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .import_export import load_conversations
from .prompt import load_prompt
from .vault import initialize_vault


def fts_available() -> bool:
    """Return whether the local sqlite build supports FTS5."""
    try:
        connection = sqlite3.connect(":memory:")
        connection.execute("CREATE VIRTUAL TABLE test_fts USING fts5(content)")
        connection.close()
        return True
    except sqlite3.DatabaseError:
        return False


def rebuild_fts_index(root: str | Path) -> dict[str, Any]:
    """Rebuild the derived FTS5 index."""
    if not fts_available():
        return {"status": "unavailable", "mode": "json-scan", "indexed_count": 0, "skipped_count": 0}

    root_path = initialize_vault(root)
    index_path = root_path / "indexes" / "vaultgpt.sqlite3"
    connection = sqlite3.connect(index_path)
    try:
        connection.execute("DROP TABLE IF EXISTS vault_fts")
        connection.execute("CREATE VIRTUAL TABLE vault_fts USING fts5(item_type, item_id, title, body, model_label)")

        indexed = 0
        for record in load_conversations(root_path):
            body = "\n".join(str(message.get("content", "")) for message in record.get("messages", []))
            connection.execute(
                "INSERT INTO vault_fts(item_type, item_id, title, body, model_label) VALUES (?, ?, ?, ?, ?)",
                ("conversation", record["id"], record.get("title", ""), body, record.get("model", {}).get("label", "unknown")),
            )
            indexed += 1

        for path in sorted((root_path / "prompts").glob("*.json")):
            prompt = load_prompt(root_path, path.stem)
            connection.execute(
                "INSERT INTO vault_fts(item_type, item_id, title, body, model_label) VALUES (?, ?, ?, ?, ?)",
                ("prompt", prompt["id"], prompt.get("title", ""), prompt.get("body", ""), ""),
            )
            indexed += 1

        connection.commit()
        return {"status": "ok", "mode": "sqlite-fts5", "indexed_count": indexed, "skipped_count": 0}
    finally:
        connection.close()


def search_fts(root: str | Path, query: str) -> list[dict[str, Any]]:
    """Search the FTS5 index."""
    root_path = initialize_vault(root)
    index_path = root_path / "indexes" / "vaultgpt.sqlite3"
    if not index_path.exists():
        raise FileNotFoundError("FTS index has not been built")

    connection = sqlite3.connect(index_path)
    try:
        rows = connection.execute(
            "SELECT item_type, item_id, title, snippet(vault_fts, 3, '[', ']', '...', 12), model_label "
            "FROM vault_fts WHERE vault_fts MATCH ? LIMIT 50",
            (query,),
        ).fetchall()
        return [
            {"type": row[0], "id": row[1], "title": row[2], "snippet": row[3], "model_label": row[4]}
            for row in rows
        ]
    finally:
        connection.close()

