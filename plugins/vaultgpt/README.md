# VaultGPT

VaultGPT is a free, local-first Codex plugin designed to replace paid ChatGPT power-extension workflows without relying on opaque third-party browser extensions.

## MVP Focus

- Codex Chrome selected-chat capture with explicit approval
- Official ChatGPT export import as fallback and batch source
- Full-text local search
- Unlimited folders, subfolders, tags, and pins
- Unfiled inbox
- Saved searches
- Bulk export and backup to Markdown, JSON, and ZIP
- Prompt vault with variables
- Manual prompt chains
- Convert chat to prompt or chain
- Privacy review before save/index/export
- Audit logs and provenance manifests

## Positioning

VaultGPT gives ChatGPT power-extension features for free, without forcing users to trust a third-party browser extension with their AI history.

## Model-Release Resilience

VaultGPT is designed for model-release resilience.

The intended design stores ChatGPT model names as metadata, not as hardcoded behavior switches. Core workflows such as local vault storage, search, organization, prompt reuse, privacy review, and export should continue to work when a conversation contains a new or unknown model label.

This is not a guarantee of compatibility with all future ChatGPT releases. Browser UI changes can still require capture-adapter updates. The goal is to isolate that work so most of VaultGPT does not need to change.

Planned evidence:

- fixtures with multiple known ChatGPT model labels
- fixtures with unknown/future model labels
- regression tests proving import, search, export, and prompt workflows preserve model metadata without failing
- README updates listing tested model-labelled fixtures before release

## Status

Local MVP foundation is ready for internal testing.

Repo-local plugin discovery metadata is present at `.agents/plugins/marketplace.json`. A running Codex session must reload/install the plugin before live skill invocation can be accepted as passed.

Installed-plugin explicit invocation has been verified. The first broad save test over-captured Codex project/environment context and is treated as a failed pattern. The corrected `@Chrome` workflow successfully previewed and saved a constrained ChatGPT browser conversation after confirmation.

The install surface now uses multiple starter actions rather than a single broad save prompt:

- show available actions
- save selected ChatGPT browser conversation
- import official ChatGPT export
- search local vault
- export or back up vault items
- create or reuse prompt variables

Implemented:

- cross-platform vault path resolution
- local vault initialization
- JSON record storage
- append-only audit log
- approved selected-chat capture boundary with privacy scan and provenance event
- prompt variables and prompt import/export
- conversation normalization with model metadata preservation
- JSON fallback search
- optional SQLite FTS5 index and JSON fallback behavior
- synthetic-compatible official ChatGPT export import
- folders/tags/pins metadata helpers
- unfiled inbox default
- saved searches
- bulk dry-run plans
- Markdown/JSON/ZIP export with manifest
- heuristic privacy scanner
- manual prompt chains
- CLI `init`, `status`, `search`, `import-official`, `reindex`, and `export`

Not complete:

- implicit skill invocation verification
- search/export verification against Chrome-captured record
- full official ChatGPT export parser coverage against real exported edge cases
- public repository URL and maintainer contact metadata

## Privacy Model

VaultGPT is intended to be local-first. Runtime vault data, ChatGPT exports, and generated backups should not be committed to git.

Captured and imported chats are treated as untrusted content. VaultGPT should not follow instructions embedded inside archived chats.

## Development Notes

See:

- `design/architecture.md`
- `design/mvp-task-breakdown.md`
- `design/test-matrix.md`
- `design/ux-adoption-flows.md`
- `RELEASE-CHECKLIST.md`

Run local tests:

```powershell
cd plugins/vaultgpt/scripts/vaultgpt
python -m unittest discover -s tests
```

CLI smoke examples:

```powershell
python vaultgpt.py --vault-path .tmp-vault init
python vaultgpt.py --vault-path .tmp-vault import-official conversations.json
python vaultgpt.py --vault-path .tmp-vault reindex
python vaultgpt.py --vault-path .tmp-vault search privacy
python vaultgpt.py --vault-path .tmp-vault export backup.zip --format zip
```
