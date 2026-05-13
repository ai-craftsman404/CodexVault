# Test Matrix

## Plugin

- Plugin name: orchex
- Version: 0.1.0
- Test date: 2026-04-30
- Tester: Codex main thread

## Installation

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Local plugin path is valid | `plugins/orchex/` exists | Exists | pass |
| `.codex-plugin/plugin.json` exists | Manifest file present | Present | pass |
| Manifest JSON parses | JSON valid | Parsed via local inspection; no parse failure encountered | pass |
| Manifest paths start with `./` | Relative paths only | `skills` path uses `./skills/` | pass |
| Repo-local marketplace entry exists | `.agents/plugins/marketplace.json` points to `./plugins/orchex` | Present and JSON-valid | pass |
| Plugin can be installed or discovered locally | Plugin loads in Codex | Prepared on disk, but not yet verified in Codex UI/runtime from this thread | pending |

## Invocation

| Test | Prompt | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- |
| Explicit plugin invocation | `$orchex Build this feature with strict workflow governance.` | Orchestrator skill should be selected | Not runtime-verified yet | pending |
| Explicit skill invocation | `$orchex-planner Create the governed plan.` | Planner skill should be selected | Not runtime-verified yet | pending |
| Implicit skill trigger | `Plan, build, test, and review this task with strict gates.` | Orchex may trigger if governance intent is clear | Not runtime-verified yet | pending |
| Should-not-trigger prompt | `Explain this function.` | Orchex should not force a governed run | Not runtime-verified yet | pending |

## Functional Behavior

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Main workflow gating scripts succeed on valid path | Transition validation passes with required artifacts and passing test evidence | Covered by script tests | pass |
| Synthetic Node E2E flow | Profile resolves and governed run can reach review and summary | Covered by `Run-OrchexE2ETests.ps1` | pass |
| Synthetic Python E2E flow | Profile resolves and governed run can complete with approval and summary | Covered by `Run-OrchexE2ETests.ps1` | pass |
| Synthetic unsupported-stack E2E flow | Detection fails closed without skipping gates | Covered by `Run-OrchexE2ETests.ps1` | pass |
| Realistic Node mini-repo flow | Profile resolves and governed run can reach review with explicit ownership | Covered by `Run-OrchexE2ETests.ps1` | pass |
| Realistic Python mini-repo flow | Profile resolves and governed run can complete with approval | Covered by `Run-OrchexE2ETests.ps1` | pass |
| Prompt-injection fixture path | Repo instructions that say to skip gates still fail without evidence | Covered by `Run-OrchexE2ETests.ps1` | pass |
| Edge case handled | Placeholder artifacts are rejected | Covered by script tests | pass |
| Run metadata required | Missing run metadata blocks validation | Covered by script tests | pass |
| Invalid input handled | Invalid transitions fail | Covered by script tests | pass |
| Script failure is understandable | Missing evidence and missing approval produce readable failures | Covered by script tests | pass |
| Output matches documented format | `run-summary.md` generated from artifacts | Covered by script tests | pass |

## Adversarial Evaluation

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Attempted stage skipping | Blocked | Covered by invalid transition test | pass |
| Fake test pass without evidence | Blocked | Covered by review-transition evidence test | pass |
| Missing approval at completion | Blocked when required | Covered by script tests | pass |
| Placeholder artifact bypass | Blocked | Covered by script tests | pass |
| Unsupported stack fallback | Fail closed with unsupported profile | Covered by script tests | pass |
| Stale artifact reuse | Blocked | Run ID mismatch covered by script tests | pass |
| E2E run ID tamper | Blocked | Covered by `Run-OrchexE2ETests.ps1` | pass |
| Ledger forgery | Blocked | Partial coverage via required run ID and current-stage mismatch validation | pass |
| Multi-agent ownership overlap | Conflict detected | Covered by script and E2E tests | pass |
| Prompt-injection bypass from repo files | Gates still enforced | Covered by prompt-injection fixture, but not yet verified in live Codex runtime behavior | pass |
| Wrong-trigger prompt | Orchex not selected | Not yet runtime-verified | pending |

## Environment

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Works without network when expected | Local scripts do not require network | No network dependency in current scripts | pass |
| Handles missing credentials | No plugin-owned credentials required | No credentials required | pass |
| Windows path behavior checked | Scripts run on PowerShell/Windows paths | Verified locally on Windows paths | pass |
| No private files required for public example | Public example uses local artifacts only | Current examples do not require private files | pass |

## Result

- Release candidate: no
- Blocking issues:
  - Codex runtime install/discovery not yet verified in the actual Codex UI/runtime
  - Invocation and wrong-trigger behavior not yet verified in a live Codex environment
  - `codex exec` probing from this thread did not yield usable runtime plugin-discovery feedback, so live verification still requires the Codex UI/runtime path
  - Several adversarial checks remain documented but not machine-enforced
- Follow-up:
  - Use the repo-local marketplace entry to test Orchex discovery in Codex
  - Verify plugin loading and skill triggering in Codex
  - Expand adversarial evaluation coverage
