# Local Codex Mapping

This directory holds the local evidence model for Codex installation and path mapping.

Current phase:
- use the Windows workstation for Windows discovery
- use WSL for Linux discovery
- treat Azure MCP and Azure VMs as out of scope for now

Mapping targets:
- Windows: Codex Desktop and Codex CLI
- Linux: Codex CLI only

Artifacts:
- `mapping-record.schema.json`: shared record shape for capture files
- `run-record.schema.json`: versioned per-run snapshot written under `runs/`
- `ledger-entry.schema.json`: append-only ledger entry shape for `ledger.jsonl`
- `examples/windows-desktop.json`: Windows Desktop mapping placeholder
- `examples/windows-cli.json`: Windows CLI mapping placeholder
- `examples/macos-desktop.json`: macOS Desktop mapping placeholder
- `examples/wsl-linux-cli.json`: WSL Linux CLI mapping placeholder

Confidence model:
- use `confidence` to rank likely targets first
- use `>= 0.85` for verified paths, `0.70-0.84` for review-band candidates, and `< 0.70` for heuristic-only paths
- use `status` to distinguish seed, verified, rejected, and heuristic paths
- keep caveats in `notes` so discovery can target the best candidates immediately

Persistence model:
- per-run evidence snapshots live under `runs/`
- cumulative append-only evidence lives in `ledger.jsonl`
- both persistence formats carry `schemaVersion` so downstream tooling can evolve safely
- both are written from the backup/simulation path so the capture history stays auditable
- review-band instructions stay embedded in the dry-run JSON so there is one canonical review artifact

These files are intentionally lightweight. They define the capture contract before real path evidence is collected from the workstation and WSL environments.
