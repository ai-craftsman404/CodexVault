# Agent Team Plan

## Plugin

- Plugin name:
- Date:
- Main thread owner:
- Reason for using agent team:
- Execution mode: local sub-agent / cloud agent / mixed
- Overall complexity:
- Default model tier:

## Workstreams

| Role | Mode | Task | Model Tier | Output Needed | File Ownership | Blocking? |
| --- | --- | --- | --- | --- | --- | --- |
| Research Scout |  |  |  |  | read-only | no |
| Design Reviewer |  |  |  |  | read-only | no |
| Build Worker |  |  |  |  |  |  |
| Test Runner |  |  |  |  | read-only unless fixing assigned test files |  |
| Security Reviewer |  |  |  |  | read-only | no |
| Release Reviewer |  |  |  |  | read-only unless assigned docs | no |

## Delegation Rules

- Main thread owns final architecture and integration.
- Each worker receives one bounded task.
- Workers editing code must have explicit file or folder ownership.
- Agents must not revert or overwrite work from other agents.
- Agents must report changed files and verification performed.
- Review agents should provide findings with severity and file references.
- Model choice should match task complexity; avoid using stronger models for simple mechanical work.
- Cloud agents must receive a clear handoff, including repo path, relevant templates, exact output expected, and file ownership if they edit.
- Main local session must inspect and integrate cloud-agent outputs before release.

## Parallelization Plan

- Immediate main-thread task:
- Parallel agent tasks:
- Cloud-agent tasks:
- Tasks that must wait:
- Integration checkpoint:

## Agent Outputs

| Role | Status | Summary | Follow-up |
| --- | --- | --- | --- |
| Research Scout | pending |  |  |
| Design Reviewer | pending |  |  |
| Build Worker | pending |  |  |
| Test Runner | pending |  |  |
| Security Reviewer | pending |  |  |
| Release Reviewer | pending |  |  |

## Final Integration Checklist

- [ ] Agent outputs reviewed.
- [ ] Conflicting recommendations resolved.
- [ ] Changed files inspected.
- [ ] Tests or checks rerun after integration.
- [ ] Security and release blockers addressed.
