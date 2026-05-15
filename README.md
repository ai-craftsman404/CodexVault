# CodexVault

CodexVault is a Codex-native workspace resilience and restoration plugin for AI-assisted development environments.

It focuses on:
- deterministic discovery
- integrity-checked snapshots
- guided restore planning
- harness-first validation
- agent-team-driven simulation and quality assurance

It is not a generic machine backup tool.

## One-command experience

The first-stop user experience is dry-run preview:

```bash
python plugins/codexvault/codexvault.py backup --workspace-root /path/to/codex-project --dry-run
```

Dry-run:
- previews the full backup workflow
- prints a structured step trace
- creates no artifacts
- helps new users understand what will happen before a real run
- gives agent-team a safe simulation surface

The real backup command uses the same CLI:

```bash
python plugins/codexvault/codexvault.py backup --workspace-root /path/to/codex-project
```

## What it does

- discovers workspace and environment state
- generates normalized manifests
- creates integrity-checked snapshot artifacts
- produces restore plans and validation reports
- simulates restore workflows with Codex agent-team orchestration

## User flow

1. Run `backup --dry-run` to preview the workflow.
2. Run `backup` to create real artifacts.
3. Review restore planning and validation output.
4. Use `simulate` to rehearse restore workflows safely.
5. Approve any destructive restore action only after review.

## CLI commands

- `discover`
- `manifest`
- `snapshot`
- `plan`
- `verify`
- `simulate`
- `backup`

## Backup modes

- `backup --workspace-root` backs up every eligible plugin project under `plugins/`
- `backup --workspace` backs up one targeted project when you need a narrower run

## MVP rules

- secrets are redacted by default
- destructive restore actions require human approval
- temp-dir partial restore is isolated and plugin-managed
- scheduling is out of MVP
- validation is tiered and does not overstate restore success
- agent-team simulation is part of the product value proposition
- the user-facing workflow is Python-based and OS-neutral

## Output style

CodexVault keeps user-facing output compact:
- one-line headline
- short status
- one blocker or risk
- one required action, if needed

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

## Support files

- plugin-specific notes: [plugins/codexvault/README.md](plugins/codexvault/README.md)
- design spec: [research/codexvault/plugin-design-spec.md](research/codexvault/plugin-design-spec.md)
- test matrix: [research/codexvault/test-matrix.md](research/codexvault/test-matrix.md)
- security review: [research/codexvault/security-review.md](research/codexvault/security-review.md)
- release checklist: [research/codexvault/release-checklist.md](research/codexvault/release-checklist.md)
