# VaultGPT Implementation Decisions

## Validated Decisions

- Runtime: Python stdlib-first CLI modules.
- Platform support: Windows, macOS, and Linux are required.
- Vault source of truth: canonical JSON/JSONL records.
- Search index: SQLite FTS5 as derived index, with deterministic JSON scan fallback.
- Vault path defaults:
  - Windows: `%LOCALAPPDATA%\VaultGPT`
  - macOS: `~/Library/Application Support/VaultGPT`
  - Linux: `${XDG_DATA_HOME:-~/.local/share}/vaultgpt`
  - override: `VAULTGPT_HOME` or CLI `--vault-path`
- Capture: Codex Chrome selected-chat capture only, preview-first and user-approved.
- Fallback ingestion: official ChatGPT export import.
- Export formats: Markdown, JSON, ZIP.
- ZIP export: include manifest, hashes, counts, skipped/failed records, and provenance.
- Privacy scanner: local heuristic triage only, not a DLP/security guarantee.
- Prompt variables: canonical syntax is `{{name}}`; `{name}` is compatibility mode only for simple identifiers.
- Model-release resilience: preserve known and unknown model labels as metadata.

## Release Blockers To Clear Later

- Replace placeholder manifest metadata before public release.
- Complete security/privacy review.
- Execute full test matrix.
- Add executable script tests.
- Verify or safely stub Codex Chrome selected-chat capture.
- Prove private vault data and exports are excluded from git.
- Add model-release resilience fixtures and passing tests.

## Immediate Build Direction

Start with cross-platform Python core:

1. OS-aware path resolver.
2. Vault initialization.
3. Audit log.
4. Canonical JSON records.
5. Prompt variable rendering.
6. Synthetic tests only.

