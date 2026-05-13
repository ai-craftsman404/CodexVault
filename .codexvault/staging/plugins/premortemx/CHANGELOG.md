# Changelog

## Unreleased

- started `v5a` docs/config-first execution
- added governed asset folders for prompts, overlays, roles, controls, policy packs, and templates
- added the first linked release-risk governed asset set
- added `Run-PreMortemXV5ATests.py` for synthetic `v5a` validation
- started `v5b` docs/config-first execution
- added governed workflow folders for lifecycle, stages, approvals, handoffs, and exceptions
- added the first linked release-risk workflow asset set
- added `Run-PreMortemXV5BTests.py` for synthetic `v5b` validation
- started `v5c` docs/config-first execution
- added runtime governance folders for policies, context, traces, dashboards, and factsheets
- added the first linked release-risk runtime asset set
- added `Run-PreMortemXV5CTests.py` for synthetic `v5c` validation
- started incremental `v5a` runtime wiring from the governed governance asset layer
- made Python run creation resolve governed prompt, overlay, policy-pack, template, role-card, and control-card assets explicitly
- extended the Python runtime suite to validate governed asset resolution in real run records
- started incremental `v5b` runtime wiring from the governed workflow asset layer
- made Python run creation resolve lifecycle, stage, approval, handoff, and exception assets explicitly
- made Python workflow state advance through governed stages during deliberation and mirror approval-playbook linkage in `approvals.json`
- extended the Python runtime suite to validate governed workflow asset resolution and stage-state transitions
- started incremental `v5c` runtime wiring from the governed runtime asset layer
- made Python run creation resolve control-tower, factsheet, boundary, policy-resolver, context-contract, and trace assets explicitly
- made Python runtime state carry active policy profile, runtime mode, approval posture, breach visibility, and operator attention items
- extended the Python runtime suite to validate governed runtime asset resolution and post-deliberation operator-state updates
- refreshed generated markdown artifacts after deliberation so user-facing reports reflect current workflow and runtime state
- added `Run Status`, `Approval Posture`, and `Next Action` guidance to the generated summaries
- added `start-here.md` as a run-folder landing file linking the key artifacts in reading order
- added `Run-PreMortemXOperatorSurfaceTests.py` for dedicated operator-surface validation
- added explicit `Continue Or Resume` guidance and confirmation cues to generated user-facing artifacts
- added runtime-backed confirmation and resume state to the Python run surface
- made the Python runtime expose `proceedAllowed` and explicit proceed blockers for Warn, Block, escalation, and exception-driven cases
- refreshed `approvals.json` to mirror confirmation, resume, and proceed-blocking state
- extended the Python runtime and operator-surface suites to validate the new confirmation and blocker enforcement cues
- expanded the synthetic workflow matrix to cover clean pass, evidence downgrade, policy downgrade, minority override, and unresolved-permission scenarios
- added workflow gate-state tracking with `gateStatus`, `allowedNextStage`, and blocker lineage in the governed run state
- made `approvals.json` mirror workflow gate-state so approval/playbook behavior reflects the enforced next-stage posture
- added runtime boundary/context enforcement for unvalidated assertions, ambient context, prior-case carry-forward, and unlinked advisory input
- surfaced `boundaryStatus`, blocked context classes, carry-forward allowance, and trusted instruction sources in the governed runtime state
- expanded the Python runtime suite with blocked-context synthetic cases and boundary-remediation assertions
- added workflow-contract enforcement for missing assess-entry prerequisites and incomplete assess-to-deliberate handoff state
- surfaced assess-entry and deliberate-handoff status in the governed workflow state and user-facing artifacts
- expanded the Python runtime suite with missing-evidence-bundle and missing-handoff synthetic workflow cases
- added `Run-PreMortemXAdversarialEvaluatorTests.py` as a dedicated adversarial evaluator pass for core runtime/workflow edge cases
- separated adversarial runtime/workflow edge validation from the broader Python runtime regression suite
- added deeper boundary/context policy enforcement for untransformed context and quarantined advisory context
- surfaced allowed evidence classes, transformation status, and carry-forward ledger state in the governed runtime and approval surfaces
- expanded the Python runtime suite with untransformed and quarantined context policy cases
- unified derived workflow/runtime state refresh so run records, summaries, and approvals use the same persisted state path
- advanced top-level run status to `adjudicated` after deliberation instead of leaving the run in `initialized`
- aligned summary next-action guidance to the same blocker-aware current-action logic used by approvals
- split approval artifacts into decision recommendation and approval recommendation, reducing semantic drift
- redacted non-promoted carry-forward ledger values from `approvals.json`
- hardened boundary marker parsing against leading whitespace and casing variation
- expanded the Python runtime suite with mixed workflow/boundary blocker precedence, multi-blocker workflow, remediation-transition, and leakage-redaction cases
- expanded the adversarial evaluator suite with mixed-blocker and quarantined-context scenarios

## 0.4.0 - 2026-05-07

- moved `PreMortemX` to a Python-first cross-platform runtime contract
- kept the existing PowerShell runtime intact as fallback compatibility
- added Python implementations for core run creation, run-record validation, and orchestrator deliberation
- added Python implementations for registry updates, registry summaries/views, quality reviews, trend summaries, guardrail recommendations, and advisory-boundary reporting
- added Python wrappers around the calibration store flow for initialization, import, summary, promotion-state changes, and approval-controlled calibration changes
- aligned the skill, manifest, testing surface, and public docs to the Python-first `v4` runtime contract
- expanded Python end-to-end validation to the same release-critical behavior shape as the established PowerShell suite

## 0.3.0 - 2026-05-06

- added `v3a` multi-agent deliberation core with orchestrator adjudication and deliberation artifacts
- added rubric-backed override logic with evidence-gated default and severity/policy backstop
- extended the run-record schema with `taskCategory`, `calibrationState`, `executionBoundary`, and `deliberation`
- added `v3b` SQLite-backed calibration storage and reviewed-run promotion flow
- added promotion states for `trusted`, `provisional`, and `excluded`
- added `v3c` calibration change request/approval flow and advisory delegation boundary script
- expanded the script suite to validate `v3a` / `v3b` / `v3c` locally
- refreshed plugin docs, security review, and test matrix for the `v3` product shape

## 0.2.0 - 2026-05-04

- shipped architecture-validation as a supported second mode
- added a registry summary script for stronger local run views
- added materialized registry views for latest-by-project and attention queues
- added local guardrail-memory recommendations based on prior runs
- added quality-review update and trend-summary scripts
- added quality-aware registry summaries and dashboards
- updated run initialization so report titles and task type adapt by mode
- updated plugin docs and examples for the two-mode product shape

## 0.1.0 - 2026-05-04

- initial PreMortemX v1 plugin release
- added release-first Codex plugin manifest and main skill
- added run artifact, schema, and evaluation design package
- added script-backed run initialization, registry update, and run-record validation
- added local script test harness
- added release, security, and testing documentation
