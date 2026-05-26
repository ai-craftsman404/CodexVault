"""VaultGPT local CLI entrypoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.audit import append_event
from lib.import_export import export_conversations, import_official_export_file
from lib.fts import rebuild_fts_index, search_fts
from lib.paths import resolve_vault_path
from lib.selective_export import build_url_input, create_job, dry_run_preview, finalize_export, ingest_capture_payloads
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
    import_parser = subcommands.add_parser("import-official", help="Import a ChatGPT conversations export JSON file")
    import_parser.add_argument("input")
    subcommands.add_parser("reindex", help="Rebuild the optional SQLite FTS5 index")
    selective_parser = subcommands.add_parser("selective-export", help="Selective async export workflow")
    selective_parser.add_argument("input", nargs="?", help="Pasted URLs or input file path")
    selective_parser.add_argument("--ingest-payloads", help="Normalized capture payload JSON file")
    selective_parser.add_argument("--output", help="Output ZIP path")
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
        try:
            results = search_fts(root, args.query)
            mode = "sqlite-fts5"
        except (FileNotFoundError, Exception):
            results = search_json(root, args.query)
            mode = "json-scan"
        print(json.dumps({"results": results, "mode": mode, "index": index_status(root)}, indent=2))
        return 0

    if args.command == "export":
        root = initialize_vault(vault_path)
        manifest = export_conversations(root, args.output, args.format)
        print(json.dumps({"status": "ok", "manifest": manifest}, indent=2))
        return 0

    if args.command == "import-official":
        root = initialize_vault(vault_path)
        written = import_official_export_file(root, args.input)
        print(json.dumps({"status": "ok", "imported_count": len(written)}, indent=2))
        return 0

    if args.command == "reindex":
        root = initialize_vault(vault_path)
        print(json.dumps(rebuild_fts_index(root), indent=2))
        return 0

    if args.command == "selective-export":
        root = initialize_vault(vault_path)
        if args.ingest_payloads:
            payload_path = Path(args.ingest_payloads)
            payloads = json.loads(payload_path.read_text(encoding="utf-8"))
            if not isinstance(payloads, list):
                raise ValueError("--ingest-payloads expects a JSON array")
            scope = {"source": "assistant_mediated_capture"}
            if args.input:
                url_input = build_url_input(args.input)
            else:
                url_input = build_url_input("\n".join(payload.get("source_url", "") for payload in payloads))
            job = create_job(root, scope, url_input)
            job = ingest_capture_payloads(root, job["job_id"], payloads)
            preview = dry_run_preview(root, job["job_id"])
            print(json.dumps({"status": "ok", "job": job, "preview": preview}, indent=2))
            if args.output:
                result = finalize_export(root, job["job_id"], args.output)
                print(json.dumps({"export": result}, indent=2))
            return 0
        if not args.input:
            raise ValueError("selective-export requires an input URL list or --ingest-payloads")
        url_input = build_url_input(args.input)
        job = create_job(root, {"source": "url_list"}, url_input)
        print(json.dumps({"status": "ok", "job": job, "preview": dry_run_preview(root, job["job_id"])}, indent=2))
        return 0

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
