# CodexVault Release Checklist

## Release Target

- Plugin: CodexVault
- Version: v1b
- Scope: discovery-intelligence increment on top of the workspace-first MVP

## Pre-Release Checks

- [x] Manifest schema is valid and versioned.
- [x] Discovery, manifest, snapshot, restore-plan, verify, and simulation scripts are present.
- [ ] Python CLI is the supported user-facing entrypoint across Windows, Linux, and macOS.
- [x] Snapshot archives use the approved allowlist and exclude secrets by default.
- [x] SHA-256 checksum sidecar is emitted and verified.
- [x] Temp-dir restore simulation stays isolated and removes its temp root on completion or failure.
- [x] Negative-path fixtures cover malformed JSON, missing fields, path traversal, and checksum failure.
- [x] v1b config schema and example configs validate against the documented path contract.
- [x] Self-improvement loop uses tiered fidelity labels, safe deltas only, and bounded adversarial rehearsal.
- [x] New behavior was added through a TDD loop where applicable.
- [x] Adversarial evaluator review ran for restore-critical or security-sensitive changes.
- [ ] Human approval remains required for destructive restore actions.
- [ ] Scheduling remains out of MVP scope.
- [x] macOS is covered by a minimal GitHub Actions smoke workflow for release validation.
- [x] Test matrix reflects current MVP decisions.
- [x] Security review reflects redaction, path safety, and restore gating decisions.
- [x] README and changelog match the shipped behavior.

## Release Wording

- highlights-only, action-first, human-gated restore workflow
- simulation exposes failure modes without performing destructive actions
- strict allowlist and isolated temp-dir restore behavior
- discovery intelligence now includes safer Linux heuristics, workspace-scoped installer seeding, and adapter-based OS metadata

## Approval

- [x] Internal review completed.
- [x] Fixture harness passed.
- [ ] No open release blockers remain.
