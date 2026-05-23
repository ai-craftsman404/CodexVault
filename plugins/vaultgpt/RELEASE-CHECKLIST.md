# VaultGPT Release Checklist

## Plugin

- Plugin name: VaultGPT
- Package name: `vaultgpt`
- Version: `0.1.0`
- Release date: unreleased
- Release owner: Code Plugin Guru

## Required Files

- [x] `.codex-plugin/plugin.json`
- [x] `README.md`
- [x] `LICENSE`
- [x] `CHANGELOG.md`
- [x] Skills under `skills/`
- [x] Scripts under `scripts/`
- [x] Design artifacts under `design/`
- [x] Security review under `design/security-review.md`
- [x] Test matrix under `design/test-matrix.md`
- [ ] Public repository metadata finalized

## Documentation

- [x] Clear description
- [x] Usage examples
- [x] Core workflows
- [x] Configuration notes for local vault path
- [x] Known limitations
- [x] Security and privacy notes
- [x] Model-release resilience positioning
- [ ] Public installation instructions after final repo URL is known
- [ ] Live Codex Chrome capture verification notes

## Quality Gates

- [x] Complexity and model selection considered
- [x] Viability assessment complete
- [x] Design spec complete
- [x] Test matrix populated
- [x] Security review complete for MVP foundation
- [x] No committed runtime vault data
- [x] Scoped secret/private-path scan completed
- [x] License selected
- [x] Version and changelog updated
- [x] Manifest JSON parses
- [x] Local Python tests pass
- [x] Repo-local marketplace entry includes `vaultgpt`
- [x] CLI E2E passes for init/import/reindex/search/export
- [x] Current-session discovery boundary tested with `tool_search`
- [x] Default starter prompts changed from broad save prompt to safe action menu
- [x] Codex app reload/install completed
- [x] Explicit VaultGPT plugin invocation verified after reload/install
- [ ] Implicit VaultGPT skill invocation verified after reload/install
- [x] Installed Chrome save preview required confirmation before writing
- [x] Installed save workflow capture scope accepted for `@Chrome` ChatGPT source
- [x] Real-browser selected-chat capture verified with connected Chrome extension
- [x] Search verified against Chrome-captured record
- [x] ZIP export verified against Chrome-captured record
- [x] Synthetic official-export edge fixtures covered
- [ ] Manifest placeholder URLs/email replaced

## Verification Snapshot

- `python -m unittest discover -s tests`: 26 tests passing
- `python -m compileall plugins/vaultgpt/scripts/vaultgpt`: pass
- `python -m json.tool plugins/vaultgpt/.codex-plugin/plugin.json`: pass
- `python -m json.tool .agents/plugins/marketplace.json`: pass
- CLI E2E: init/import-official/reindex/search/export ZIP pass
- Installed plugin invocation: pass, wrote `chat_codex_vaultgpt_save_20260522.json` and `audit.jsonl`
- Installed save privacy review: warning, one medium `windows_path`
- Installed save capture scope: failed acceptance because it captured Codex project/environment context rather than a constrained ChatGPT selected chat
- Installed Chrome capture preview: pass, title `Claude Code vs Kimi`, source URL `https://chatgpt.com/c/69f75455-25d8-8391-a04d-5943d722c696`, 6 visible messages, privacy passed, no save before confirmation
- Installed Chrome capture save: pass, record `chat_a548c903b716a69a`, privacy passed, audit included source URL, message count, and constrained capture scope
- Installed Chrome record search: pass, query `Claude Code Kimi DeepSeek` returned `chat_a548c903b716a69a` using SQLite FTS5
- Installed Chrome record export: pass, ZIP export succeeded and manifest included `chat_a548c903b716a69a`; test vault also contained the earlier failed broad-capture artifact
- Synthetic official export edge fixture: pass, covers missing title, `conversation_id`, multipart dict content, empty system content, and tool result content
- Scoped sensitive-pattern scan: no real secret/private-path hits

## Known Release Blockers

- Public GitHub URL and maintainer contact are not finalized.
- Implicit invocation and should-not-trigger behavior still need installed-plugin checks.
- Redacted real-export validation is deferred to post-MVP/public-beta hardening unless a safe sample becomes available.

## Release Notes Draft

```markdown
## v0.1.0

- Adds VaultGPT local-first ChatGPT vault MVP foundation.
- Includes approved selected-chat capture boundary, official export import, local search, optional SQLite FTS5, folder/tag/pin organization, prompt vaults, manual chains, privacy review, audit logs, and Markdown/JSON/ZIP export.
- Known limitations: live browser capture must be verified per environment; official export parser is tolerant but needs redacted real-export edge-case validation before broad public release.
```
