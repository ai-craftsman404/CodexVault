# VaultGPT

VaultGPT gives you the ChatGPT power-extension features people normally pay for, such as saved chats, folders, tags, search, exports, prompt libraries, and backups, but free, local-first, and powered by Codex instead of an opaque third-party browser extension.

If your ChatGPT history has become valuable knowledge, VaultGPT helps you keep ownership of it: preview before saving, store it locally in open formats, search it later, reuse prompts, export backups, and keep an audit trail without handing your conversation archive to another extension vendor.

It is designed to replace the most useful paid/capped workflows from popular ChatGPT browser extensions:

- save useful ChatGPT conversations
- organize chats with folders, tags, pins, and an inbox
- search across saved chats and prompts
- export or back up chats to open local formats
- build a reusable prompt vault with variables and simple chains
- review privacy before saving or exporting
- keep an audit trail of what was captured and where it came from

VaultGPT's core bet is simple: users should own their ChatGPT history locally, in open files, using Codex-native workflows instead of opaque browser-extension storage.

## Why VaultGPT

Many ChatGPT users already pay for third-party extensions because ChatGPT history becomes hard to manage at scale. The common paid features are not exotic: better search, folders, prompt libraries, bulk export, backups, tags, pins, and workflow shortcuts.

VaultGPT targets that demand directly:

- Free instead of subscription-gated.
- Local-first instead of extension-cloud-first.
- Codex-native instead of opaque third-party scraping.
- Open formats instead of lock-in.
- Explicit preview and confirmation instead of silent capture.
- Privacy review and audit logs by default.

The goal is not to win by adding more UI complexity. The goal is to give users the familiar high-value extension workflows they already understand, but in a safer Codex-powered package.

## MVP Focus

- Codex Chrome selected-chat capture with explicit approval through the Chrome skill runtime (`browser.user.openTabs()` + `browser.user.claimTab()`)
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

VaultGPT is positioned as the free, privacy-first alternative to paid ChatGPT productivity extensions.

The adoption pitch:

```text
Keep the ChatGPT extension features you already want. Drop the subscription and the opaque data risk.
```

For MVP, VaultGPT prioritizes competitor-parity features that users already value over speculative novelty. Its main differentiator is the delivery model: local-first storage, Codex Chrome capture, transparent operations, and a path to deeper Codex agent workflows over time.

## Cross-Platform Design

VaultGPT is designed to be operating-system agnostic across Windows, macOS, and Linux. Core vault workflows use local filesystem paths, JSON, SQLite FTS5 when available, Markdown, and ZIP archives rather than OS-specific services.

Codex Chrome capture depends on the Codex desktop app, Chrome, the Codex Chrome extension, and the Chrome skill runtime being able to see the selected Chrome profile. Those integration requirements can vary by platform, network region, and Codex release.

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

VaultGPT is an MVP feature-complete release candidate.

Repo-local plugin discovery metadata is present at `.agents/plugins/marketplace.json`. A running Codex session must reload/install the plugin before live skill invocation can be accepted as passed.

Installed-plugin explicit invocation has been verified. The first broad save test over-captured Codex project/environment context and is treated as a failed pattern. The corrected Chrome skill workflow successfully previewed and saved a constrained ChatGPT browser conversation after confirmation.

Implicit search routing, should-not-trigger behavior, and the implicit active-tab save preview have also been verified. The active-tab preview used the Chrome skill against a real ChatGPT tab, showed privacy and fidelity results, and stopped before saving.

The install surface now uses multiple starter actions rather than a single broad save prompt:

- show available actions
- save selected ChatGPT browser conversation
- import official ChatGPT export
- search local vault
- export or back up vault items
- create or reuse prompt variables

Implemented and verified:

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
- installed explicit VaultGPT invocation
- installed Chrome-skill ChatGPT capture preview/save with approval
- search and export against a Chrome-captured record
- implicit VaultGPT search routing
- implicit active ChatGPT tab save preview with no write before confirmation
- should-not-trigger behavior for unrelated cryptography prompts
- 28 local VaultGPT tests

Deferred hardening:

- real exported ChatGPT edge-case validation, deferred to post-MVP/public-beta unless a safe redacted sample becomes available

## Public Metadata

