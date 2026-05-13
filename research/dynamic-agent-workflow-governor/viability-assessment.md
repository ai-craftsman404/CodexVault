# Viability Assessment

## Plugin

- Working name: orchex
- Date: 2026-04-30
- Assessor: Codex main thread

## Scoring

Score each area from 1 to 5.

| Area | Score | Notes |
| --- | ---: | --- |
| Usefulness | 5 | Addresses a common failure mode in agent-assisted engineering: inconsistent execution discipline. |
| Uniqueness | 4 | The concept is validated by adjacent systems, but a governance-first Codex plugin is still differentiated from full workflow engines. |
| Technical feasibility | 4 | A `skill + scripts` V1 is feasible; stronger runtime enforcement can be deferred. |
| Low maintenance burden | 3 | Stack profile support and evolving Codex behavior will require ongoing maintenance. |
| Low security/privacy risk | 3 | Local code execution and validation scripts create manageable but real safety considerations. |
| GitHub visibility value | 4 | The category is timely and likely to attract attention if scoped clearly. |

## Decision

- Total score: 23 / 30
- Decision: proceed
- Reason: The problem is real, the V1 is implementable without overbuilding, and the concept has a credible differentiation if kept governance-first.

## Complexity and Model Recommendation

- Estimated complexity: high
- Recommended model tier for design: mid-tier for drafting, strong for architecture checkpoints
- Recommended model tier for build: mid-tier for bounded implementation, strong for integration-heavy workflow logic
- Recommended model tier for final review: strong

## Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| V1 collapses into a prompt pack with weak enforcement | Medium | High | Require script-backed artifact and transition validation from day one. |
| Flexibility across stacks undermines predictability | High | High | Keep determinism at the workflow contract layer and move variability into adapter profiles. |
| Multi-agent mode causes ownership drift | Medium | High | Make the orchestrator the only transition authority and assign non-overlapping role ownership. |
| Testing scope becomes too large for MVP | High | Medium | Prioritize core path, failure path, resume path, and adversarial gate-bypass tests. |
| Plugin positioning overlaps with heavier workflow engines | Medium | Medium | Emphasize lightweight governance, Codex-first usability, and no-MCP V1 simplicity. |

## MVP Recommendation

- Smallest useful version: A Codex-first plugin that enforces `plan -> build -> test -> review`, writes required artifacts, validates transitions with local scripts, and supports stack-specific command profiles.
- Required capabilities:
  - Orchestrator and role skills
  - Artifact and gate validation scripts
  - Task ledger and run summary
  - Controlled replan flow
  - TDD and adversarial evaluation guidance
- Deferred capabilities:
  - MCP runtime coordinator
  - GUI observability
  - Broad provider portability
  - Deep parallel agent swarms
