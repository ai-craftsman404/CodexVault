# Plugin Design Spec

## Identity

- Plugin package name: codex-last-mile-verifier
- Display name: Codex Last-Mile Verifier
- Version: 0.1.0
- Description: Guided live discovery, installation, and invocation verification for Codex plugins and skills with reusable evidence and pass/fail reporting.
- Developer name: Code Plugin Guru
- Repository: TBD
- License: MIT
- Keywords: codex, verification, plugin, skill, install, discovery, smoke-test
- Category: developer-tools

## Classification

- Type: skill plus scripts
- Reason for this type:
  - The core value is process standardization, which belongs in a skill.
  - Local scripts make the workflow repeatable and artifact-driven without depending on runtime automation.

## Complexity and Model Selection

- Overall complexity: medium
- Recommended main-thread model tier: strong model for design and release review, lighter model for mechanical script and doc work
- Recommended agent model tiers: not required for v1 implementation
- Escalation triggers:
  - UI automation becomes a required dependency
  - external services are added
  - cross-workspace regression analytics move into scope

## User workflows

| Workflow | User Prompt | Expected Codex Behavior | Success Criteria |
| --- | --- | --- | --- |
| Plugin live verification | "Verify whether this local plugin is discoverable and installable in Codex." | Create a run, check preflight paths, guide the user through discovery and install steps, and produce a final report. | The user gets a reusable per-step result bundle with evidence and fixes. |
| Skill live verification | "Run a last-mile check for this Codex skill." | Create a skill-targeted run, verify discovery and invocation behavior, and log smoke-test evidence. | The final report makes skill runtime readiness clear. |
| Regression retest | "Re-run the live verification after my fix." | Create a new run, reuse the same target expectations, and append the result to the registry. | Repeated runs can be compared manually through stored artifacts. |

## Manifest plan

- `name`: codex-last-mile-verifier
- `version`: 0.1.0
- `description`: Guided live discovery, installation, and invocation verification for Codex plugins and skills with reusable evidence and pass/fail reporting.
- `skills`: `./skills/`
- `interface.displayName`: Codex Last-Mile Verifier
- `interface.shortDescription`: Standardize real Codex discovery, install, and smoke-test verification for plugins and skills.
- `interface.capabilities`: interactive workflow, local execution, report generation
- `interface.defaultPrompt`: create a run, guide the live check, and return a standard report

## Scripts

| Script | Purpose | Inputs | Outputs | Validation |
| --- | --- | --- | --- | --- |
| `New-CodexLastMileRun.ps1` | Create a dated run bundle and initialized record | target metadata | run folder and report templates | script test |
| `Set-CodexLastMileStepStatus.ps1` | Update step status, evidence, issues, and summary artifacts | run record, step result | updated run record and markdown summaries | script test |
| `Test-CodexLastMileRunRecord.ps1` | Validate schema and allowed values | run record path | validation result | script test |
| `Update-CodexLastMileRegistry.ps1` | Append run metadata to the index | run record path | registry index entry | script test |

## Definition of done

- [x] plugin manifest created
- [x] skill created
- [x] scripts created
- [x] script tests created
- [x] README, changelog, release checklist, test matrix, and security review created
- [ ] sample live verification runs completed against real target extensions
