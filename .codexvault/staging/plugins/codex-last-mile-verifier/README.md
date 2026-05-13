# Codex Last-Mile Verifier

Codex Last-Mile Verifier is a reusable Codex plugin for the final live validation step that local file checks cannot prove. It standardizes whether a Codex plugin or skill is actually discoverable, installable, and invokable in the real Codex runtime.

## What it does

- creates a structured verification run for a target plugin or skill
- records preflight checks for local path and expected entrypoint
- guides the live runtime checklist across discovery, install, and smoke-test steps
- stores notes, evidence references, issues, and recommended fixes
- produces a reusable pass/fail or blocked summary

## V1 scope

V1 is a guided workflow, not a fake runtime. It does not publish plugins, emulate Codex, or claim success without an observed live check.

The default live checklist covers:

1. target appears in the Codex discovery surface
2. display name is correct
3. description is correct
4. install action is available
5. installation completes
6. post-install invocation is available
7. smoke-test invocation behaves as expected

## Plugin layout

```text
plugins/codex-last-mile-verifier/
  .codex-plugin/plugin.json
  skills/codex-last-mile-verifier/SKILL.md
  scripts/
  registry/runs/index.jsonl
  runs/
  design/
```

## Core workflow

1. Create a run.
2. Validate the generated run record.
3. Perform or guide the live Codex checks.
4. Update each step with pass, fail, blocked, or not-run.
5. Add evidence notes or screenshots under the run attachments folder.
6. Update the registry and return the final summary.

## Example commands

Create a run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\plugins\codex-last-mile-verifier\scripts\New-CodexLastMileRun.ps1 `
  -TargetName "Sample Plugin" `
  -TargetType plugin `
  -LocalPath ".\plugins\sample-plugin" `
  -ExpectedEntrypoint ".codex-plugin\plugin.json" `
  -ExpectedInvocationMethod "Install from Plugins, then use the bundled skill or app surface" `
  -ExpectedDisplayName "Sample Plugin" `
  -ExpectedShortDescription "One-line runtime description shown in Codex."
```

Mark a step result:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\plugins\codex-last-mile-verifier\scripts\Set-CodexLastMileStepStatus.ps1 `
  -RunRecordPath "<run-record-path>" `
  -StepId discovery-surface `
  -Status pass `
  -Note "Plugin appeared in the library." `
  -EvidenceItem "Screenshot: discovery-surface.png"
```

Validate and register:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\plugins\codex-last-mile-verifier\scripts\Test-CodexLastMileRunRecord.ps1 -RunRecordPath "<run-record-path>"
powershell -NoProfile -ExecutionPolicy Bypass -File .\plugins\codex-last-mile-verifier\scripts\Update-CodexLastMileRegistry.ps1 -RunRecordPath "<run-record-path>"
```

Run script tests:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\plugins\codex-last-mile-verifier\scripts\tests\Run-CodexLastMileVerifierScriptTests.ps1
```

## Run artifacts

Each run creates a dated bundle under `runs/YYYY/MM/<run-id>/`:

- `checklist.md`
- `final-summary.md`
- `evidence-log.md`
- `issues-found.md`
- `run-record.json`
- `attachments/`

## Limits and assumptions

- Real Codex verification still requires runtime access and appropriate workspace controls.
- If live UI tooling is unavailable, the plugin should return a blocked or partial report rather than a false pass.
- Screenshots are optional in v1, but the report should still capture observed evidence as notes.
