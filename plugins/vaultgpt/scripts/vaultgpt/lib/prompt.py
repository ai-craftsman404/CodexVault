"""Prompt vault helpers for VaultGPT."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .audit import append_event
from .vault import SCHEMA_VERSION, initialize_vault, safe_record_id, write_record

DOUBLE_BRACE_RE = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")
SINGLE_BRACE_RE = re.compile(r"(?<!\{)\{([A-Za-z_][A-Za-z0-9_]*)\}(?!\})")


def detect_variables(body: str, include_compat: bool = True) -> list[str]:
    """Detect prompt variable names, preferring canonical {{name}} syntax."""
    found = set(DOUBLE_BRACE_RE.findall(body))
    if include_compat:
        found.update(SINGLE_BRACE_RE.findall(body))
    return sorted(found)


def create_prompt_record(
    prompt_id: str,
    title: str,
    body: str,
    tags: list[str] | None = None,
    favorite: bool = False,
) -> dict[str, Any]:
    """Create a prompt record with detected variable metadata."""
    variables = [{"name": name, "required": True, "default": ""} for name in detect_variables(body)]
    return {
        "id": prompt_id,
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "body": body,
        "variables": variables,
        "tags": tags or [],
        "favorite": favorite,
        "usage": {
            "last_used_at": None,
            "run_count": 0,
        },
    }


def save_prompt(root: str | Path, record: dict[str, Any]) -> Path:
    """Save a prompt record and append an audit event."""
    root_path = initialize_vault(root)
    record_path = write_record(root_path, "prompts", record)
    append_event(root_path, "prompt.created", {"item_id": record["id"], "title": record.get("title", "")})
    return record_path


def load_prompt(root: str | Path, prompt_id: str) -> dict[str, Any]:
    """Load a prompt record."""
    root_path = initialize_vault(root)
    path = root_path / "prompts" / f"{safe_record_id(prompt_id)}.json"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def render_prompt(record: dict[str, Any], values: dict[str, str]) -> str:
    """Render a prompt using canonical and compatibility variable syntax."""
    required = {variable["name"] for variable in record.get("variables", []) if variable.get("required", True)}
    missing = sorted(name for name in required if name not in values and not _default_for(record, name))
    if missing:
        raise ValueError(f"Missing required variables: {', '.join(missing)}")

    merged = {}
    for variable in record.get("variables", []):
        name = variable["name"]
        merged[name] = values.get(name, variable.get("default", ""))

    def replace(match: re.Match[str]) -> str:
        return str(merged.get(match.group(1), match.group(0)))

    rendered = DOUBLE_BRACE_RE.sub(replace, record["body"])
    return SINGLE_BRACE_RE.sub(replace, rendered)


def export_prompts(root: str | Path, output_path: str | Path) -> Path:
    """Export all prompt records to a JSON file."""
    root_path = initialize_vault(root)
    prompts = []
    for path in sorted((root_path / "prompts").glob("*.json")):
        prompts.append(json.loads(path.read_text(encoding="utf-8")))

    output = {
        "schema_version": SCHEMA_VERSION,
        "type": "vaultgpt.prompts",
        "prompts": prompts,
    }
    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_event(root_path, "prompts.exported", {"item_count": len(prompts), "destination": str(destination)})
    return destination


def import_prompts(root: str | Path, input_path: str | Path) -> list[Path]:
    """Import prompt records from a VaultGPT prompt export."""
    source = Path(input_path).expanduser().resolve()
    data = json.loads(source.read_text(encoding="utf-8"))
    if data.get("type") != "vaultgpt.prompts":
        raise ValueError("Unsupported prompt import format")

    written = []
    for record in data.get("prompts", []):
        written.append(save_prompt(root, record))
    append_event(root, "prompts.imported", {"item_count": len(written), "source": str(source)})
    return written


def _default_for(record: dict[str, Any], name: str) -> str:
    for variable in record.get("variables", []):
        if variable["name"] == name:
            return str(variable.get("default", ""))
    return ""

