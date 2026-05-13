# PreMortemX Status

## Current Status

- Current phase: `v5 docs-config slices complete; initial runtime wiring, user-surface refinement, workflow-gate enforcement, stage/handoff workflow enforcement, deeper boundary/context policy enforcement, and high-assurance synthetic validation locally hardened`
- Latest local verification:
  - `PreMortemX script tests passed: 22`
  - `PreMortemX Python runtime tests passed: 39`
  - `PreMortemX operator-surface tests passed: 4`
  - `PreMortemX v5a tests passed: 10`
  - `PreMortemX v5b tests passed: 11`
  - `PreMortemX v5c tests passed: 12`
  - `PreMortemX adversarial evaluator tests passed: 8`
- Discovery/install verification: completed in live Codex
- Smoke-test verification: completed in live Codex
- Next-version shaping: `v6` risk-journey direction locked at artifact-first planning level

## Discussion Summary

PreMortemX started as a release-first Codex plugin idea focused on evidence-backed pre-mortem reasoning. The design was intentionally narrowed for v1 so the plugin would make disciplined `Pass` / `Warn` / `Block` decisions instead of becoming a vague multi-purpose advisor.

The core differentiator chosen during the discussion was the harness concept rather than pre-mortem prompting alone. That led to local run artifacts, machine-readable records, registry updates, structured overrides, adaptive approvals, and later quality-review/trend features.

After v1 was completed and verified in live Codex, work continued into v2. V2 added architecture-validation mode, stronger registry views, guardrail-memory recommendations, quality-review logging, trend summaries, and quality-aware dashboards.

## Key Decisions

- Plugin name: `PreMortemX`
- Packaging: `Codex plugin` using `skill + scripts`
- v1 primary mode: `release-risk-gating`
- Decision model: `Pass`, `Warn`, `Block`, plus structured human override
- Routing model: `hybrid`
- Evidence policy: docs + code context + test evidence
- Output style: tiered human-facing reports plus machine-readable run records
- Runtime posture: local-first, conservative-by-default
- Permission model: adaptive approvals, always human-governed
- Retention model: privacy-first hybrid
- Harness principle: recommend broader access when repeated need appears, never silently self-loosen
- V2 mode expansion: architecture validation shipped
- V3 direction: structured multi-agent deliberation, not simple agent majority voting
- Calibration principle: user is responsible for supplying a high-quality curated dataset
- V3 top-level task types: `risk analysis` and `calibration`
- V3 agent-pool structure: one approved master pool, categorized by task type, with orchestrator selecting only from the relevant subset per task
- V3 approved role model:
  - `Lens + evidence + policy`
  - shared cross-task roles:
    - `Evidence Auditor`
    - `Decision Policy Reviewer`
  - `risk analysis` specialist roles:
    - `Domain Risk Specialist`
    - `Operational/Release Risk Specialist`
    - `Security/Privacy Risk Specialist`
  - `calibration` specialist roles:
    - `Dataset Quality Reviewer`
    - `Label Consistency Reviewer`
    - `Threshold/Calibration Reviewer`
    - `Drift Reviewer`
  - `Orchestrator` remains the final adjudicator
- V3 agreed strategy:
  - `structured multi-agent deliberation`
  - `lens + evidence + policy` role model
  - `independent pass -> targeted rebuttal -> orchestrator synthesis`
  - local orchestrator with optional delegated specialist review
  - curated/adjudicated calibration datasets
  - raw signals in `JSONL`, curated calibration data in `SQLite`
- V3 calibration approval-control model:
  - `risk-tiered approvals` as the main model
  - `medium-risk` changes can use session-scoped approval
  - `persistent preferences` are optional tuning, not the safety backbone
  - `uncertain classification` escalates one tier
  - `Tier A`: low-risk changes may auto-apply if logged
  - `Tier B`: medium-risk changes require human approval within bounded policy envelopes
  - `Tier C`: high-risk changes remain fully manual and explicitly authorized
- V3 product-positioning principle:
  - `PreMortemX` is not inventing a new risk discipline
  - it applies established risk-assessment practice through specialist AI agents, orchestrated deliberation, central adjudication, evidence-backed recommendations, and maintainable calibration
  - the novelty is the AI operating model, not the underlying risk principles
