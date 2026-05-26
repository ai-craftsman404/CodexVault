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
- [x] Public repository metadata finalized

## Documentation

- [x] Clear description
- [x] Usage examples
- [x] Core workflows
- [x] Configuration notes for local vault path
- [x] Known limitations
- [x] Security and privacy notes
- [x] Model-release resilience positioning
- [x] Public installation instructions after final repo URL is known
- [x] Live Chrome skill capture verification notes

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
- [x] Implicit VaultGPT active-tab save preview verified after reload/install
- [x] Implicit VaultGPT search routing verified after reload/install
- [x] Should-not-trigger behavior verified for unrelated cryptography prompt
- [x] Installed Chrome save preview required confirmation before writing
- [x] Installed save workflow capture scope accepted for Chrome skill ChatGPT source
- [x] Real-browser selected-chat capture verified with connected Chrome extension
- [x] Search verified against Chrome-captured record
- [x] ZIP export verified against Chrome-captured record
- [x] Synthetic official-export edge fixtures covered
- [x] Manifest placeholder URLs/email replaced
- [x] VaultGPT package public scan completed
- [x] VaultGPT package tracked-artifact scan completed

## Verification Snapshot

- `$env:PYTHONPATH='plugins/vaultgpt/scripts/vaultgpt'; python -m unittest discover -s plugins/vaultgpt/scripts/vaultgpt/tests`: 28 tests passing
- `python -m compileall plugins/vaultgpt/scripts/vaultgpt`: pass
- `python -m json.tool plugins/vaultgpt/.codex-plugin/plugin.json`: pass
- `python -m json.tool .agents/plugins/marketplace.json`: pass
- Public metadata placeholder scan: pass, no placeholder URL or maintainer values remain in release metadata
- Scoped sensitive-pattern scan: pass, no matches for API keys, OpenAI keys, private user paths, temporary data paths, or literal credential assignments in `plugins/vaultgpt` or `.agents/plugins/marketplace.json`
- VaultGPT tracked-artifact scan: pass, no tracked `.codexvault/`, screenshots, ZIP exports, SQLite/DB files, JSONL logs, keys, credentials, or ChatGPT export payloads under `plugins/vaultgpt`
- Repo-wide tracked-artifact scan: pass, root `.codexvault/` artifacts have been removed from git tracking with `git rm --cached -r .codexvault` and are covered by the root `.gitignore`
- Repo-wide private-path note: unrelated private-path examples remain outside VaultGPT in CodexVault/PremortemX docs and tooling; clean those in a separate repo hygiene pass if the whole repository is being published
- CLI E2E: init/import-official/reindex/search/export ZIP pass
- Installed plugin invocation: pass, wrote `chat_codex_vaultgpt_save_20260522.json` and `audit.jsonl`
- Installed save privacy review: warning, one medium `windows_path`
- Installed save capture scope: failed acceptance because it captured Codex project/environment context rather than a constrained ChatGPT selected chat
- Installed Chrome capture preview: pass, title `Claude Code vs Kimi`, source URL `https://chatgpt.com/c/69f75455-25d8-8391-a04d-5943d722c696`, 6 visible messages, privacy passed, no save before confirmation
- Installed Chrome capture save: pass, record `chat_a548c903b716a69a`, privacy passed, audit included source URL, message count, and constrained capture scope
- Installed Chrome record search: pass, query `Claude Code Kimi DeepSeek` returned `chat_a548c903b716a69a` using SQLite FTS5
- Installed implicit search prompt: pass, query `Claude Code Kimi` returned `chat_a548c903b716a69a`, title `Claude Code vs Kimi`, mode `sqlite-fts5`, index status `ok`
- Installed should-not-trigger prompt: pass, `Explain what a vault is in cryptography.` returned no VaultGPT/tool route during discovery
- Installed implicit active-tab save preview: pass on final 2026-05-23 retry using Chrome `Profile 3` and `https://chatgpt.com/c/69f75455-25d8-8391-a04d-5943d722c696`; `openTabs()` saw `Claude Code vs Kimi`; claimed tab was readable; preview showed 6 messages, role counts user 3 / assistant 3, privacy `passed`, capture confidence `chrome_accessibility_snapshot`, fidelity `warn` for capture limitations only; no vault save was performed and no Codex thread/project/environment context was captured
- Installed Chrome record export: pass, ZIP export succeeded and manifest included `chat_a548c903b716a69a`; test vault also contained the earlier failed broad-capture artifact
- Synthetic official export edge fixture: pass, covers missing title, `conversation_id`, multipart dict content, empty system content, and tool result content
- Scoped sensitive-pattern scan: no real secret/private-path hits
- Public metadata: finalized with repository `https://github.com/ai-craftsman404/CodexVault`, plugin homepage path, GitHub maintainer contact URL, README privacy section, and MIT license terms URL

## Known Release Blockers

- No VaultGPT package blocker remains for MVP release candidate status.
- Whole-repository tracked `.codexvault/` blocker cleared.
- Whole-repository private-path cleanup outside VaultGPT remains separate from this VaultGPT release hygiene pass.
- Redacted real-export validation is deferred to post-MVP/public-beta hardening unless a safe sample becomes available.

## Release Notes Draft

```markdown
## v0.1.0

- Adds VaultGPT local-first ChatGPT vault MVP foundation.
- Includes approved selected-chat capture boundary, official export import, local search, optional SQLite FTS5, folder/tag/pin organization, prompt vaults, manual chains, privacy review, audit logs, and Markdown/JSON/ZIP export.
- Known limitations: live browser capture must be verified per environment; official export parser is tolerant but needs redacted real-export edge-case validation before broad public release.
```
