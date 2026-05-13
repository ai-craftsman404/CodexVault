# Build Plan

## Plugin

- Plugin: CodexVault
- Version line: v1a
- Date: 2026-05-13

## Goal

Build the MVP core for workspace resilience with harness-first QA and human-gated restore safety.

## Build Scope

### Core scripts

1. `discover_workspace`
   - Detect OS, shell, Codex paths, package managers, Git state, runtime versions, and MCP topology.
   - Output a normalized discovery record.
   - v1a targets Windows and Linux first; macOS is post-MVP.

2. `write_manifest`
   - Convert discovery data into a versioned manifest.
   - Keep the manifest core small and cross-platform.

3. `create_snapshot`
   - Package snapshot artifacts with checksum metadata.
   - Keep secrets redacted by default.

4. `plan_restore`
   - Generate restore ordering, checkpoints, and approval notes.
   - Support dry-run only by default.
   - Keep temp-dir isolated restore scope only.

5. `verify_restore`
   - Validate runtime readiness, dependency state, and restore-readiness.
   - Output tiered validation labels.

6. `simulate_restore_team`
   - Run bounded agent-team restore simulation.
   - Capture disagreements, risk signals, and adjudicated recommendations.
   - Record a shared JSON adjudication envelope.

## Build Rules

- Prefer the cheapest model tier that can reliably complete the task.
- Use subagents for isolated, non-overlapping work whenever useful.
- Keep all destructive operations behind human approval gates.
- Keep temp-dir partial restore isolated and non-destructive.
- Do not implement encrypted retention in v1a.
- Do not implement scheduling in v1a.
- Keep outputs highlights-only in the normal user path.

## File Ownership

- Core scripts: to be created under `plugins/codexvault/scripts/`
- Test fixtures: to be created under `plugins/codexvault/tests/` or `plugins/codexvault/scripts/tests/`
- Documentation updates: `plugins/codexvault/README.md` and `research/codexvault/*`

## Immediate Next Steps

1. Scaffold script directory and core script stubs.
2. Add fixtures for Windows and Linux discovery profiles.
3. Draft the first test cases for manifest and validation outputs.
4. Add a temp-dir restore simulation fixture set.
