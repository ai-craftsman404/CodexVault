# CodexVault

CodexVault is a Codex recovery intelligence layer for workspace resilience and restoration.

It is not a generic backup tool. It discovers what matters, ranks uncertain paths for human review, and produces integrity-checked artifacts that support safer restore planning.

## Quickstart

```bash
python plugins/codexvault/codexvault.py backup --workspace-root /path/to/codex-project --dry-run
python plugins/codexvault/codexvault.py backup --workspace-root /path/to/codex-project
```

Use `--dry-run` first. It previews the workflow, prints the review guidance, and creates no artifacts.

## Prerequisites

- Python 3.12 or newer
- A local clone of this repository
- A workspace that contains Codex projects under `plugins/`, or a targeted workspace path
- `git` on PATH if you want discovery metadata to include repository information

Optional:
- `node` if you want version metadata to be reported during discovery
- `python -m unittest` or `pytest` for local verification

## Install

From a fresh clone:

```bash
git clone https://github.com/ai-craftsman404/CodexVault.git
cd CodexVault
```

The plugin lives at:

```text
plugins/codexvault/
```

Its manifest lives at:

```text
plugins/codexvault/.codex-plugin/plugin.json
```

## Run

Dry run:

```bash
python plugins/codexvault/codexvault.py backup --workspace-root /path/to/codex-project --dry-run
```

Real backup:

```bash
python plugins/codexvault/codexvault.py backup --workspace-root /path/to/codex-project
```

Target a single project instead of scanning all projects:

```bash
python plugins/codexvault/codexvault.py backup --workspace /path/to/codex-project/plugins/my-plugin
```

Run the test suite:

```bash
python -m unittest discover -s plugins/codexvault/tests -p "test_*.py"
```

## Supported OS Matrix

| OS | Status | Notes |
| --- | --- | --- |
| Windows | Supported | Primary discovery target for desktop and CLI surfaces |
| Linux | Supported | Includes WSL and container-oriented discovery heuristics |
| macOS | Smoke-tested | Covered in CI and release posture, but not the primary local target |

## What Gets Backed Up

CodexVault focuses on workspace and Codex-adjacent state, including:

- plugin and skill files
- manifests and other JSON control files
- workspace-level recovery metadata
- integrity information for snapshot artifacts
- review-band evidence for uncertain paths

## What Gets Excluded

By default CodexVault excludes:

- `.git`
- `node_modules`
- `__pycache__`
- `.codexvault`
- `.DS_Store`

It also avoids surfacing sensitive path families such as:

- SSH material
- GPG material
- generic credential stores
- obvious secret or keyring locations

## Common Workflow

1. Run a dry run to see what CodexVault would touch.
2. Review the JSON guidance for any review-band candidates.
3. Run the real backup after the preview looks correct.
4. Use restore planning and validation before any destructive action.
5. Treat simulation output as a rehearsal, not as a guarantee of recovery.

## CLI Commands

- `discover`
- `manifest`
- `snapshot`
- `plan`
- `verify`
- `simulate`
- `backup`

## Troubleshooting

- If discovery reports no project, confirm you are pointing at the repository root or a plugin workspace under `plugins/`.
- If `git` metadata is missing, make sure the workspace is inside a real git checkout and `git` is installed.
- If `backup --dry-run` shows no artifacts, that is expected. Dry-run never writes snapshot output.
- If a path appears in the review band, confirm or reject it in the JSON guidance rather than assuming it should be promoted.
- If restore planning warns about compatibility, treat that as a review signal, not as a green light.

## Security & Privacy

CodexVault redacts secrets by default and avoids exposing sensitive content in dry-run preview output. Destructive restore actions remain human-gated.

## Repository Layout

```text
plugins/codexvault/
  .codex-plugin/plugin.json
  README.md
  LICENSE
  scripts/
  skills/
  tests/
.github/workflows/
  CodexVault CI
research/codexvault/
  design, test, security, and local-mapping notes
```

## Version Notes

CodexVault is currently on the `v1b` discovery-intelligence posture. The runtime remains Python-only, while discovery metadata, review-band handling, and mapping evidence are more structured than the original baseline.

## Related Docs

- [Plugin README](plugins/codexvault/README.md)
- [Design spec](research/codexvault/plugin-design-spec.md)
- [Test matrix](research/codexvault/test-matrix.md)
- [Security review](research/codexvault/security-review.md)
- [Release checklist](research/codexvault/release-checklist.md)
