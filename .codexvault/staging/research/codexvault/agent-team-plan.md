# Agent Team Plan

## Plugin

- Plugin name: CodexVault
- Date: 2026-05-13
- Main thread owner: Codex
- Reason for using agent team: Persona-based orchestration and simulated restore rehearsal are core to the MVP workflow and benefit from bounded parallel roles.
- Execution mode: local sub-agent
- Overall complexity: high
- Default model tier: gpt-5.4-mini for bounded research and mechanical tasks; stronger model only for security-sensitive or architecture decisions

## Workstreams

| Role | Mode | Task | Model Tier | Output Needed | File Ownership | Blocking? |
| --- | --- | --- | --- | --- | --- | --- |
| Research Scout | local sub-agent | Refine MVP gaps, restore boundaries, and simulation scope | gpt-5.4-mini | Ranked research notes | read-only | no |
| Design Reviewer | local sub-agent | Check agent personas, restore guarantees, and safety boundaries | gpt-5.4-mini | Design findings | read-only | no |
| Build Worker | local sub-agent | Implement bounded discovery/manifest/simulation scaffolding | gpt-5.4-mini | Draft code or spec changes | Assigned files only | yes |
| Test Runner | local sub-agent | Propose and/or run MVP test coverage by platform and failure mode | gpt-5.4-mini | Test matrix and failures | read-only unless fixing tests | no |
| Security Reviewer | local sub-agent | Review secret handling, restore safety, and destructive-action limits | gpt-5.4-mini | Security findings | read-only | no |
| Release Reviewer | local sub-agent | Review release packaging, docs, and public-facing claims | gpt-5.4-mini | Release readiness findings | read-only unless assigned docs | no |

## Delegation Rules

- Main thread owns final architecture and integration.
- Each worker receives one bounded task.
- Workers editing code must have explicit file or folder ownership.
- Agents must not revert or overwrite work from other agents.
- Agents must report changed files and verification performed.
- Review agents should provide findings with severity and file references.
- Model choice should match task complexity; avoid using stronger models for simple mechanical work.
- Main local session must inspect and integrate agent outputs before release.

## Parallelization Plan

- Immediate main-thread task: freeze CodexVault MVP scope and turn the agreed ideas into build-ready artifacts.
- Parallel agent tasks: research gap refinement, design review, security review, and release packaging review.
- Cloud-agent tasks: none for now.
- Tasks that must wait: implementation of plugin scaffolding until the spec is finalized.
- Integration checkpoint: after all research and review outputs are merged into the design spec and test matrix.

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