- V3 orchestrator rubric model:
  - orchestrator decisions should be supported by a rubric, not ad hoc intuition
  - core rubric dimensions:
    - `confidence`
    - `evidence strength`
    - `risk severity`
    - `evidence completeness`
    - `specialist disagreement level`
    - `calibration/policy fit`
    - `decision sensitivity`
  - secondary refinements may include:
    - `source provenance and freshness`
    - `mitigation readiness`
    - `pattern match to calibrated history`
    - `risk concentration vs diffuse weak signals`
    - `contradictory or missing artifact pressure`
  - preferred grading approach:
    - `5-band internal grading`
    - simplified human-facing bands where appropriate
    - final judgment remains rule-based, with rubric scores as structured support rather than a blind formula
- V3 orchestrator override model:
  - `evidence-first override` is the default
  - `policy-bounded override` is the safety backstop
  - expected hard constraints:
    - no silent override
    - rationale must be logged
    - no weakening of evidence requirements for serious outcomes
    - no bypass of approval rules
    - no suppression of unresolved critical uncertainty in high-sensitivity cases
- V3 calibration dataset schema direction:
  - `two-layer schema`
  - simple required user-facing fields plus richer internal calibration labels
- V3 calibration promotion model:
  - `tiered promotion`
  - promotion states should distinguish `trusted`, `provisional`, and `excluded` cases
- V3 calibration database direction:
  - `normalized audit schema`
  - schema should support multiple reviews, labels, promotions, approvals, and scenario growth over time
- V3 dataset-quality guidance direction:
  - combine `principles-based guidance` with `good vs bad dataset` examples
- V3 execution-boundary direction:
  - `local-first core, cloud optional edge`
  - always local:
    - orchestrator
    - evidence handling
    - final decision
    - approvals
    - audit writes
  - optionally delegated:
    - adversarial critique
    - narrow specialist review
    - calibration batch analysis
- V3 override-trigger direction:
  - `evidence-gated override` as the default trigger model
  - `severity-and-policy override` as the backstop trigger model
- V3 dataset-field direction:
  - `extended two-layer schema`
  - user-facing required fields plus richer internal fields for policy, drift, override, availability, and promotion state
- V3 promotion-state direction:
  - `strict state machine`
  - cases should move through clear criteria into `trusted`, `provisional`, or `excluded`
- V3 database direction:
  - `audit-first normalized schema`
  - recommended tables:
    - `cases`
    - `case_artifacts`
    - `case_reviews`
    - `case_labels`
    - `promotion_events`
    - `calibration_change_requests`
    - `calibration_change_approvals`
    - `dataset_versions`
- V3 dataset-guidance direction:
  - `principles + failure examples`
  - guidance should explain both what strong datasets look like and what common dataset mistakes look like
- V3 final execution-boundary preference:
  - `local-only authority, cloud-only advisory`
  - cloud use should remain optional and advisory, never authoritative by default
- V5 architecture direction:
  - `layered governance + task overlays` for system prompts
  - `deterministic stage-gated workflow` for workflow rules
  - `static policy manifest + dynamic runtime resolver` for metadata/configuration
  - `guardrailed context pipeline` for context engineering
  - `versioned base prompt with variables` plus role overlays for prompt templates

## Completed Work

