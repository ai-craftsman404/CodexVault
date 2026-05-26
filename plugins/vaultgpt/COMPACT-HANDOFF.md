# VaultGPT Compact Handoff

## Current Decision

VaultGPT public preview is no longer the old single-tab/local-archive MVP.

The public-preview focus is:

```text
Selective Async ChatGPT Export
Export exactly the ChatGPT conversations you choose, not your entire account.
```

## Current Architecture

Final public-preview architecture:

```text
assistant-level @Chrome capture
-> normalized capture payloads
-> VaultGPT selective export ingest
-> privacy/fidelity/audit
-> ZIP package
```

Important correction:

- There is no documented official Python/CLI API for a Codex plugin to directly call the Codex Chrome extension.
- `VAULTGPT_CHROME_BRIDGE_MODULE` is a future seam, not a public-preview dependency.
- `--provider codex` should remain blocked unless a supported bridge exists.
- Public preview uses assistant-mediated `@Chrome` capture plus `--ingest-payloads <json>`.

Working Chrome startup recipe:

```bat
cmd /c start chrome.exe --profile-directory="Profile 3" "https://chatgpt.com/"
```

Then use only the Codex Chrome skill surface:

- `browser.user.openTabs()`
- `browser.user.claimTab(tab)`
- `tab.url()`
- `tab.title()`
- `tab.playwright.domSnapshot()`

Do not substitute Playwright MCP, shell-driven bridge code, or the Codex in-app browser for this path.

## Implementation Status From Build Session

Implemented in dedicated worktree/session:

- URL ingestion, canonicalization, duplicate/invalid reporting.
- 25 URL cap.
- async job model under `jobs/<job_id>/`.
- retry/status/preview.
- ZIP-only package.
- simulation provider.
- `CodexChromeCaptureProvider` seam added but blocked for public preview without bridge.
- `--ingest-payloads <json>` added for assistant-produced normalized payloads.
- `--provider codex` explicitly blocked in public preview.
- README updated to describe assistant-mediated Codex Chrome capture.
- Test suite reported passing: 33 tests.

## Next E2E Task

Use 2-3 real ChatGPT conversation URLs.

Flow:

1. In a Codex session where `@Chrome` is available, assistant opens/claims/reads each selected ChatGPT URL.
2. Assistant creates normalized capture payloads with URL, title, messages, role counts, confidence, limitations, privacy/fidelity status.
3. Save payloads to JSON.
4. Run VaultGPT selective export with `--ingest-payloads <json>`.
5. Verify job status, preview, privacy/fidelity, ZIP package, manifest, Markdown/JSON, events, failures.
6. Confirm no Codex thread/project/environment context is captured.

Do not claim `--provider codex` works unless a real supported bridge is provided.

## Scope Guardrails

Do not implement for public preview:

- ChatGPT App integration.
- Direct ChatGPT-to-Codex plugin invocation.
- Cloud Codex delegation.
- Open-tab discovery.
- Full account crawl.
- True parallel Chrome capture.
- Native messaging host.
- Custom browser extension.
- Playwright/Profile 3 automation as default path.
- Generic RAG/search as the product wedge.

## Key Files

- `plugins/vaultgpt/IMPLEMENTATION-HANDOFF-SELECTIVE-ASYNC-EXPORT.md`
- `plugins/vaultgpt/notes/mvp-scope.md`
- `plugins/vaultgpt/notes/feature-candidates.md`
- `plugins/vaultgpt/notes/strategy-roadmap.md`
- `plugins/vaultgpt/scripts/vaultgpt/lib/selective_export.py`
- `plugins/vaultgpt/scripts/vaultgpt/vaultgpt.py`
- `plugins/vaultgpt/scripts/vaultgpt/tests/test_core.py`

## Before Release

- Run real assistant-mediated `@Chrome` E2E with user-provided URLs.
- Verify ZIP contents and manifests.
- Update README/test matrix/release checklist to match assistant-mediated flow.
- Run full tests.
- Scan for private vault data, paths, screenshots, exports, or secrets.
