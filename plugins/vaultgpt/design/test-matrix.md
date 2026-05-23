# VaultGPT Draft Test Matrix

## Plugin

- Plugin name: VaultGPT
- Version: 0.1.0 draft
- Test date: 2026-05-23
- Tester: Codex

## Testing Category Coverage

| Category | Priority | In Scope? | Validation Approach | Result / Gap | Notes |
| --- | --- | --- | --- | --- | --- |
| Unit testing | Mandatory | Yes | Script/module tests for vault, prompt, index, export, privacy | Pass | 28 tests passing for MVP foundation |
| Integration testing | Mandatory | Yes | End-to-end local vault fixture workflows | Pass | CLI E2E passed for init/import/reindex/search/export |
| Workflow testing | Mandatory | Yes | Save/Search/Export/Prompt/Privacy journeys | Partial pass | local CLI workflows pass; constrained Chrome save preview/confirm passed; installed search prompt verified; active Chrome tab unavailable for final implicit save retest |
| Error and fallback testing | Mandatory | Yes | Malformed export, missing vault, failed export target | Partial pass | unsupported export shape raises; more failed-target tests pending |
| Boundary testing | Mandatory | Yes | Empty vault, large prompt, duplicate IDs, missing fields | Partial pass | synthetic official export edge fixture covers missing title/id fallback and empty messages |
| Contract/schema testing | Mandatory | Yes | JSON schema/version validation | Partial pass | schema version and manifest fields covered in unit tests |
| Model-release resilience | Mandatory | Yes | Known/unknown model-label fixtures across import/search/export | Pass | unknown model label preservation, official model field, and synthetic edge model covered |
| Negative/abuse testing | Mandatory | Yes | prompt injection, path traversal, unsafe delete | Pending |  |
| Static checks | Mandatory | Yes | PowerShell/Python lint/static checks as applicable | Partial pass | Python compileall and JSON parse pass |
| Prompt injection testing | Mandatory | Yes | Archived chat contains malicious instructions | Partial pass | fixture proves import/export treats malicious text as inert data |
| Sensitive data leakage | Mandatory | Yes | Secret/PII fixtures and export checks | Partial pass | first broad capture produced warning; constrained Chrome capture passed with no findings |
| Data provenance | Mandatory | Yes | manifest/source IDs/audit events | Partial pass | export manifest and audit append tests covered |
| Tool/action validation | Mandatory | Yes | dry-run/confirmation for bulk actions | Partial pass | bulk plan is dry-run and requires confirmation |
| Human-in-the-loop bypass | Mandatory | Yes | destructive/export override tests | Pending |  |
| Agent-to-agent boundary | Mandatory | Yes | if subagents used for review, main thread adjudicates | Pending | Design-time then runtime |
| Dependency/secret leakage | Mandatory | Yes | git status, ignore rules, secret scan where available | Partial pass | scoped VaultGPT scan found no real secret/private-path hits |
| Audit trail completeness | Mandatory | Yes | capture/export/privacy/delete events logged | Partial pass | init/import/export and constrained Chrome capture covered; delete pending |
| GDPR/data retention | Mandatory | Partial | delete/retention documented; no enterprise claims | Pending | MVP local-only |
| RBAC | Mandatory | No | N/A | Not applicable | Single-user local MVP |
| RAG/retrieval security | Mandatory | Partial | FTS context is cited; no vector DB MVP | Partial pass | derived SQLite FTS5 optional; semantic search deferred |
| Memory security | Mandatory | Partial | local vault access and deletion behavior | Pending | no cloud memory |

## Installation

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Local plugin path is valid | `plugins/vaultgpt/` is self-contained | Pass | Pass |
| `.codex-plugin/plugin.json` exists | Manifest exists | Pass | Pass |
| Manifest JSON parses | Valid JSON | Pass | Pass |
| Manifest paths start with `./` | All relative paths valid | Pass | Pass |
| Repo-local marketplace entry exists | `.agents/plugins/marketplace.json` includes VaultGPT | Pass | Pass |
| Plugin can be installed/discovered locally | Codex recognizes plugin | VaultGPT installed and appeared in Codex plugin invocation UI on 2026-05-22 | Pass |

## Invocation

| Test | Prompt | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- |
| Explicit plugin invocation | Use VaultGPT to save current conversation | VaultGPT skill activates | Pass: plugin invoked and produced local record/audit output | Pass |
| Explicit skill invocation | Use the VaultGPT skill to export prompts | VaultGPT skill activates | Covered by installed explicit invocation and export/search verification; prompt-only export remains a low-risk follow-up | Partial |
| Implicit skill trigger | Save my current active ChatGPT tab to VaultGPT. Preview first and do not save until I confirm. | VaultGPT activates and uses `@Chrome`; no save before confirmation | Blocked on 2026-05-23: Chrome extension connection was live, but `openTabs()` returned `[]` and `browser.tabs.selected()` returned `No active tab found`; no broad Codex-thread capture was accepted as success | Blocked |
| Implicit search trigger | Search my VaultGPT archive for Claude Code Kimi. | VaultGPT activates or routes to local VaultGPT search; returns saved record or index status | Pass: local installed vault search returned `chat_a548c903b716a69a`, title `Claude Code vs Kimi`, mode `sqlite-fts5`, index status `ok` | Pass |
| Should-not-trigger prompt | Explain what a vault is in cryptography | VaultGPT does not trigger | Pass: tool discovery for the exact negative prompt returned no tools; VaultGPT was not routed | Pass |
| Current-session tool discovery | `tool_search` query for `vaultgpt` | VaultGPT is visible after reload/install | Visible in installed session context after reload/install | Pass |

