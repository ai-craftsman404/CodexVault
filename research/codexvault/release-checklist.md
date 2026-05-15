# CodexVault Release Checklist

## Release Target

- Plugin: CodexVault
- Version: v1a
- Scope: Windows and Linux MVP only

## Pre-Release Checks

- [ ] Manifest schema is valid and versioned.
- [ ] Discovery, manifest, snapshot, restore-plan, verify, and simulation scripts are present.
- [ ] Python CLI is the supported user-facing entrypoint across Windows, Linux, and macOS.
- [ ] Snapshot archives use the approved allowlist and exclude secrets by default.
- [ ] SHA-256 checksum sidecar is emitted and verified.
- [ ] Temp-dir restore simulation stays isolated and removes its temp root on completion or failure.
- [ ] Negative-path fixtures cover malformed JSON, missing fields, path traversal, and checksum failure.
- [ ] v1b config schema and example configs validate against the documented path contract.
- [ ] Self-improvement loop uses tiered fidelity labels, safe deltas only, and bounded adversarial rehearsal.
- [ ] New behavior was added through a TDD loop where applicable.
- [ ] Adversarial evaluator review ran for restore-critical or security-sensitive changes.
- [ ] Human approval remains required for destructive restore actions.
- [ ] Scheduling remains out of MVP scope.
- [ ] macOS remains deferred to post-MVP.
- [ ] Test matrix reflects current MVP decisions.
- [ ] Security review reflects redaction, path safety, and restore gating decisions.
- [ ] README and changelog match the shipped behavior.

## Release Wording

- highlights-only, action-first, human-gated restore workflow
- simulation exposes failure modes without performing destructive actions
- strict allowlist and isolated temp-dir restore behavior

## Approval

- [ ] Internal review completed.
- [ ] Fixture harness passed.
- [ ] No open release blockers remain.
