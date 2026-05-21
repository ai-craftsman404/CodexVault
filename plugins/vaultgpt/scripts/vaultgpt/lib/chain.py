"""Manual prompt-chain helpers for VaultGPT."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .audit import append_event
from .prompt import detect_variables
from .vault import SCHEMA_VERSION, initialize_vault, safe_record_id, write_record


def create_chain_record(chain_id: str, title: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
    """Create a manual chain record."""
    variables = sorted({variable for step in steps for variable in detect_variables(step.get("body", ""))})
    return {
        "id": chain_id,
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "mode": "manual",
        "variables": [{"name": name, "required": True, "default": ""} for name in variables],
        "steps": steps,
    }


def save_chain(root: str | Path, record: dict[str, Any]) -> Path:
    """Save a chain record."""
    root_path = initialize_vault(root)
    path = write_record(root_path, "chains", record)
    append_event(root_path, "chain.created", {"item_id": record["id"], "step_count": len(record.get("steps", []))})
    return path


def load_chain(root: str | Path, chain_id: str) -> dict[str, Any]:
    """Load a chain record."""
    root_path = initialize_vault(root)
    path = root_path / "chains" / f"{safe_record_id(chain_id)}.json"
    if not path.exists():
        raise FileNotFoundError(f"Chain not found: {chain_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def start_chain_run(root: str | Path, chain_id: str) -> dict[str, Any]:
    """Create an initial manual chain run state."""
    chain = load_chain(root, chain_id)
    state = {
        "chain_id": chain_id,
        "current_step": 0,
        "status": "pending",
        "step_count": len(chain.get("steps", [])),
    }
    append_event(root, "chain.run_started", {"item_id": chain_id, "step_count": state["step_count"]})
    return state


def chat_to_prompt_candidate(conversation: dict[str, Any]) -> dict[str, Any]:
    """Create a prompt candidate from the first user message in a conversation."""
    for message in conversation.get("messages", []):
        if message.get("role") == "user" and message.get("content"):
            return {
                "title": f"Prompt from {conversation.get('title', 'chat')}",
                "body": message["content"],
                "source_conversation_id": conversation.get("id"),
                "requires_confirmation": True,
            }
    raise ValueError("Conversation has no user message to convert")