- [x] PRD reviewed and normalized into plugin intake/design artifacts
- [x] v1 design package created
- [x] v1 plugin scaffolded under `plugins/premortemx/`
- [x] plugin manifest created
- [x] main skill created
- [x] run-record schema and artifact layout implemented
- [x] local registry update flow implemented
- [x] local script test harness implemented
- [x] release docs, security review, checklist, and test matrix created
- [x] local Codex discovery metadata wired
- [x] live Codex install/discovery manually verified
- [x] live Codex invocation manually smoke-tested
- [x] release blockers from v1 smoke test fixed
- [x] v2 architecture-validation mode implemented
- [x] v2 registry summary script implemented
- [x] v2 registry materialized views implemented
- [x] v2 guardrail-memory recommendation script implemented
- [x] v2 quality-review update script implemented
- [x] v2 trend-summary script implemented
- [x] v2 quality-aware registry summaries and dashboards implemented
- [x] v3a multi-agent deliberation core implemented
- [x] v3b calibration dataset and promotion system implemented
- [x] v3c calibration approvals and advisory-boundary controls implemented
- [x] all current local tests passing
- [x] v4 Python-first runtime path implemented for core run creation, validation, deliberation, registry, review, and calibration flows
- [x] v4 skill, manifest, docs, and test surface aligned to the Python-first runtime contract
- [x] v4 Python runtime validated end to end locally
- [x] v5 architecture direction researched against official guidance
- [x] v5 architecture plan recorded in the design package
- [x] v5 high-level artifact structure recorded
- [x] v5a governance asset contracts recorded
- [x] v5b workflow asset contracts recorded
- [x] v5c runtime asset contracts recorded
- [x] v5 rollout and implementation plan recorded
- [x] v5a governance asset files created
- [x] v5a synthetic validation implemented and passing
- [x] v5b workflow asset files created
- [x] v5b synthetic validation implemented and passing
- [x] v5c runtime asset files created
- [x] v5c synthetic validation implemented and passing
- [x] v5 docs/config-first slices regression-checked against existing Python and PowerShell runtime suites
- [x] v5a runtime wiring started from the governed governance asset layer
- [x] Python runtime now resolves governed governance assets explicitly during run creation
- [x] v5b runtime wiring started from the governed workflow asset layer
- [x] Python runtime now resolves governed workflow assets explicitly during run creation
- [x] Python workflow state now advances through governed stage state during deliberation
- [x] v5b runtime wiring regression-checked against v5a, v5c, Python, and PowerShell test surfaces
- [x] v5c runtime wiring started from the governed runtime asset layer
- [x] Python runtime now resolves governed runtime assets explicitly during run creation
- [x] Python runtime now carries operator-facing runtime state and updates it after deliberation
- [x] v5c runtime wiring regression-checked against v5a, v5b, Python, and PowerShell test surfaces
- [x] generated markdown summaries now refresh after deliberation to reflect real workflow/runtime state
- [x] generated summaries now surface run status, approval posture, and next action near the top
- [x] run folders now include `start-here.md` as an operator/user landing file
- [x] operator-surface behavior now has its own dedicated validation pass
- [x] generated user-facing artifacts now surface explicit continue/resume guidance and confirmation requirements
- [x] minimal deeper runtime enforcement implemented for confirmation, proceed blocking, and exception-driven resume state
- [x] derived workflow/runtime state now refreshes from a single shared Python state path
- [x] top-level run status now advances to `adjudicated` after deliberation
- [x] approval artifacts now separate decision recommendation from approval recommendation
- [x] approval artifacts now redact non-promoted carry-forward ledger values
- [x] boundary marker handling now tolerates leading whitespace and casing variation
- [x] mixed workflow/boundary blocker precedence cases validated
- [x] missing-scope, missing-risk-picture, and multi-blocker workflow cases validated
- [x] remediation transition from blocked-context to ready validated
- [x] operator/public artifact consistency hardened against summary/runtime drift
- [x] adversarial suite expanded with mixed-blocker and quarantined-context cases
- [x] Python runtime and operator-surface suites now validate proceed blockers and confirmation/resume enforcement cues
- [x] synthetic workflow coverage expanded across clean-pass, evidence downgrade, policy downgrade, minority override, and unresolved-permission scenarios
- [x] workflow state now exposes gate status, allowed next stage, and blocker lineage as active gating state
- [x] runtime boundary/context enforcement implemented for unvalidated assertions, ambient context, prior-case carry-forward, and unlinked advisory input
- [x] synthetic runtime coverage expanded for blocked-context scenarios and boundary remediation flow
- [x] workflow enforcement expanded to assess-entry and assess-to-deliberate handoff contracts
- [x] synthetic workflow coverage expanded for missing-evidence-bundle and missing-handoff scenarios
- [x] dedicated adversarial evaluator suite added for runtime/workflow boundary cases
- [x] adversarial evaluator coverage now has its own runnable local test entrypoint
- [x] deeper boundary/context policy enforcement implemented for untransformed context, quarantined advisory context, allowed evidence class surfacing, transformation status, and carry-forward ledger tracking
- [x] synthetic runtime coverage expanded for untransformed and quarantined context scenarios

## Remaining Tasks

- no critical `v5` task remains
- optional future work:
  - deeper enterprise/operator dashboard work
  - broader evaluator expansion over time
  - future enterprise distribution/publishing path work
  - `v6` risk-journey visual surface

## V3 Scope Direction

- structured multi-agent deliberation for risk assessment and classification
- specialist agents from different risk lenses
- orchestrator synthesis that weighs evidence quality and disagreement
- orchestrator override capability with explicit rationale
- calibration workflows using user-provided curated datasets
- README and calibration docs must educate users on what a good-quality calibration dataset looks like
- two top-level task types only for now:
  - `risk analysis`
  - `calibration`
- one approved master pool of agent roles, categorized by task type
- orchestrator should determine the exact agent roles and number of agents dynamically per task, but only within approved guardrails
- approved master pool should map to real-world risk-assessment functions rather than arbitrary AI personas

