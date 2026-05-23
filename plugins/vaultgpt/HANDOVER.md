# VaultGPT Handover

## Current Status

VaultGPT is an installable Codex plugin and MVP feature-complete release candidate with a working local engine and a verified `@Chrome` capture path.

The VaultGPT package is release-candidate ready. Whole-repository publication still needs pre-existing root `.codexvault/` artifacts outside `plugins/vaultgpt` removed or excluded.

## Latest Important Commits

- `4887943` Add VaultGPT synthetic export edge coverage
- `fe381ec` Add VaultGPT lightweight fidelity review
- `5f0d8c1` Add VaultGPT capture confidence metadata
- `92dea5a` Record VaultGPT competitor capture insights
- `88af3d1` Verify VaultGPT Chrome record search export
- `ff92d35` Prioritize active ChatGPT tab capture
- `0273657` Record VaultGPT Chrome capture pass
- `1c03727` Improve VaultGPT starter action menu
- `adcbe14` Wire VaultGPT local marketplace discovery

## What Is Done

- Plugin scaffold and marketplace entry.
- Starter action menu instead of one broad save prompt.
- Core local vault engine.
- Local audit log.
- Privacy scanner.
- Capture confidence metadata.
- Lightweight pass/warn/block fidelity review.
- Official export import with synthetic edge-case coverage.
- SQLite FTS5 search with JSON fallback.
- Markdown/JSON/ZIP export with manifest and fidelity summary.
- Prompt vault with variables.
- Manual prompt chains.
- Folders, tags, pins, saved searches, unfiled inbox.
- Installed plugin explicit invocation.
- Connected `@Chrome` current active ChatGPT tab preview/save.
- Search/export verification against Chrome-captured record.
- Installed implicit search routing.
- Installed should-not-trigger behavior for unrelated cryptography prompt.
- 28 local VaultGPT tests passing.

## Critical Lessons Learned

- Do not use Codex in-app browser for signed-in ChatGPT capture.
- Use `@Chrome` with the connected Codex Chrome extension.
- Primary MVP capture target is current active ChatGPT tab.
- Specific ChatGPT URL is fallback/debug only.
- Selected/multiple tabs are deferred.
- Broad visible Codex thread capture is a failed pattern and must not be treated as MVP success.
- Chrome accessibility snapshot is acceptable for MVP if labeled with capture confidence and limitations.
- Fidelity review mitigates, but cannot prove, full completeness if the snapshot omits hidden/virtualized content.
- Codex Chrome access may be region/network gated. In testing, `@Chrome` only became available again after switching the desktop network to a US region; if Chrome/extension are installed but `@Chrome` reports unavailable, check supported region/network before debugging VaultGPT.

## Verified Chrome Capture Evidence

Test chat:

```text
https://chatgpt.com/c/69f75455-25d8-8391-a04d-5943d722c696
```

Saved record:

```text
<repo>/.codexvault/conversations/chat_a548c903b716a69a.json
```

Record summary:

- title: `Claude Code vs Kimi`
- source type: `codex_chrome_selected_chat`
- source URL: ChatGPT conversation URL above
- messages: 6
- privacy: `passed`
- tags: `chatgpt`, `chrome-capture`, `vaultgpt`

Audit file:

```text
<repo>/.codexvault/audit.jsonl
```

Search verification command:

```powershell
python <codex-plugin-cache>/vaultgpt/0.1.0/scripts/vaultgpt/vaultgpt.py --vault-path <repo>/.codexvault search "Claude Code Kimi DeepSeek"
```

Expected result:

- returns `chat_a548c903b716a69a`
- search mode: `sqlite-fts5`

## Remaining MVP Gates

### 1. Installed-Plugin Invocation Tests

Complete for MVP.

Implicit trigger prompt:

```text
Save my current active ChatGPT tab to VaultGPT. Preview first and do not save until I confirm.
```

Expected:

- VaultGPT activates without explicit plugin mention.
- It uses `@Chrome`, not in-app browser.
- It previews title, URL, message count, roles count, privacy, capture confidence, limitations, folder/status, proposed ID.
- It does not save before confirmation.

Latest result:

