# Test Matrix

## Functional checks

- Manifest loads from `.codex-plugin/plugin.json`.
- Skill path resolves from `skills/`.
- `New-CodexLastMileRun.ps1` creates a valid run bundle.
- `Set-CodexLastMileStepStatus.ps1` updates step status and summary artifacts.
- `Test-CodexLastMileRunRecord.ps1` accepts valid records and rejects invalid ones.
- `Update-CodexLastMileRegistry.ps1` appends registry entries.

## Runtime workflow checks

- Plugin workflow supports both `plugin` and `skill` targets.
- Discovery step can be recorded as `pass`, `fail`, `blocked`, or `not-run`.
- Smoke-test metadata can be captured when the smoke-test step is updated.
- Final report reflects issues and recommended fixes after step updates.

## Negative checks

- Invalid run record path fails validation.
- Invalid step status fails validation.
- Unknown step id fails step update.
- Empty or malformed target name fails run creation.

## Environment checks

- PowerShell scripts run on Windows.
- Relative local paths resolve correctly from the caller working directory.
- Registry initialization works when no prior `index.jsonl` exists.

## Live verification acceptance checks

- Can capture a real discovery result for a prepared sample extension.
- Can capture a real install result for a prepared sample extension.
- Can capture a real post-install invocation result for a prepared sample extension.
- Can produce a concise final report for a completed live run.
