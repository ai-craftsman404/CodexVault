"""VaultGPT local CLI entrypoint."""

from __future__ import annotations

import argparse
import json

from lib.audit import append_event
from lib.import_export import export_conversations
from lib.paths import resolve_vault_path
from lib.search import index_status, search_json
from lib.vault import initialize_vault


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VaultGPT local vault utility")
    parser.add_argument("--vault-path", help="Override the VaultGPT vault path")

    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("init", help="Initialize the local VaultGPT vault")
    subcommands.add_parser("status", help="Print local VaultGPT vault status")
    search_parser = subcommands.add_parser("search", help="Search the local VaultGPT vault")
    search_parser.add_argument("query")
    export_parser = subcommands.add_parser("export", help="Export conversations")
    export_parser.add_argument("output")
    export_parser.add_argument("--format", choices=["json", "markdown", "zip"], default="json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    vault_path = resolve_vault_path(args.vault_path)

    if args.command == "init":
        root = initialize_vault(vault_path)
        append_event(root, "vault.initialized", {"item_id": "vault"})
        print(json.dumps({"status": "ok", "vault_path": str(root)}, indent=2))
        return 0

    if args.command == "status":
        root = initialize_vault(vault_path)
        status = {
            "status": "ok",
            "vault_path": str(root),
            "has_metadata": (root / "vault.json").is_file(),
            "has_audit_log": (root / "audit.jsonl").is_file(),
            "index": index_status(root),
        }
        print(json.dumps(status, indent=2))
        return 0

    if args.command == "search":
        root = initialize_vault(vault_path)
        print(json.dumps({"results": search_json(root, args.query), "index": index_status(root)}, indent=2))
        return 0

    if args.command == "export":
        root = initialize_vault(vault_path)
        manifest = export_conversations(root, args.output, args.format)
        print(json.dumps({"status": "ok", "manifest": manifest}, indent=2))
        return 0

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
