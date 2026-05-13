# V1 Task Breakdown

## Goal

Deliver Orchex as a Codex-first `skill + scripts` plugin that governs `plan -> build -> test -> review` execution with deterministic transitions, required artifacts, TDD-first guidance, and adversarial evaluation coverage.

## Task Tracking Rules

- Every task must have a single owner.
- Every task must produce a concrete artifact or measurable outcome.
- Complex tasks should be split before implementation starts.
- No task should span multiple unrelated deliverables.
- Testing tasks are first-class tasks, not cleanup work.

## Task List

| ID | Task | Owner | Output | Depends On | Status |
| --- | --- | --- | --- | --- | --- |
| V1-01 | Finalize package naming and public positioning | Main thread | Confirmed plugin identity | None | completed |
| V1-02 | Define workflow artifact schema | Main thread | Artifact contract doc | V1-01 | completed |
| V1-03 | Define task ledger format and status model | Main thread | Ledger schema doc | V1-02 | completed |
| V1-04 | Define stack profile format | Main thread | Stack profile schema doc | V1-02 | completed |
| V1-05 | Draft orchestrator skill | Skills worker | Orchestrator skill file | V1-02, V1-03, V1-04 | completed |
| V1-06 | Draft planner skill | Skills worker | Planner skill file | V1-02 | completed |
| V1-07 | Draft coder skill with TDD rules | Skills worker | Coder skill file | V1-02, V1-03 | completed |
| V1-08 | Draft tester skill | Skills worker | Tester skill file | V1-02, V1-04 | completed |
| V1-09 | Draft reviewer skill | Skills worker | Reviewer skill file | V1-02 | completed |
| V1-10 | Implement stack profile resolver script | Scripts worker | `resolve-stack-profile.ps1` | V1-04 | completed |
| V1-11 | Implement artifact validator script | Scripts worker | `validate-artifacts.ps1` | V1-02 | completed |
| V1-12 | Implement stage transition validator script | Scripts worker | `validate-stage.ps1` | V1-02, V1-03 | completed |
| V1-13 | Implement run summary generator script | Scripts worker | `summarize-run.ps1` | V1-02, V1-03 | completed |
| V1-14 | Create manifest and plugin structure | Main thread | Plugin scaffold | V1-05 through V1-13 | completed |
| V1-15 | Write README and example prompts | Docs worker | Public plugin docs | V1-14 | completed |
| V1-16 | Write unit tests for validation scripts | Test worker | Script test suite | V1-10 through V1-13 | completed |
| V1-17 | Write workflow behavior tests | Test worker | Workflow test suite | V1-05 through V1-14 | completed |
| V1-18 | Write adversarial evaluation cases | Eval worker | Adversarial eval suite | V1-05 through V1-14 | in progress |
| V1-19 | Run install and trigger tests | Test worker | Completed test matrix rows | V1-14, V1-15 | in progress |
| V1-20 | Run security and privacy review | Security reviewer | Security review doc | V1-14, V1-17, V1-18 | in progress |
| V1-21 | Run final release-readiness review | Main thread | Release verdict and gap list | V1-15 through V1-20 | open |

## Test Requirements

- TDD expectation:
  - Validation scripts should be developed test-first where feasible.
  - Workflow behavior should be exercised against failing and passing paths.
- Core workflow coverage:
  - Happy path
  - Missing artifact
  - Failed tests
  - Replan request
  - Resume or retry after failure
- Adversarial coverage:
  - Attempted stage skipping
  - Attempted fake pass state
  - Missing approval where required
  - Overlapping multi-agent ownership
  - Wrong-trigger invocation

## Monitoring Fields

Each implementation task should later record:

- start date
- finish date
- owner
- touched files
- tests added
- tests run
- blockers
- gate result

## Current Monitoring Snapshot

- Latest implementation milestone:
  - Plugin scaffold, manifest, skills, scripts, README, and hardened run-integrity checks are in place under `plugins/orchex/`.
- Tests added:
  - `plugins/orchex/scripts/tests/Run-OrchexScriptTests.ps1`
  - `plugins/orchex/scripts/tests/Run-OrchexE2ETests.ps1`
- Tests last run:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\plugins\orchex\scripts\tests\Run-OrchexScriptTests.ps1`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\plugins\orchex\scripts\tests\Run-OrchexE2ETests.ps1`
- Last result:
  - Passed: 14 script tests
  - Passed: 8 E2E tests
- Active blockers:
  - Need live trigger/install validation in Codex UI/runtime.

## Exit Condition

V1 implementation is complete when release-gating tests, adversarial evaluation coverage, security review, and release-readiness review are all complete.
