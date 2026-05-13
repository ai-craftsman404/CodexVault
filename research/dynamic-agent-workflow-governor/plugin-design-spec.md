# Plugin Design Spec

## Identity

- Plugin package name: orchex
- Display name: Orchex
- Version: 0.1.0
- Description: A Codex-first plugin for deterministic workflow governance across planning, implementation, testing, and review.
- Developer name: TBD
- Repository: TBD
- License: MIT
- Keywords: codex, workflow, governance, tdd, multi-agent, testing, orchestration
- Category: engineering workflow

## Classification

- Type: skill plus scripts
- Reason for this type: V1 needs machine-checkable artifact and transition enforcement, but does not yet justify the weight of an MCP-backed coordinator.

## Complexity and Model Selection

- Overall complexity: high
- Recommended main-thread model tier: strong for architecture review and integration decisions; mid-tier is sufficient for bounded drafting and mechanical implementation tasks
- Recommended agent model tiers: lightweight for checklist maintenance, mid-tier for bounded code and tests, strong for security/privacy review and adversarial evaluation design
- Escalation triggers:
  - Runtime coordination logic becomes stateful beyond file-based enforcement
  - Security/privacy concerns emerge from script execution or file access
  - Multi-agent behavior requires unresolved architecture tradeoffs

## V1 Product Contract

- Deterministic contract:
  - Fixed stage order: `plan -> build -> test -> review`
  - No silent step skipping
  - Only the orchestrator can advance stages
- Adaptive execution:
  - Stack-specific commands come from adapter profiles
  - Agents may change implementation approach within stage boundaries
  - Replans are allowed only through a governed replan path
- Governance:
  - Every complex task is decomposed into bounded subtasks where possible
  - Every stage writes a required artifact
  - Every stage change is recorded in a task ledger
  - Validation gates block completion when checks fail
- Testing discipline:
  - TDD is the default implementation workflow
  - Adversarial evaluation is part of the official test matrix
  - Agent teams are used only for bounded, non-overlapping tasks

## User Workflows

| Workflow | User Prompt | Expected Codex Behavior | Success Criteria |
| --- | --- | --- | --- |
| Governed feature delivery | `$orchex Build this feature with strict workflow governance.` | Detect stack profile, create a plan, decompose tasks, implement via TDD, run validation, produce review artifact, and summarize gate outcomes. | All required artifacts exist, tests pass, review artifact is produced, and no stage is skipped. |
| Governed bug fix | `$orchex Fix this bug and do not bypass tests or review.` | Produce a bug-fix plan, create or update failing tests first, implement the fix, validate, and record decisions. | Failing test precedes implementation, tests pass after fix, and decision log explains any replan. |
| Governed multi-agent run | `$orchex Use agent roles with strict ownership for this task.` | Assign bounded roles, keep orchestrator control local, track task ownership, and prevent overlapping edits. | Role ownership is explicit, outputs are staged correctly, and integration decisions remain with orchestrator flow. |

## Plugin Structure

```text
plugins/orchex/
  .codex-plugin/plugin.json
  skills/
  scripts/
  assets/
```

## Manifest Plan

- `name`: `orchex`
- `version`: `0.1.0`
- `description`: `Deterministic workflow governance for Codex tasks with artifacts, gates, and stack-aware execution.`
- `skills`: orchestrator, planner, coder, tester, reviewer
- `mcpServers`: none in v1
- `apps`: none in v1
- `interface.displayName`: `Orchex`
- `interface.shortDescription`: `Govern Codex work with deterministic stages and validation gates.`
- `interface.longDescription`: `Standardize agent execution with a fixed workflow contract, required artifacts, TDD-first implementation, and comprehensive validation.`
- `interface.capabilities`: workflow governance, task tracking, validation gating, stack-aware profiles, multi-agent role discipline
- `interface.defaultPrompt`: `Use the governed workflow. Plan first, decompose the work, enforce artifacts and gates, use TDD, then review.`
- `interface.logo`: TBD
- `interface.composerIcon`: TBD
- `interface.screenshots`: TBD

## Skills

