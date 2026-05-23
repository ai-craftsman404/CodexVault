# VaultGPT Handover

## Current Status

VaultGPT is an installable Codex plugin and MVP feature-complete release candidate with a working local engine and a verified `@Chrome` capture path.

The VaultGPT package is release-candidate ready. The previous whole-repository tracked `.codexvault/` publication blocker has been cleared by removing root `.codexvault/` artifacts from git tracking while leaving local files ignored.

## Latest Important Commits

- `8d35f90` Finalize VaultGPT release readiness
- `b9b3fd5` Record VaultGPT implicit Chrome preview pass
- `c2c970c` Clarify VaultGPT Chrome native host blocker
- `940fedf` Record VaultGPT Chrome gate retry
- `c583e51` Update VaultGPT MVP progress docs
- `23554a1` Record VaultGPT installed invocation gates
- `dd5d3e3` Add VaultGPT handover notes
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
- Installed implicit active-tab save preview.
- Final public metadata.
- Final VaultGPT package public-release scan.
- 28 local VaultGPT tests passing.

## 2026-05-23 Session Record

Completed activities:

- Continued from `plugins/vaultgpt/HANDOVER.md`.
- Verified installed-plugin implicit search routing with query `Claude Code Kimi`; result returned `chat_a548c903b716a69a` via SQLite FTS5.
- Verified should-not-trigger behavior for `Explain what a vault is in cryptography.`; VaultGPT did not route.
- Retried `@Chrome` active-tab testing multiple times against Chrome `Profile 3` and `https://chatgpt.com/c/69f75455-25d8-8391-a04d-5943d722c696`.
- Documented blocked Chrome attempts when Codex Chrome could not attach to the extension backend, then later cleared the blocker when `openTabs()` exposed the ChatGPT tab.
- Verified Chrome tab title/URL: `Claude Code vs Kimi`, matching the ChatGPT test URL.
- Claimed the visible Chrome tab and confirmed visible ChatGPT messages were readable.
- Ran implicit active-tab save preview without naming VaultGPT, stopping before save.
- Verified preview evidence: 6 visible messages, role counts user 3 / assistant 3, privacy `passed`, capture confidence `chrome_accessibility_snapshot`, fidelity `warn` only because capture limitations are present.
- Confirmed no Codex thread/project/environment context was captured during the final Chrome preview.
- Finalized public metadata in `plugins/vaultgpt/.codex-plugin/plugin.json`.
- Added public repository/contact/install metadata to `plugins/vaultgpt/README.md`.
- Updated `plugins/vaultgpt/RELEASE-CHECKLIST.md`, `plugins/vaultgpt/design/test-matrix.md`, and this handover with pass/blocker status.
- Added `.codexvault/` to `plugins/vaultgpt/.gitignore`.
- Adjusted synthetic privacy-test strings so public scans do not flag test fixtures as real placeholder emails, tokens, or private paths.
- Ran final VaultGPT verification: 28 tests passing, Python compileall passing, manifest JSON parsing, marketplace JSON parsing, scoped sensitive-pattern scan passing, and tracked-artifact scan passing for `plugins/vaultgpt`.
- Committed only VaultGPT-related final release changes.

Practical insights:

- Use `@Chrome` for signed-in ChatGPT capture; the Codex in-app browser is not an acceptable MVP capture substitute.
- `browser.tabs.selected()` can fail even when the desired ChatGPT tab is visible to Codex Chrome; `browser.user.openTabs()` plus `browser.user.claimTab()` is the reliable pattern for this workflow.
- `@Chrome` availability may depend on the current desktop network/region. In this session, Chrome became available again after switching the desktop network to a US region.
- Missing Chrome native host registration can look similar to a VaultGPT failure, but it is an environment/plugin connectivity issue.
- Broad Codex-thread capture must remain explicitly rejected as a failed pattern, even if it writes a syntactically valid vault record.
- Accessibility/DOM snapshot capture is acceptable for MVP only when the preview labels confidence and limitations; official export remains the authoritative full-history backup path.
- Public scans should distinguish real committed secrets/private paths from intentionally synthetic privacy-scanner fixtures.
- VaultGPT package readiness and whole-repository publication readiness are different; root repo `.codexvault/` artifacts must stay ignored and out of git.

Branch/worktree insight:

- Current VaultGPT branch: `codex/vaultgpt-strategy-notes`.
- Latest VaultGPT release-readiness commit: `8d35f90`.
- The branch is ahead of `origin/main` with the VaultGPT work.
- VaultGPT package tree is clean after commit.
- The Codex UI still shows a large diff because the wider worktree has unrelated dirty/deleted tracked files, especially pre-existing `.codexvault/staging/...` content and unrelated PremortemX/CodexVault changes.
- Do not mix root `.codexvault/` cleanup or unrelated plugin changes into VaultGPT release commits.

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

- pre-existing root `.codexvault/` artifacts were removed from git tracking with `git rm --cached -r .codexvault`; they remain local and are covered by root `.gitignore`
- unrelated private-path examples remain outside VaultGPT in CodexVault/PremortemX docs and tooling; clean those in a separate repo hygiene pass before publishing the entire repository

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
