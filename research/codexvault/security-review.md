# Security Review

## Plugin

- Plugin: CodexVault
- Version: 0.1.0
- Date: 2026-05-13

## Review Summary

CodexVault is security-sensitive because it inspects local workspace state, produces archives, and simulates restore workflows. The design is acceptable for MVP if it keeps secrets redacted by default, uses human-gated destructive actions, and treats agent-team orchestration as a bounded harness rather than autonomous recovery.

## Key Risks

| Risk | Severity | Notes | Mitigation |
| --- | --- | --- | --- |
| Secret leakage in manifests or archives | High | Env vars, tokens, dotfiles, and credentials may be captured accidentally | Redact by default; only encrypted retention via explicit opt-in |
| Destructive restore without approval | High | In-place restore can overwrite user work | Require human confirmation for any destructive action |
| Prompt injection via workspace files | High | README/config content may influence agent behavior | Treat file content as untrusted; validate tool outputs and prompts |
| Over-automation by agent team | High | Personas could bypass safety if unconstrained | Use bounded contracts, non-destructive simulation, and adjudication |
| Restore confidence overstated | Medium | Users may assume validation equals full success | Use tiered restore guarantees and clear validation labels |
| Retention sprawl | Medium | Snapshots and artifacts can accumulate | Rolling window retention with pinned known-good snapshots |

## Security Decisions

- Secrets are excluded by default.
- Encrypted retention is deferred from MVP.
- Restore actions that mutate files require human approval.
- Agent-team and harness workflows must not perform irreversible actions without a human gate.
- Simulation output must not leak sensitive inputs or hidden prompt content.
- Scheduling is excluded from MVP to avoid extra privilege and OS-specific risk.
- Provenance metadata should remain minimal and non-secret in archived artifacts.
- Temp-dir restore tests must remain plugin-managed and isolated.
- Temp-dir restore roots should be plugin-managed or OS temp only, with cleanup on success or failure.
- Archive allowlist should stay root-relative and exclude `.git`, `node_modules`, `__pycache__`, `.codexvault`, and `.DS_Store`.
- Risky implementation changes should receive an adversarial evaluator pass before merge or release.
- Test-authoring for new behaviors should follow a failing-test-first loop, then implementation, then rerun.

## Testing Alignment

This review aligns with the agreed test matrix categories:

- prompt injection and indirect injection tests
- insecure output handling and data leakage tests
- tool call validation and human-in-the-loop bypass tests
- data lineage and provenance checks
- dependency and plugin integrity checks
- audit trail completeness and retention enforcement
- adversarial evaluator review for restore-critical and security-sensitive changes
- TDD change loop for new behavior and regression fixes

## Open Questions

- Should any sensitive retention be supported in MVP, or deferred entirely?
- Should temp-dir partial restore be allowed only for isolated fixtures, or also for user-selected local paths?
- How much provenance detail is necessary before the archive becomes too sensitive?