- Repository: `https://github.com/ai-craftsman404/CodexVault`
- Plugin path: `plugins/vaultgpt`
- Maintainer contact: `https://github.com/ai-craftsman404`
- Privacy model: see [Privacy Model](#privacy-model)
- Terms/license: see `LICENSE`

## Installation

Until VaultGPT is split into a standalone repository, install it from this repository path:

```text
https://github.com/ai-craftsman404/CodexVault/tree/main/plugins/vaultgpt
```

## User Workflows

### Simple Example: Save And Find One Useful Chat

Use case: you had a useful ChatGPT conversation about choosing between Claude Code, Kimi, and DeepSeek, and you want to save it locally so you can find it later.

1. Open that ChatGPT conversation in Chrome.
2. In Codex, type:

```text
Save my current active ChatGPT tab to VaultGPT. Preview first and do not save until I confirm.
```

3. VaultGPT shows a preview, for example:

```text
Title: Claude Code vs Kimi
Source: https://chatgpt.com/c/...
Visible messages: 6
Roles: user 3, assistant 3
Privacy: passed
Capture confidence: chrome_accessibility_snapshot
Fidelity: warn, because browser snapshots can miss hidden or collapsed content
Target folder: Inbox
```

4. If the preview looks correct, reply:

```text
Confirm save.
```

5. Later, search for it:

```text
Search my VaultGPT archive for Claude Code Kimi.
```

6. VaultGPT returns the saved chat from your local vault. You can then export it, tag it, pin it, or turn part of it into a reusable prompt.

### Save The Current ChatGPT Tab

1. Open the target ChatGPT conversation in Chrome.
2. Confirm the Codex Chrome extension is connected and the Chrome skill can see the active tab.
3. In Codex, ask VaultGPT to save the current active ChatGPT tab.
4. Review the preview before saving. It should show the ChatGPT title, URL, visible message count, role counts, privacy result, capture confidence, fidelity status, target folder/status, and proposed record ID.
5. Confirm only if the preview scope is correct.
6. VaultGPT saves the chat to the local vault, records an audit event, and rebuilds the search index.

Example prompt:

```text
Save my current active ChatGPT tab to VaultGPT. Preview first and do not save until I confirm.
```

Expected safety behavior:

- VaultGPT must not save before confirmation.
- VaultGPT must not capture the Codex thread, project instructions, shell output, or local environment context as a substitute for the ChatGPT tab.
- If the Chrome skill cannot see the active ChatGPT tab, the save should be treated as blocked.

### Search The Local Vault

Use search when you want to find saved chats, prompts, or imported export content.

Example prompt:

```text
Search my VaultGPT archive for Claude Code Kimi.
```

VaultGPT searches the local index first and can fall back to JSON search when SQLite FTS5 is unavailable.

### Import An Official ChatGPT Export

Use official ChatGPT export import for fallback, backup, or batch loading.

Typical flow:

1. Export your ChatGPT data from ChatGPT.
2. Keep the export local.
3. Ask VaultGPT to import the `conversations.json` file.
4. Rebuild/search the local index.

Synthetic official-export edge cases are covered by tests. Real redacted export validation is deferred to post-MVP/public-beta unless a safe sample is available.

### Export Or Back Up The Vault

VaultGPT can export saved vault items to Markdown, JSON, or ZIP.

Typical flow:

1. Choose the scope: selected items, folder, tag, saved search, prompts only, chats only, or full vault.
2. Choose the format: Markdown, JSON, or ZIP.
3. Review privacy status and export preview.
4. Confirm export.
5. VaultGPT writes output with a provenance manifest and audit event.

### Use Prompt Variables And Chains

VaultGPT supports a local prompt vault with variables and manual prompt chains.

Typical flow:

1. Save or create a prompt template.
2. Use `{field}` or `{{field}}` placeholders for variables.
3. Fill variables before reuse.
4. For chains, run steps manually with preview, pause, retry, skip, or stop.

### MVP Constraints And Caveats

- MVP capture target is the current active ChatGPT tab.
- Selected-tab and multi-tab capture are deferred.
- Full unattended account crawl is intentionally not part of MVP.
- Chrome capture uses an accessibility snapshot, so hidden, collapsed, or virtualized content may be incomplete.
- VaultGPT records capture confidence and fidelity status so users can see this limitation.
- Official export import remains the more complete fallback for bulk historical archives.
- Local vault data, official exports, and generated backups are private runtime data and should not be committed to git.

## Codex Chrome Availability

VaultGPT's active-tab capture depends on the Codex Chrome extension and the Chrome skill runtime being available in the current desktop environment. If the Chrome skill reports that the browser or extension is unavailable, confirm that Codex Chrome access is supported for the current network region. During MVP testing, the final Chrome retry only passed after switching the desktop network to a US region; non-approved regions may block the bridge even when Chrome and the extension appear installed.

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
