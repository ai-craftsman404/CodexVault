# CodexVault

CodexVault is a Codex-native workspace resilience and restoration plugin focused on deterministic discovery, integrity-checked snapshots, guided restore planning, and harness-first validation.

It is designed to help AI-assisted development environments recover safely without pretending to be a full machine backup tool.

## What it does

- discovers workspace and environment state
- generates normalized manifests
- creates integrity-checked snapshot artifacts
- produces restore plans and validation reports
- simulates restore workflows with Codex agent-team orchestration

## MVP rules

- secrets are redacted by default
- destructive restore actions require human approval
- temp-dir partial restore is isolated and plugin-managed
- scheduling is out of MVP
- validation is tiered and does not overstate restore success
- agent-team simulation is part of the product value proposition

## Repository layout

```text
plugins/codexvault/
  .codex-plugin/plugin.json
  README.md
  LICENSE
  scripts/
  skills/
  tests/
.github/workflows/
  CI for Windows, Linux, and macOS
```

## Release posture

CodexVault v1a is scoped to Windows and Linux MVP validation first, with macOS coverage introduced through GitHub Actions smoke testing.

## Quick start

1. Install the CodexVault plugin from `plugins/codexvault/`.
2. Preview the full workflow with:

   ```bash
   python plugins/codexvault/codexvault.py backup --workspace-root /path/to/codex-project --dry-run
   ```

3. Run the real backup when you are satisfied with the preview.
4. Create a snapshot archive and checksum sidecar.
5. Plan or simulate a restore before any destructive action.

## Dry-run mode

Dry-run is the first-stop user experience for CodexVault:

- previews the full backup workflow
- prints a structured step trace
- creates no artifacts
- helps new users understand what will happen before a real run

## Output style

CodexVault keeps user-facing output compact:

- one-line headline
- short status
- one blocker or risk
- one required action, if needed
