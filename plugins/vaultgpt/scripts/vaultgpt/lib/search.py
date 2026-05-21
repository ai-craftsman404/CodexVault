"""Search helpers for VaultGPT."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .import_export import load_conversations
from .prompt import load_prompt
from .vault import initialize_vault


def search_json(root: str | Path, query: str) -> list[dict[str, Any]]:
    """Deterministic JSON scan fallback search."""
    root_path = initialize_vault(root)
    normalized_query = query.casefold()
    results = []

    for record in load_conversations(root_path):
        haystack_parts = [record.get("title", ""), " ".join(record.get("tags", []))]
        for message in record.get("messages", []):
            haystack_parts.append(str(message.get("content", "")))
            haystack_parts.append(str(message.get("role", "")))
        haystack = "\n".join(haystack_parts)
        if normalized_query in haystack.casefold():
            results.append(
                {
                    "type": "conversation",
                    "id": record["id"],
                    "title": record.get("title", ""),
                    "model_label": record.get("model", {}).get("label", "unknown"),
                    "snippet": _snippet(haystack, normalized_query),
                }
            )

    for path in sorted((root_path / "prompts").glob("*.json")):
        prompt = load_prompt(root_path, path.stem)
        haystack = "\n".join([prompt.get("title", ""), prompt.get("body", ""), " ".join(prompt.get("tags", []))])
        if normalized_query in haystack.casefold():
            results.append(
                {
                    "type": "prompt",
                    "id": prompt["id"],
                    "title": prompt.get("title", ""),
                    "snippet": _snippet(haystack, normalized_query),
                }
            )
    return results


def index_status(root: str | Path) -> dict[str, Any]:
    """Return lightweight index/source status for MVP JSON fallback."""
    root_path = initialize_vault(root)
    return {
        "mode": "json-scan",
        "conversation_count": len(list((root_path / "conversations").glob("*.json"))),
        "prompt_count": len(list((root_path / "prompts").glob("*.json"))),
        "fts_available": False,
        "status": "ok",
    }


def _snippet(text: str, query: str, size: int = 120) -> str:
    lower = text.casefold()
    index = lower.find(query)
    if index < 0:
        return text[:size]
    start = max(0, index - size // 3)
    end = min(len(text), index + size)
    return text[start:end].replace("\n", " ")

