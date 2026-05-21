# VaultGPT Security Review

## Status

- Review date: 2026-05-21
- Release state: MVP implementation, not public-release ready
- Decision: proceed with local MVP development; block public release until live capture and release packaging checks pass

## Security Model

VaultGPT is local-first. The vault stores imported chats, prompts, chains, indexes, audit logs, and exports on the user's filesystem. No cloud sync, telemetry, or remote service is part of the MVP design.

Archived conversations are untrusted data. VaultGPT must not execute instructions found inside saved chats, prompts, imports, or exports.

## Implemented Controls

- OS-native default vault paths with `VAULTGPT_HOME` and `--vault-path` override.
- Runtime vault data is outside the plugin directory by default.
- Append-only JSONL audit events for initialization, imports, and exports.
- Export manifests include schema version, record IDs, titles, model labels, and content hashes.
- Prompt variables require explicit values before render.
- Bulk actions currently produce dry-run plans requiring confirmation.
- Heuristic privacy scanner detects common emails, local Windows paths, private URLs, generic tokens, and OpenAI-style API keys.
- Unknown/future ChatGPT model labels are preserved as metadata and do not control execution behavior.
- SQLite FTS5 index is derived from canonical JSON records; JSON scan fallback remains available.

## Current Risks

| Risk | Severity | MVP Handling | Release Requirement |
| --- | --- | --- | --- |
| Live browser capture may over-collect page content | High | selected-chat capture is not released as verified yet | add constrained capture test and manual verification notes |
| Imported chats may contain prompt injection | High | treated as data in design and tests | add negative fixture proving archived instructions are not followed |
| Heuristic privacy scanner is not DLP | Medium | documented as warning-only | README must avoid compliance/security guarantees |
| Official ChatGPT export shapes may vary | Medium | tolerant synthetic parser exists | test against redacted real export shapes before public release |
| Local vault can contain sensitive data | Medium | local-only by default | document backup/delete responsibilities |
| Placeholder URLs/emails in manifest | Low | acceptable during draft | replace before public publication |

## Non-Goals For MVP

- Enterprise DLP certification.
- Cloud sync security model.
- Team RBAC or admin governance.
- Full unattended ChatGPT account crawl.
- Guaranteed compatibility with future ChatGPT UI changes.

## Required Release Gates

- Run full unit suite.
- Parse `.codex-plugin/plugin.json`.
- Verify no committed runtime vault data, exports, screenshots, secrets, or private paths.
- Verify live Codex Chrome selected-chat capture uses explicit approval and only stores intended content.
- Add negative prompt-injection fixture.
- Complete `design/test-matrix.md` with final results.
- Replace placeholder manifest URLs and maintainer email.