### V3 delivery split

- `v3a`: multi-agent deliberation core
  - orchestrator flow
  - approved specialist pool selection
  - rubric-based adjudication
  - override triggers and audit trail
  - human-facing adjudicated output only
- `v3b`: calibration dataset and promotion system
  - two-layer dataset schema
  - normalized SQLite store
  - reviewed-run promotion flow
  - `trusted` / `provisional` / `excluded` state handling
  - dataset-quality guidance and docs
- `v3c`: calibration-driven controls and optional advisory delegation
  - calibration change requests and approvals
  - session/persistent approval handling
  - local-only authority enforcement
  - optional cloud-advisory specialist paths
  - stronger governance and evaluator coverage

### Proposed V3 Approved Agent Pool

Shared cross-task roles:
- `Evidence Auditor`
  - tests whether claims are genuinely supported by the available evidence bundle
- `Decision Policy Reviewer`
  - checks whether the emerging judgment matches declared thresholds, confidence policy, and governance rules
- `Orchestrator`
  - selects from the approved pool, controls deliberation flow, and issues the final adjudicated result

`risk analysis` sub-pool:
- `Domain Risk Specialist`
  - evaluates core design, product, implementation, and assumption failure modes
- `Operational/Release Risk Specialist`
  - evaluates rollout, recoverability, observability, dependency, and operational readiness risks
- `Security/Privacy Risk Specialist`
  - evaluates abuse, data handling, access scope, leakage, and privacy/security concerns

`calibration` sub-pool:
- `Dataset Quality Reviewer`
  - evaluates representativeness, completeness, and structural quality of the calibration dataset
- `Label Consistency Reviewer`
  - checks whether adjudicated outcomes and rationale labels are coherent and reviewable
- `Threshold/Calibration Reviewer`
  - evaluates whether proposed calibration effects are justified within approved safety bounds
- `Drift Reviewer`
  - checks for distribution shift, changing conditions, or unstable behavior patterns across time

## V3 Non-Goals

- simple majority voting as the decision rule
- automatic trust in more agents just because there are more votes
- automatic calibration from low-quality or unreviewed datasets
- unconstrained ad hoc agent selection outside the approved pool/sub-pool structure

## Latest V3 Discussion Snapshot

- We agreed that `structured multi-agent deliberation` is the right v3 direction, not plain majority voting.
- We agreed that `calibration` and `risk analysis` should be the only two top-level task types for now.
- We agreed that the orchestrator should choose agent roles and agent count dynamically per task.
- We also agreed that this dynamic behavior must remain within guardrails.
- The preferred structure is:
  - one approved master pool
  - categorized by task type
  - orchestrator selects only from the relevant subset per task

## Remaining V3 Knowledge Gaps

- none at the product-design level

## V3 Exact Default Configuration

### Orchestrator override thresholds

- internal grading scale: `1-5`
- primary override dimensions:
  - `confidence`
  - `evidenceStrength`
  - `riskSeverity`
  - `evidenceCompleteness`
  - `disagreementLevel`
  - `policyFit`
  - `decisionSensitivity`
- default override triggers:
  - evidence-gated override:
    - trigger when a minority specialist view has `evidenceStrength >= 4` and exceeds the leading consensus evidence grade by at least `2`
    - trigger when consensus `evidenceCompleteness <= 2`
    - trigger when `disagreementLevel >= 4` and `confidence <= 2`
  - severity-and-policy backstop:
    - trigger when `riskSeverity >= 4` and `evidenceStrength >= 4`
    - trigger when `policyFit <= 2`
    - trigger when `decisionSensitivity >= 4` and unresolved uncertainty remains
- mandatory human escalation triggers:
  - proposed approval or permission broadening beyond current safe scope
  - calibration change request in `Tier C`
  - high-sensitivity case with unresolved critical uncertainty
  - override that would weaken evidence requirements for a serious outcome

### Two-layer calibration dataset fields

- required user-facing fields:
  - `caseId`
  - `taskType`
  - `createdAt`
  - `sourceRunId`
  - `artifactRefs`
  - `initialDecision`
  - `adjudicatedDecision`
  - `rationaleSummary`
  - `reviewedOutcome`
  - `reviewer`
  - `reviewDate`
- richer internal fields:
  - `evidenceQuality`
  - `riskSeverity`
  - `uncertaintyLevel`
  - `confidenceExpected`
  - `inputAvailability`
  - `permissionContext`
  - `overrideUsed`
  - `overrideLegitimacy`
  - `policyBand`
  - `driftTag`
  - `falsePositiveFlag`
  - `missedRiskFlag`
  - `promotionState`
  - `datasetVersion`
  - `notes`

