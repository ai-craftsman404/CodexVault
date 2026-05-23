# VaultGPT Viability Assessment

## Plugin

- Working name: VaultGPT
- Date: 2026-05-21
- Assessor: Codex

## Scoring

| Area | Score | Notes |
| --- | ---: | --- |
| Usefulness | 5 | Targets features users already pay for or complain about. |
| Uniqueness | 4 | Feature categories exist, but Codex-native free replacement plus governance is differentiated. |
| Technical feasibility | 3 | Local vault/search/export is feasible; Chrome capture has UI and permission risk. |
| Low maintenance burden | 3 | Browser capture and ChatGPT schema drift create maintenance load. |
| Low security/privacy risk | 3 | Risk is manageable with local-first defaults, approvals, and privacy review. |
| GitHub visibility value | 5 | Strong public positioning: free power-extension alternative without opaque third-party extension reliance. |

## Decision

- Total score: 23 / 30
- Decision: proceed to design spec
- Reason: The concept has a clear business wedge and feasible local-first core, provided browser capture remains constrained and user-approved.

## MVP Recommendation

Build the cancellation-worthy replacement set:

- full-text local search
- unlimited folders/tags/pins
- bulk export/backup
- bulk move/archive/delete/tag with safety
- prompt vault with variables
- simple prompt chains
- Codex Chrome selected-chat capture
- privacy review
- audit/provenance logs

## Primary Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| ChatGPT UI changes break capture | Medium | High | Keep official export import as fallback; isolate capture adapter. |
| Scope expands into generic AI sidebar | Medium | High | Keep MVP focused on paid-extension replacement features. |
| Privacy claims become overbroad | Medium | High | Say reduced attack surface and local-first controls, not guaranteed security. |
| Bulk actions cause user harm | Medium | High | Require dry-run, confirmation, undo, and audit logs. |
| Prompt injection through archived chats | High | Medium | Treat all imported/captured chat content as untrusted data. |

