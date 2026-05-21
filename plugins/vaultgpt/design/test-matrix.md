# VaultGPT Draft Test Matrix

## Plugin

- Plugin name: VaultGPT
- Version: 0.1.0 draft
- Test date: TBD
- Tester: TBD

## Testing Category Coverage

| Category | Priority | In Scope? | Validation Approach | Result / Gap | Notes |
| --- | --- | --- | --- | --- | --- |
| Unit testing | Mandatory | Yes | Script/module tests for vault, prompt, index, export, privacy | Pending |  |
| Integration testing | Mandatory | Yes | End-to-end local vault fixture workflows | Pending |  |
| Workflow testing | Mandatory | Yes | Save/Search/Export/Prompt/Privacy journeys | Pending |  |
| Error and fallback testing | Mandatory | Yes | Malformed export, missing vault, failed export target | Pending |  |
| Boundary testing | Mandatory | Yes | Empty vault, large prompt, duplicate IDs, missing fields | Pending |  |
| Contract/schema testing | Mandatory | Yes | JSON schema/version validation | Pending |  |
| Model-release resilience | Mandatory | Yes | Known/unknown model-label fixtures across import/search/export | Pending | VaultGPT claim must be evidence-backed |
| Negative/abuse testing | Mandatory | Yes | prompt injection, path traversal, unsafe delete | Pending |  |
| Static checks | Mandatory | Yes | PowerShell/Python lint/static checks as applicable | Pending |  |
| Prompt injection testing | Mandatory | Yes | Archived chat contains malicious instructions | Pending | Treat captured content as data |
| Sensitive data leakage | Mandatory | Yes | Secret/PII fixtures and export checks | Pending |  |
| Data provenance | Mandatory | Yes | manifest/source IDs/audit events | Pending |  |
| Tool/action validation | Mandatory | Yes | dry-run/confirmation for bulk actions | Pending |  |
| Human-in-the-loop bypass | Mandatory | Yes | destructive/export override tests | Pending |  |
| Agent-to-agent boundary | Mandatory | Yes | if subagents used for review, main thread adjudicates | Pending | Design-time then runtime |
| Dependency/secret leakage | Mandatory | Yes | git status, ignore rules, secret scan where available | Pending |  |
| Audit trail completeness | Mandatory | Yes | capture/export/privacy/delete events logged | Pending |  |
| GDPR/data retention | Mandatory | Partial | delete/retention documented; no enterprise claims | Pending | MVP local-only |
| RBAC | Mandatory | No | N/A | Not applicable | Single-user local MVP |
| RAG/retrieval security | Mandatory | Partial | FTS context is cited; no vector DB MVP | Pending | Semantic search deferred |
| Memory security | Mandatory | Partial | local vault access and deletion behavior | Pending | no cloud memory |

## Installation

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Local plugin path is valid | `plugins/vaultgpt/` is self-contained |  | Pending |
| `.codex-plugin/plugin.json` exists | Manifest exists |  | Pending |
| Manifest JSON parses | Valid JSON |  | Pending |
| Manifest paths start with `./` | All relative paths valid |  | Pending |
| Plugin can be installed/discovered locally | Codex recognizes plugin |  | Pending |

## Invocation

| Test | Prompt | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- |
| Explicit plugin invocation | Use VaultGPT to search my vault | VaultGPT skill activates |  | Pending |
| Explicit skill invocation | Use the VaultGPT skill to export prompts | VaultGPT skill activates |  | Pending |
| Implicit skill trigger | Save this ChatGPT conversation to my vault | VaultGPT skill activates |  | Pending |
| Should-not-trigger prompt | Explain what a vault is in cryptography | VaultGPT does not trigger |  | Pending |

## Functional Behavior

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Initialize vault | Local vault structure created outside repo |  | Pending |
| Import fixture | Conversations normalize with IDs/hashes |  | Pending |
| Import known model labels | Model metadata preserved and workflows continue |  | Pending |
| Import unknown future model label | Unknown model label preserved, not rejected |  | Pending |
| Capture fixture | Selected-chat payload normalizes |  | Pending |
| Search fixture | Query returns snippets and source IDs |  | Pending |
| Organize | Folder/tag/pin metadata updates only metadata |  | Pending |
| Bulk dry-run | Shows affected items without changes |  | Pending |
| Export | Writes Markdown/JSON/ZIP with manifest |  | Pending |
| Export model metadata | Model labels appear in metadata without controlling behavior |  | Pending |
| Prompt render | Variables fill and preview correctly |  | Pending |
| Chain run | Manual chain step state records correctly |  | Pending |
| Privacy review | Warnings before sensitive export |  | Pending |
| Audit log | Events append without duplicating full content |  | Pending |

## UX Journey Tests

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| First-time Save Chat | useful chat saved under 30 seconds conceptually/manual |  | Pending |
| Returning Search Vault | saved chat/prompt found under 20 seconds conceptually/manual |  | Pending |
| Backup Vault | local backup created under 60 seconds conceptually/manual |  | Pending |
| Convert chat to prompt | candidate prompt previewed before save |  | Pending |
| Prompt variables | form preview shown before use |  | Pending |

## Environment

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Works without network for local vault operations | import/search/export work offline |  | Pending |
| Handles missing Chrome extension | fallback import path documented |  | Pending |
| Windows path behavior checked | reserved names and path separators safe |  | Pending |
| No private files required for public example | fixtures synthetic only |  | Pending |

## Result

- Release candidate: no
- Blocking issues:
  - implementation not started
  - Chrome capture path not verified
  - security review not complete
- Follow-up:
  - convert this draft to release test matrix after scaffold