### Promotion-state criteria

- `trusted`:
  - adjudicated decision present
  - evidence traceable through `artifactRefs`
  - reviewed by a human with named reviewer and date
  - no unresolved critical ambiguity
  - either outcome-grounded or explicitly expert-adjudicated
- `provisional`:
  - reviewed case exists
  - useful signals present
  - one or more of: incomplete outcome grounding, incomplete traceability, limited confidence in labels, pending follow-up
- `excluded`:
  - materially incomplete artifacts
  - contradictory or unreliable labels
  - unresolved structural ambiguity
  - unsuitable for calibration due to noise or missing provenance

### SQLite schema defaults

- `cases`
  - `case_id` PK
  - `task_type`
  - `created_at`
  - `source_run_id`
  - `initial_decision`
  - `adjudicated_decision`
  - `reviewed_outcome`
  - `promotion_state`
  - `dataset_version`
- `case_artifacts`
  - `artifact_id` PK
  - `case_id` FK
  - `artifact_type`
  - `artifact_ref`
  - `is_available`
  - `provenance_note`
- `case_reviews`
  - `review_id` PK
  - `case_id` FK
  - `reviewer`
  - `review_date`
  - `rationale_summary`
  - `notes`
- `case_labels`
  - `label_id` PK
  - `case_id` FK
  - `evidence_quality`
  - `risk_severity`
  - `uncertainty_level`
  - `confidence_expected`
  - `policy_band`
  - `drift_tag`
  - `false_positive_flag`
  - `missed_risk_flag`
  - `override_used`
  - `override_legitimacy`
  - `permission_context`
  - `input_availability`
- `promotion_events`
  - `promotion_event_id` PK
  - `case_id` FK
  - `from_state`
  - `to_state`
  - `changed_at`
  - `changed_by`
  - `reason`
- `calibration_change_requests`
  - `change_request_id` PK
  - `requested_at`
  - `requested_by`
  - `change_tier`
  - `change_type`
  - `proposed_value`
  - `reason`
  - `status`
- `calibration_change_approvals`
  - `approval_id` PK
  - `change_request_id` FK
  - `approved_at`
  - `approved_by`
  - `approval_scope`
  - `approval_decision`
  - `approval_note`
- `dataset_versions`
  - `dataset_version` PK
  - `created_at`
  - `created_by`
  - `description`

### Dataset-quality guidance default wording

- strong calibration datasets should be:
  - outcome-grounded where possible
  - explicitly adjudicated
  - representative across typical, edge, and adversarial cases
  - traceable to the evidence available at decision time
  - versioned and reviewable over time
- weak calibration datasets commonly fail because of:
  - hindsight leakage
  - easy-case bias
  - weak or inconsistent labels
  - missing evidence context
  - one-sided outcomes that distort thresholds

### Local vs cloud execution boundary

- local-only authority:
  - orchestrator selection and synthesis
  - evidence handling
  - final adjudicated outcome
  - approval handling
  - policy changes
  - audit and registry writes
- optional cloud-only advisory:
  - adversarial critique
  - bounded specialist second opinions
  - calibration batch analysis on approved data slices

## Likely Next Steps

- Optional polish:
  - keep refreshing public examples and screenshots as product surface evolves
- If moving into `v6`:
  - prototype `v6a` for `release-risk-gating` using `HTML + inline SVG`
  - implement the journey-builder against the new artifact contract
  - add the first synthetic `v6a` visual-journey tests

## Next-Version Seed

- `v6` is now shaped as:
  - `artifact-based first`
  - `HTML + inline SVG` per-run rendering
  - derived journey schema over canonical run artifacts
  - compact auto-collapsed default for simple runs
  - `release-risk-gating` as the first supported mode
- primary reference:
  - [design/v6-risk-journey-prd.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v6-risk-journey-prd.md)
- first implementation contract:
  - [design/v6a-journey-artifact-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v6a-journey-artifact-spec.md)

## Files Most Relevant To Current State

- [README.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/README.md)
- [CHANGELOG.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/CHANGELOG.md)
- [TEST-MATRIX.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/TEST-MATRIX.md)
- [SECURITY-REVIEW.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/SECURITY-REVIEW.md)
- [design-package.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/design-package.md)
- [artifact-and-schema-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/artifact-and-schema-spec.md)
- [evaluation-plan.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/evaluation-plan.md)