| Skill | Trigger Description | Scope | Scripts | References |
| --- | --- | --- | --- | --- |
| orchestrator | Use when the user asks for governed execution, deterministic stages, or disciplined multi-agent work | Own workflow state, task ledger, stage transitions, approvals, and summaries | `validate-stage.ps1`, `summarize-run.ps1` | workflow contract, stack profile docs |
| planner | Use during the planning stage only | Create verifiable step plans and bounded task decomposition | `validate-artifacts.ps1` | planning artifact template |
| coder | Use during the build stage only | Implement approved plan steps under TDD discipline | `resolve-stack-profile.ps1` | task ledger, approved plan |
| tester | Use during the test stage only | Run validation commands, capture failures, and block progression on failed gates | `validate-stage.ps1` | stack profile, test artifact template |
| reviewer | Use during the review stage only | Assess completeness, quality, and policy compliance | `validate-artifacts.ps1` | review checklist |

## Scripts

| Script | Purpose | Inputs | Outputs | Validation |
| --- | --- | --- | --- | --- |
| `resolve-stack-profile.ps1` | Detect or load repo-specific command profile | Repo path, optional profile config | Stack profile object/file | Returns supported commands or explicit unsupported status |
| `validate-artifacts.ps1` | Verify required stage artifacts exist and are non-empty | Run directory, expected stage | Pass/fail result | Fails when required files are missing |
| `validate-stage.ps1` | Enforce transition eligibility and gate results | Run directory, current stage, target stage | Pass/fail result and reason | Fails on invalid transition, failed tests, or missing approvals |
| `summarize-run.ps1` | Produce final run summary from ledger and artifacts | Run directory | Summary artifact | Confirms all expected stages are accounted for |

## Workflow Artifacts

- Required artifacts for V1:
  - `plan.md`
  - `task-ledger.md`
  - `build-log.md`
  - `test-report.md`
  - `review.md`
  - `run-summary.md`
- Optional artifacts:
  - `replan-request.md`
  - `approval-note.md`
  - `adversarial-eval-report.md`

## V1 Acceptance Criteria

- A governed run cannot advance from `plan` to `build` without a valid plan artifact.
- A governed run cannot advance from `build` to `test` without updated task ledger and build log artifacts.
- A governed run cannot complete the `test` stage if configured validation commands fail.
- A governed run cannot complete the `review` stage without a review artifact and final summary.
- Complex tasks are decomposed into bounded subtasks in the plan artifact unless explicitly documented as already atomic.
- Replans require a written reason, preserved artifact history, and orchestrator approval.
- Multi-agent runs record role ownership and avoid overlapping file responsibilities.
- TDD guidance is present in the build workflow and reflected in at least one acceptance test scenario.
- Adversarial evaluation scenarios are included in the test matrix before release readiness.

## Test Strategy

- Unit-level script tests:
  - artifact presence checks
  - invalid transition checks
  - summary generation checks
- Workflow behavior tests:
  - happy path
  - failed test gate
  - missing artifact gate
  - controlled replan
  - resume/retry behavior
- Adversarial evaluation tests:
  - attempt to skip a stage
  - attempt to mark tests passed without evidence
  - attempt to replan without justification
  - overlapping multi-agent ownership attempt
  - wrong-trigger prompt

## MCP and Apps

- MCP servers: none in v1
- App connectors: none in v1
- Authentication: none in v1
- Permissions: local file access and local command execution only

## Definition of Done

- [ ] Plugin installs locally.
- [ ] Manifest paths are valid and relative to plugin root.
- [ ] Skills trigger correctly.
- [ ] Example prompts work.
- [ ] Scripts are tested where applicable.
- [ ] Security and privacy review is complete.
- [ ] Public README is complete.
- [ ] Changelog and license are present.
- [ ] Workflow artifacts and gate behavior are documented.
- [ ] Adversarial evaluation coverage is included in the test matrix.

## Agent Team Plan

- Agent team needed: yes
- Reason: Build, testing, adversarial evaluation, and security review can be split into bounded non-overlapping workstreams once implementation starts.
- Planned roles:
  - Build worker for skills
  - Build worker for scripts
  - Test runner for TDD and matrix execution
  - Adversarial evaluator
  - Security/privacy reviewer
- Non-overlapping file ownership:
  - Skills under `plugins/orchex/skills/`
  - Scripts under `plugins/orchex/scripts/`
  - Tests under plugin test directories
  - Release and review docs under plugin docs paths
