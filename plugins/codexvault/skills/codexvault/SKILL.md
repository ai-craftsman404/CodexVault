---
name: "codexvault"
description: "Use when the user wants CodexVault to discover workspace state, generate manifests, create integrity-checked snapshots, simulate restore workflows with agent-team orchestration, or validate recovery readiness."
---

# CodexVault

CodexVault is the Codex workspace resilience skill. It should be used to inspect, snapshot, validate, and rehearse restore workflows for AI-assisted development environments.

## Core contract

- Discover workspace state before acting.
- Redact secrets by default.
- Prefer harness-first simulation and validation.
- Use Codex agent-team orchestration for discovery, restore rehearsal, validation cross-checks, and failure analysis where it materially improves confidence.
- Keep destructive restore actions human-gated.
- Use dry-run or temp-dir isolated restore tests before any in-place restore.

## Required behavior

- Produce normalized workspace manifests.
- Record integrity metadata and provenance.
- Generate restore plans with checkpoints and failure handling.
- Explain validation status as `validated`, `validated-with-warnings`, or `not-validated`.
- Use stable CVX error codes for failures.

## Backup artifact contract

- Artifact name pattern: `codexvault-<workspaceId>-<timestamp>-<platform>`
- Manifest: JSON with normalized discovery and restore metadata
- Snapshot archive: OS-native archive with explicit allowlist and secret redaction
- Checksum algorithm: SHA-256
- Checksum sidecar: plain JSON with archive path and digest
- Provenance: minimal non-secret provenance only
- Temp-dir restore: plugin-managed isolated temp-dir only, no subpath preview in v1a
- Default output: highlights-only summary with one action, one status, one blocker, if any

## Path contract

- Backup destination: `.codexvault/snapshots/`
- Staging directory: `.codexvault/staging/`
- Manifest output: `.codexvault/manifests/`
- Restore plans: `.codexvault/restores/`
- Verification reports: `.codexvault/verification/`
- Simulation outputs: `.codexvault/simulations/`
- Fixture root: `plugins/codexvault/tests/fixtures/`
- Include root: workspace root filtered by explicit allowlist

## Safety rules

- Do not capture secrets by default.
- Do not perform in-place destructive restore without explicit approval.
- Do not treat agent simulation as a substitute for real validation evidence.
- Do not promise full host recovery or universal determinism.

## Suggested workflow

1. Discover workspace and environment state.
2. Build or update the manifest.
3. Create or verify the snapshot archive.
4. Simulate restore using agent-team roles.
5. Run isolated temp-dir restore tests when appropriate.
6. Validate results and report confidence.

## Output style

Keep operation output highlights-only and action-first.

### Backup example

- Headline: `Backup complete`
- Status: `3.4 GB captured, integrity verified`
- Key detail: `Snapshot stored at .codexvault/snapshots/2026-05-13T...`
- Action: `None`

### Restore example

- Headline: `Restore ready for approval`
- Status: `Dry-run passed, 2 dependencies need confirmation`
- Key detail: `Restoring into isolated temp dir first`
- Action: `Approve temp-dir restore`

### Validation example

- Headline: `Validation: validated-with-warnings`
- Status: `Runtime mismatch detected for Python 3.12`
- Key detail: `Package manager and manifest checks passed`
- Action: `Install matching runtime or proceed with warnings`

### Error example

- Headline: `CVX-3002 snapshot integrity failed`
- Status: `Checksum mismatch on 1 archive segment`
- Key detail: `Archive should be re-created before restore`
- Action: `Re-run snapshot creation`
