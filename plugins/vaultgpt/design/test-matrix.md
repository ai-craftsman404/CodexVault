# VaultGPT Draft Test Matrix

## Plugin

- Plugin name: VaultGPT
- Version: 0.1.0 draft
- Test date: 2026-05-22
- Tester: Codex

## Testing Category Coverage

| Category | Priority | In Scope? | Validation Approach | Result / Gap | Notes |
| --- | --- | --- | --- | --- | --- |
| Unit testing | Mandatory | Yes | Script/module tests for vault, prompt, index, export, privacy | Pass | 26 tests passing for MVP foundation |
| Integration testing | Mandatory | Yes | End-to-end local vault fixture workflows | Pass | CLI E2E passed for init/import/reindex/search/export |
| Workflow testing | Mandatory | Yes | Save/Search/Export/Prompt/Privacy journeys | Partial pass | local CLI workflows pass; constrained Chrome save preview/confirm passed; remaining plugin workflows pending |
| Error and fallback testing | Mandatory | Yes | Malformed export, missing vault, failed export target | Pending |  |
| Boundary testing | Mandatory | Yes | Empty vault, large prompt, duplicate IDs, missing fields | Pending |  |
| Contract/schema testing | Mandatory | Yes | JSON schema/version validation | Partial pass | schema version and manifest fields covered in unit tests |
| Model-release resilience | Mandatory | Yes | Known/unknown model-label fixtures across import/search/export | Partial pass | unknown model label preservation and official model field covered; more fixtures needed |
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
| Explicit skill invocation | Use the VaultGPT skill to export prompts | VaultGPT skill activates |  | Pending |
| Implicit skill trigger | Save this ChatGPT conversation to my vault | VaultGPT skill activates |  | Pending |
| Should-not-trigger prompt | Explain what a vault is in cryptography | VaultGPT does not trigger |  | Pending |
| Current-session tool discovery | `tool_search` query for `vaultgpt` | VaultGPT is visible after reload/install | Visible in installed session context after reload/install | Pass |

## Functional Behavior

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Initialize vault | Local vault structure created outside repo | Pass | Partial |
| Import fixture | Conversations normalize with IDs/hashes | Pass | Pass |
| Import known model labels | Model metadata preserved and workflows continue | Pass | Partial |
| Import unknown future model label | Unknown model label preserved, not rejected | Pass | Partial |
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

## UX Journey Tests

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| First-time Save Chat | useful chat saved under 30 seconds conceptually/manual | Chrome capture preview/confirm/save worked with constrained source | Pass with note: accessibility snapshot may omit some detailed bullet text |
| Returning Search Vault | saved chat/prompt found under 20 seconds conceptually/manual |  | Pending |
| Backup Vault | local backup created under 60 seconds conceptually/manual |  | Pending |
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
  - real export edge cases not verified
  - public manifest metadata not finalized
- Follow-up:
  - verify search/export against saved Chrome-captured record
  - verify implicit invocation and should-not-trigger behavior
  - replace public metadata before GitHub publication