- pass on final 2026-05-23 retry using Chrome `Profile 3` and `https://chatgpt.com/c/69f75455-25d8-8391-a04d-5943d722c696`
- `openTabs()` saw `Claude Code vs Kimi`
- claimed user tab URL matched the ChatGPT test URL
- visible ChatGPT messages were readable
- preview showed 6 messages, role counts user 3 / assistant 3
- privacy result: `passed`
- capture confidence: `chrome_accessibility_snapshot`
- fidelity result: `warn` because capture limitations are present
- no vault save was performed before confirmation
- no Codex thread/project/environment context was captured

Completed search prompt:

```text
Search my VaultGPT archive for Claude Code Kimi.
```

Result:

- pass
- returned `chat_a548c903b716a69a`
- title: `Claude Code vs Kimi`
- mode: `sqlite-fts5`
- index status: `ok`

Completed should-not-trigger prompt:

```text
Explain what a vault is in cryptography.
```

Result:

- pass
- no VaultGPT/tool route returned during discovery

Recorded results in:

- `plugins/vaultgpt/design/test-matrix.md`
- `plugins/vaultgpt/RELEASE-CHECKLIST.md`

### 2. Final Public Metadata

Complete.

- public GitHub repo URL: `https://github.com/ai-craftsman404/CodexVault`
- plugin homepage: `https://github.com/ai-craftsman404/CodexVault/tree/main/plugins/vaultgpt`
- maintainer contact URL: `https://github.com/ai-craftsman404`
- privacy URL: `https://github.com/ai-craftsman404/CodexVault/blob/main/plugins/vaultgpt/README.md#privacy-model`
- terms URL: `https://github.com/ai-craftsman404/CodexVault/blob/main/plugins/vaultgpt/LICENSE`

Updated files:

- `plugins/vaultgpt/.codex-plugin/plugin.json`
- `plugins/vaultgpt/README.md`
- `plugins/vaultgpt/RELEASE-CHECKLIST.md`

### 3. Final Public Scan

VaultGPT package result:

- 28 tests passing
- manifest and marketplace JSON parse
- no placeholder metadata remains
- no scoped sensitive-pattern hits in `plugins/vaultgpt` or `.agents/plugins/marketplace.json`
- no tracked VaultGPT package runtime artifacts, screenshots, exports, backups, DBs, or personal vault files found
- `plugins/vaultgpt/.gitignore` covers runtime vault data, exports, backups, user ChatGPT/OpenAI exports, secrets, and local env files

Whole-repo note:

- pre-existing tracked root `.codexvault/` artifacts remain outside the VaultGPT package and must be removed or excluded before publishing the whole repository

Useful checks:

```powershell
$env:PYTHONPATH='plugins/vaultgpt/scripts/vaultgpt'; python -m unittest discover -s plugins/vaultgpt/scripts/vaultgpt/tests
python -m json.tool plugins/vaultgpt/.codex-plugin/plugin.json > $null
python -m json.tool .agents/plugins/marketplace.json > $null
git status --short
```

## Deferred / Documented Risks

- Redacted real ChatGPT export fixture is not available. Synthetic edge fixtures are used for MVP.
- Real-export validation should be post-MVP/public-beta hardening unless a safe redacted sample becomes available.
- Accessibility snapshot may omit hidden/collapsed/virtualized content, detailed code blocks, tables, links, or images.
- Official ChatGPT export remains authoritative for full-history backup where available.

## Important Files

- `plugins/vaultgpt/.codex-plugin/plugin.json`
- `plugins/vaultgpt/skills/vaultgpt/SKILL.md`
- `plugins/vaultgpt/scripts/vaultgpt/lib/capture.py`
- `plugins/vaultgpt/scripts/vaultgpt/lib/fidelity.py`
- `plugins/vaultgpt/scripts/vaultgpt/lib/import_export.py`
- `plugins/vaultgpt/scripts/vaultgpt/tests/test_core.py`
- `plugins/vaultgpt/design/test-matrix.md`
- `plugins/vaultgpt/RELEASE-CHECKLIST.md`
- `plugins/vaultgpt/design/security-review.md`
- `plugins/vaultgpt/notes/mvp-scope.md`

## Current Test Count

Last verified:

```text
28 tests passing
```

Command used:

```powershell
$env:PYTHONPATH='plugins/vaultgpt/scripts/vaultgpt'; python -m unittest discover -s plugins/vaultgpt/scripts/vaultgpt/tests
```
