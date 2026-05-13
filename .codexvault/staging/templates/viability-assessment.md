# Viability Assessment

## Plugin

- Working name: PreMortemX
- Date: 2026-05-04
- Assessor: Codex

## Scoring

Score each area from 1 to 5.

| Area | Score | Notes |
| --- | ---: | --- |
| Usefulness | 5 | Clear need for stronger pre-release risk review with readable outputs and human override. |
| Uniqueness | 4 | Pre-mortem reasoning exists, but the harness plus auditability angle creates stronger differentiation. |
| Technical feasibility | 4 | V1 is feasible as skill plus scripts with local records and no mandatory external dependencies. |
| Low maintenance burden | 3 | Ongoing burden exists around scoring calibration, artifact quality, and privacy/security behavior. |
| Low security/privacy risk | 3 | Risk is manageable with conservative defaults, local-first scope, adaptive approvals, and privacy-first retention. |
| GitHub visibility value | 4 | Strong positioning potential because it speaks to AI-agent reliability, release confidence, and auditable workflows. |

## Decision

- Total score: 23 / 30
- Decision: proceed
- Reason:
  - The concept is useful, differentiated enough, and implementable as a disciplined v1 without requiring heavy infrastructure.

## Complexity and Model Recommendation

- Estimated complexity: high
- Recommended model tier for design: strong
- Recommended model tier for build: mid-tier for bounded implementation, strong for harness/security-critical components
- Recommended model tier for final review: strong

## Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| V1 becomes over-scoped and diluted across too many modes | Medium | High | Keep v1 release-first and defer full architecture-validation mode. |
| Risk scoring appears opaque or overconfident | Medium | High | Use rule-first decisioning and score-second explanation model with readable outputs. |
| Sensitive evidence is retained too broadly | Medium | High | Use privacy-first retention, optional encryption, and conservative local scope. |
| Harness concept becomes too heavy for the initial release | Medium | Medium | Keep v1 skill plus scripts, not harness-first or full multi-capability packaging. |

## MVP Recommendation

- Smallest useful version:
  - Release-first pre-mortem plugin that inspects a design-to-release bundle, validates claims against docs/code/test evidence, and returns readable Pass/Warn/Block output with structured override support.
- Required capabilities:
  - Hybrid intake routing
  - Release-first analysis
  - Tiered artifacts
  - Rule-first recommendation model
  - Structured override flow
  - Registry-linked bundle storage
  - Adaptive approvals
- Deferred capabilities:
  - Shipped architecture-validation mode
  - Optional AgentFS backend
  - Advanced managed-key support
  - More autonomous harness optimization

## Versioned Outlook

- V1 outlook:
  - Strongest chance of success comes from a disciplined release-first workflow with local-first records and readable outputs.
- V2 outlook:
  - Viability improves further if architecture validation and stronger harness memory are added without compromising simplicity.
- V3 outlook:
  - Long-term upside is highest if PreMortemX becomes a broader decision harness while preserving evidence discipline and human governance.

## Validation Notes

- Release readiness should include adversarial evaluator coverage, not just standard functional tests.
- Each major feature should have explicit acceptance criteria tied to expected decision quality and guardrail behavior.