## Functional Behavior

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Initialize vault | Local vault structure created outside repo | Pass | Partial |
| Import fixture | Conversations normalize with IDs/hashes | Pass | Pass |
| Import known model labels | Model metadata preserved and workflows continue | Pass | Pass |
| Import unknown future model label | Unknown model label preserved, not rejected | Pass | Pass |
| Import synthetic official export edge cases | Missing title, conversation_id, multipart dict content, tool result | Pass | Pass |
| Capture fixture | Selected-chat payload normalizes | Pass with approval/privacy/audit checks | Pass |
| Search fixture | Query returns snippets and source IDs | Pass | Pass |
| SQLite FTS fixture | Rebuild/search works when FTS5 is available | Pass | Pass |
| Organize | Folder/tag/pin metadata updates only metadata | Pass | Pass |
| Bulk dry-run | Shows affected items without changes | Pass | Pass |
| Export | Writes Markdown/JSON/ZIP with manifest | Pass | Pass |
| Export model metadata | Model labels appear in metadata without controlling behavior | Pass | Pass |
| Prompt render | Variables fill and preview correctly | Pass | Pass |
| Chain run | Manual chain step state records correctly | Pass | Pass |
| Privacy review | Warnings before sensitive export | Pass with manifest warning counts | Partial |
| Audit log | Events append without duplicating full content | Pass | Partial |
| CLI E2E | init/import-official/reindex/search/export zip | Pass: search hit `e2e_chat`, mode `sqlite-fts5`, backup/audit exist | Pass |
| Installed broad save E2E | Save current visible conversation with privacy/audit | Plugin wrote record and audit event | Warn: captured Codex project/environment context; recorded as failed pattern |
| Installed Chrome capture preview | Use VaultGPT with `@Chrome` to preview open ChatGPT conversation | Preview title, URL, message count, roles, privacy, folder/status, ID; no save before confirmation | Pass |
| Installed Chrome capture save | Confirm saving previewed Chrome ChatGPT conversation | Saved `chat_a548c903b716a69a`, privacy passed, audit recorded URL/message count/source | Pass |
| Installed Chrome record search | Search `.codexvault` for `Claude Code Kimi DeepSeek` | Returned `chat_a548c903b716a69a` via SQLite FTS5 | Pass |
| Installed Chrome record export | Export `.codexvault` to ZIP | ZIP export succeeded and manifest included `chat_a548c903b716a69a` | Pass with note: test vault also contained earlier failed broad-capture record |
| Installed implicit Chrome active-tab retest | Prompt without explicit plugin name: save current active ChatGPT tab, preview first, no save until confirm | Uses `@Chrome` current active ChatGPT tab; previews only constrained ChatGPT source; no write before confirmation | Blocked on 2026-05-23: Chrome extension connected, but no active/open tab was exposed to Codex Chrome; broad Codex-thread capture remains rejected as non-success | Blocked |

## UX Journey Tests

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| First-time Save Chat | useful chat saved under 30 seconds conceptually/manual | Chrome capture preview/confirm/save worked with constrained source | Pass with note: accessibility snapshot may omit some detailed bullet text |
| Returning Search Vault | saved chat/prompt found under 20 seconds conceptually/manual | `Claude Code Kimi DeepSeek` returned Chrome-captured record | Pass |
| Backup Vault | local backup created under 60 seconds conceptually/manual | ZIP export succeeded for `.codexvault` | Pass with note: test vault included failed broad-capture artifact |
| Convert chat to prompt | candidate prompt previewed before save |  | Pending |
| Prompt variables | form preview shown before use |  | Pending |

## Environment

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Works without network for local vault operations | import/search/export work offline | Pass via local temp fixture | Pass |
| Handles missing Chrome extension | fallback import path documented |  | Pending |
| Windows path behavior checked | reserved names and path separators safe |  | Pending |
| No private files required for public example | fixtures synthetic only |  | Pending |

## Result

- Release candidate: not yet
- Blocking issues:
  - public manifest metadata not finalized
  - final installed implicit active-tab save retest needs a Chrome tab visible to Codex Chrome
- Follow-up:
  - rerun implicit active-tab save retest when Chrome exposes an active ChatGPT tab to Codex Chrome
  - keep real export validation as post-MVP/public-beta hardening unless redacted sample becomes available
  - replace public metadata before GitHub publication
