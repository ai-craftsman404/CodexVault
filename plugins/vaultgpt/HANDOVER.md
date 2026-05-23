# VaultGPT Handover

## Current Status

VaultGPT is an installable Codex plugin with a working local engine and a verified `@Chrome` capture path.

Do not call this a finished public MVP yet. Remaining work is mostly installed-plugin acceptance testing and final public metadata.

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

## Critical Lessons Learned

- Do not use Codex in-app browser for signed-in ChatGPT capture.
- Use `@Chrome` with the connected Codex Chrome extension.
- Primary MVP capture target is current active ChatGPT tab.
- Specific ChatGPT URL is fallback/debug only.
- Selected/multiple tabs are deferred.
- Broad visible Codex thread capture is a failed pattern and must not be treated as MVP success.
- Chrome accessibility snapshot is acceptable for MVP if labeled with capture confidence and limitations.
- Fidelity review mitigates, but cannot prove, full completeness if the snapshot omits hidden/virtualized content.

## Verified Chrome Capture Evidence

Test chat:

```text
https://chatgpt.com/c/69f75455-25d8-8391-a04d-5943d722c696
```

Saved record:

```text
C:\Users\georg\codex-project\Code-Plugin-Guru\.codexvault\conversations\chat_a548c903b716a69a.json
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
C:\Users\georg\codex-project\Code-Plugin-Guru\.codexvault\audit.jsonl
```

Search verification command:

```powershell
python C:\Users\georg\.codex\plugins\cache\code-plugin-guru-local\vaultgpt\0.1.0\scripts\vaultgpt\vaultgpt.py --vault-path C:\Users\georg\codex-project\Code-Plugin-Guru\.codexvault search "Claude Code Kimi DeepSeek"
```

Expected result:

- returns `chat_a548c903b716a69a`
- search mode: `sqlite-fts5`

## Remaining MVP Gates

### 1. Installed-Plugin Invocation Tests

Run in a fresh/new Codex chat where VaultGPT is installed.

Implicit trigger prompt:

```text
Save my current active ChatGPT tab to VaultGPT. Preview first and do not save until I confirm.
```

Expected:

- VaultGPT activates without explicit plugin mention.
- It uses `@Chrome`, not in-app browser.
- It previews title, URL, message count, roles count, privacy, capture confidence, limitations, folder/status, proposed ID.
- It does not save before confirmation.

Search prompt:

```text
Search my VaultGPT archive for Claude Code Kimi.
```

Expected:

- VaultGPT activates.
- Returns saved record or says no matches with index status.

Should-not-trigger prompt:

```text
Explain what a vault is in cryptography.
```

Expected:

- VaultGPT should not activate.

Record results in:

- `plugins/vaultgpt/design/test-matrix.md`
- `plugins/vaultgpt/RELEASE-CHECKLIST.md`

### 2. Final Public Metadata

Leave until the end, per user decision.

Need:

- public GitHub repo URL
- maintainer email or contact URL
- homepage/privacy/terms URLs or remove/replace placeholders

Files:

- `plugins/vaultgpt/.codex-plugin/plugin.json`
- `plugins/vaultgpt/README.md`
- `plugins/vaultgpt/RELEASE-CHECKLIST.md`

### 3. Final Public Scan

Before release:

- ensure `.codexvault/` is not committed
- ensure no runtime vault data is committed
- scan for private paths, API keys, screenshots, exports
- verify `plugins/vaultgpt/.gitignore`

Useful commands:

```powershell
python -m unittest discover -s tests
python -m json.tool plugins/vaultgpt/.codex-plugin/plugin.json > $null
python -m json.tool .agents/plugins/marketplace.json > $null
rg -n "sk-[A-Za-z0-9]|sk-proj|OPENAI_API_KEY|C:\\Users\\|/mnt/data|token=" plugins/vaultgpt
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
