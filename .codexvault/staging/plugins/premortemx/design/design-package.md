# PreMortemX Design Package

## Purpose

PreMortemX is a Codex plugin for evidence-backed pre-mortem analysis.

V1 is intentionally narrow:
- focus on release risk gating
- use a hybrid routing model
- inspect a design-to-release bundle
- return clear Pass / Warn / Block recommendations
- preserve human override with structured accountability

The long-term goal is broader than v1. PreMortemX should evolve into a trusted, human-governed decision harness for Codex workflows, but the first release must stay disciplined.

## Positioning Principle

PreMortemX should be positioned as an AI operating model for an established discipline, not as a brand-new theory of risk assessment.

The core value proposition is:
- established risk-assessment best practices
- executed through specialist AI lenses
- orchestrated into a single adjudicated outcome
- backed by evidence, auditability, and calibration over time

This distinction matters for adoption. Users should recognize the underlying process as disciplined and familiar, while seeing the speed, consistency, and scalability benefits of the AI specialist-team model.

## Product Shape

- Plugin type: skill plus scripts
- Primary mode: release risk gating
- Secondary mode: architecture validation
- Evidence scope: docs, code context, and test evidence
- Runtime posture: local-first, conservative by default, broader access only through adaptive human-approved escalation

## User-Facing Behavior

### Intake and routing

- PreMortemX first attempts to infer the likely analysis mode from the user request and local context.
- If routing confidence is low, it asks a short targeted Q&A before proceeding.
- V1 should bias toward the release-first path and avoid pretending to support broad multi-mode analysis when the evidence is weak.

### Decision model

- `Pass`: adequate evidence coverage, no warn/block rule triggered, and only low residual risk remains
- `Warn`: meaningful medium risk or uncertainty prevents a confident pass
- `Block`: a credible high-severity risk exists or aggregate risk crosses the block threshold
- `Override`: not a fourth decision state in the core engine; it is a recorded human action that can follow `Block`

### Confidence model

- Internal confidence should be finer-grained.
- Human-facing confidence should be shown as plain-language bands.
- Avoid false precision in the main report.

## Core Components

### Skill layer

Responsibilities:
- run hybrid intake routing
- structure the pre-mortem analysis
- classify risks
- explain recommendations in readable language

### Script layer

Responsibilities:
- compute structured scoring support for rule-first decisions
- write human-facing artifacts
- write machine-readable run records
- update the local registry

### Harness layer

V1 harness behavior should stay lightweight:
- local registry plus per-run artifacts
- adaptive approvals
- remembered boundary patterns and exceptions
- privacy-first retention behavior
- recommendations for broader permissions when repeated need is detected

The harness should recommend boundary expansion, not silently self-loosen guardrails.

## Release-First Workflow

1. Collect the design-to-release bundle.
2. Determine whether release gating is the correct active mode.
3. Identify candidate risks using pre-mortem reasoning.
4. Validate claims against docs, code context, and test evidence.
5. Apply rule-first pass/warn/block logic.
6. Rank and explain risks using supporting score data.
7. Produce tiered artifacts.
8. If blocked and the human chooses to proceed, capture a structured override.
9. Update registry and per-run records.
10. Support later review of false positives, missed risks, and actual outcomes.

## Security and Privacy Model

- Start less permissive.
- Keep evidence local by default.
- Separate human-readable summaries from rawer machine records.
- Detect likely sensitive retained content and recommend stronger protection.
- Keep the final retention/protection choice human-controlled.
- Support optional encryption for sensitive artifacts using a local-user-controlled key source.

AgentFS is a strong architectural reference for isolation and auditing, but it should remain optional and non-required in v1.

## Report Design Rule

Human-facing reports should default to this structure when appropriate:
- title at the top
- detailed bullet points in the core body
- summary of key points at the bottom
- version and/or date stamp when the artifact is meant to be maintained over time

The writing style should stay intuitive, easy to read, and semi-technical where possible.

## Version Roadmap

### V1

- release-first workflow only
- tiered outputs
- local registry plus per-run artifacts
- structured override flow
- adaptive approvals
- privacy-first retention

### V2

- architecture validation mode shipped
- stronger run-record and registry views
- richer guardrail memory and permission recommendation behavior
- possible optional isolation backend improvements

### V3

- structured multi-agent deliberation for risk classification and risk assessment
- specialized agent lenses with orchestrator synthesis instead of naive majority voting
- optional orchestrator override with explicit rationale
- stronger calibration workflows using user-supplied curated datasets
- clearer dataset-quality guidance so calibration quality expectations are explicit
- more mature team/organization governance patterns

#### Recommended delivery split

`v3` should not ship as one lump. It should be delivered in three coherent slices:

- `v3a`: multi-agent deliberation core
  - orchestrator-led specialist selection
  - rubric-based adjudication
  - override triggers and audit recording
  - adjudicated output contract
- `v3b`: calibration dataset and promotion system
  - two-layer schema
  - normalized SQLite store
  - promotion-state workflow
  - dataset-quality guidance
- `v3c`: calibration-driven controls and optional advisory delegation
  - change-request and approval system
  - session/persistent approval behavior
  - local-only authority with cloud-only advisory paths
  - stronger governance and adversarial evaluator coverage

#### Proposed V3 agent-role pool

One approved master pool should be used, categorized by task type. The orchestrator may dynamically choose the exact subset and agent count per task, but only from this approved pool.

Shared cross-task roles:
- `Evidence Auditor`
- `Decision Policy Reviewer`
- `Orchestrator`

`risk analysis` sub-pool:
- `Domain Risk Specialist`
- `Operational/Release Risk Specialist`
- `Security/Privacy Risk Specialist`

`calibration` sub-pool:
- `Dataset Quality Reviewer`
- `Label Consistency Reviewer`
- `Threshold/Calibration Reviewer`
- `Drift Reviewer`

#### Why this pool

- It mirrors real-world risk-assessment functions instead of arbitrary agent personas.
- It keeps the role model aligned with the agreed `lens + evidence + policy` structure.
- It preserves one governed master pool while still allowing dynamic task-specific composition.
- It keeps the orchestrator authoritative without collapsing into naive majority voting.

#### Proposed V3 governance and calibration model

Orchestrator override model:
- `evidence-first override` should be the default
- `policy-bounded override` should act as the safety backstop
- hard constraints should include:
  - no silent override
  - rationale must be logged
  - no weakening of evidence requirements for serious outcomes
  - no bypass of approval rules
  - no suppression of unresolved critical uncertainty in high-sensitivity cases

Calibration dataset model:
- `two-layer schema`
- a simple required user-facing case contract
- a richer internal annotation layer for calibration and review

Promotion model:
- `tiered promotion`
- cases should be classified as:
  - `trusted`
  - `provisional`
  - `excluded`

Calibration storage model:
- `normalized audit schema`
- the database should support multiple reviews, labels, promotion events, approval events, and scenario growth over time

Dataset-quality guidance model:
- combine principles-based guidance with explicit good-versus-bad dataset examples

Execution boundary model:
- `local-first core, cloud optional edge`
- keep orchestrator, evidence handling, final decisions, approvals, and audit writes local
- allow optional delegated work for adversarial critique, narrow specialist review, and calibration batch analysis

Override-trigger model:
- `evidence-gated override` should be the default
- `severity-and-policy override` should be the backstop

Calibration dataset field model:
- use an `extended two-layer schema`
- include a compact user-facing case contract
- include richer internal fields for:
  - evidence quality
  - severity and uncertainty labels
  - confidence expectation
  - override usage and legitimacy
  - policy band
  - drift tagging
  - promotion state
  - dataset version

Promotion-state model:
- use a `strict state machine`
- cases should be classified as:
  - `trusted`
  - `provisional`
  - `excluded`

Recommended calibration database shape:
- use an `audit-first normalized schema`
- recommended table families:
  - `cases`
  - `case_artifacts`
  - `case_reviews`
  - `case_labels`
  - `promotion_events`
  - `calibration_change_requests`
  - `calibration_change_approvals`
  - `dataset_versions`

Dataset-quality guidance model:
- combine principles-based guidance with explicit failure examples
- explain both what high-quality calibration data looks like and what common dataset mistakes look like

Preferred execution authority model:
- `local-only authority, cloud-only advisory`
- optional cloud use may support critique, bounded specialist review, or calibration batch work
- authority for final adjudication, approvals, and persisted policy changes should remain local

#### Exact recommended defaults

Override thresholds:
- use a `1-5` internal grading scale
- default evidence-gated override triggers:
  - minority view `evidenceStrength >= 4` and ahead of the leading consensus evidence grade by at least `2`
  - `evidenceCompleteness <= 2`
  - `disagreementLevel >= 4` together with `confidence <= 2`
- default severity-and-policy backstop triggers:
  - `riskSeverity >= 4` and `evidenceStrength >= 4`
  - `policyFit <= 2`
  - `decisionSensitivity >= 4` with unresolved uncertainty
- mandatory human escalation:
  - permission broadening
  - `Tier C` calibration changes
  - unresolved critical uncertainty in high-sensitivity cases
  - any override that would weaken serious-outcome evidence requirements

Calibration dataset fields:
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

Promotion criteria:
- `trusted`:
  - adjudicated
  - traceable
  - reviewed
  - no unresolved critical ambiguity
  - outcome-grounded or expert-adjudicated
- `provisional`:
  - reviewed and useful
  - but incomplete on traceability, outcome grounding, or label confidence
- `excluded`:
  - materially incomplete
  - contradictory
  - structurally ambiguous
  - noisy or lacking provenance

SQLite shape:
- recommended normalized tables:
  - `cases`
  - `case_artifacts`
  - `case_reviews`
  - `case_labels`
  - `promotion_events`
  - `calibration_change_requests`
  - `calibration_change_approvals`
  - `dataset_versions`

Dataset-quality guidance:
- strong datasets should be:
  - outcome-grounded
  - adjudicated
  - representative across typical, edge, and adversarial cases
  - traceable to the evidence available at decision time
  - versioned and reviewable
- weak datasets often fail because of:
  - hindsight leakage
  - easy-case bias
  - weak labels
  - missing evidence context
  - one-sided outcome bias

### V5

- evolve `PreMortemX` from a governed plugin into a governed execution environment
- make prompt, workflow, configuration, and context behavior explicit architecture assets
- preserve the existing release-risk, architecture-validation, calibration, and artifact model
- strengthen internal execution control without diluting the current product identity

### V6

- introduce a visual risk-journey surface for complex governed runs
- turn workflow state, branch state, boundary state, approval state, and adjudication state into one intuitive mental model
- make blocker precedence, winning path, and resume/re-entry behavior visually explicit
- strengthen the harness as a visible product moat rather than only an internal control layer

Recommended `v6` interaction model:
- `lifecycle rail + expandable branch tree + gate card + audit drawer`

Locked first-pass `v6` decisions:
- `artifact-based first`
- `HTML + inline SVG` rendering
- derived journey schema over canonical run artifacts
- auto-collapsed compact view for simple runs
- `release-risk-gating` only for `v6a`

Primary reference:
- [v6-risk-journey-prd.md](v6-risk-journey-prd.md)

First implementation contract:
- [v6a-journey-artifact-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v6a-journey-artifact-spec.md)

#### V5 architecture objective

`PreMortemX` should no longer depend on prompt/workflow behavior being implicitly scattered across skill text, runtime code, and documentation.

Instead, `v5` should introduce explicit execution-governance assets for:
- system prompts
- workflow rules
- metadata and configuration
- context engineering
- prompt templates

#### Recommended V5 architecture model

System prompts:
- use `layered governance + task overlays`
- one stable governance prompt should define:
  - identity
  - tone
  - safety boundaries
  - approval rules
  - evidence discipline
  - decision priorities
- smaller overlays should specialize the base for:
  - release-risk gating
  - architecture validation
  - calibration
  - specialist roles
  - orchestrator adjudication

Workflow rules:
- use a `deterministic stage-gated workflow`
- recommended canonical stages:
  1. `route`
  2. `inspect`
  3. `validate`
  4. `deliberate`
  5. `decide`
  6. `record`
  7. `verify`
  8. `summarize`
- each stage should define:
  - entry criteria
  - outputs
  - failure handling
  - retry behavior
  - approval requirements where relevant

Metadata and configuration:
- use a `static policy manifest + dynamic runtime resolver`
- static manifest responsibilities:
  - approved models
  - reasoning defaults
  - permission classes
  - allowed tools
  - feature flags
  - retention defaults
  - environment overlays
- runtime resolver responsibilities:
  - choose model by task, risk, and cost
  - enable or disable tools by mode and context
  - enforce approval gates before higher-risk behavior
  - decide whether specialist passes, calibration flows, or advisory edges are allowed

Context engineering:
- use a `guardrailed context pipeline`
- explicitly separate:
  - trusted instructions and policy
  - inspected evidence
  - user assertions
  - generated summaries
  - calibration and review metadata
- only validated structured fields should move between stages or agent roles by default
- long or noisy context should be summarized and reduced rather than replayed wholesale

Prompt templates:
- use a `versioned base prompt with variables`, combined with role-specific overlays
- maintain a reusable template family for:
  - release-risk mode
  - architecture-validation mode
  - calibration mode
  - specialist roles
  - orchestrator adjudication
  - smoke test mode
- template versions should be explicit and tied to evaluation coverage where practical

#### Recommended V5 asset set

Create explicit architecture assets for:
- `governance/`
  - base governance prompt
  - task overlays
  - specialist overlays
- `workflow/`
  - stage definitions
  - retry and approval rules
  - failure routing rules
- `policy/`
  - static manifest
  - environment overlays
  - feature-flag defaults
- `context/`
  - context contracts
  - trust-boundary definitions
  - summarization and carry-forward rules
- `templates/`
  - versioned prompt files
  - reusable interaction templates
  - output contract templates

High-level artifact layout and presentation structure are defined in:
- [v5-structure-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5-structure-spec.md)

#### V5 non-goals

- replacing the current `v4` runtime or artifact system
- introducing MCP by default
- adding broad new product modes before governance assets are stabilized
- turning `PreMortemX` into an autonomous release authority

#### Recommended V5 delivery split

- `v5a`: governance and template assets
  - base governance prompt
  - task and role overlays
  - versioned template family
- `v5b`: deterministic workflow asset layer
  - stage definitions
  - retry, failure, and approval rules
  - workflow verification coverage
- `v5c`: policy/config and context pipeline
  - static policy manifest
  - dynamic runtime resolver
  - context contracts and trust-boundary enforcement

#### Why V5 matters

The goal is not more prompt complexity.

The goal is:
- more reliable behavior across modes
- cleaner specialist and orchestrator coordination
- safer context flow
- clearer auditability of why the plugin behaved a certain way
- easier future extension without spreading governance logic across scripts and README prose

Detailed first-pass governance asset contracts for `v5a` are defined in:
- [v5a-governance-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5a-governance-spec.md)

Detailed first-pass workflow asset contracts for `v5b` are defined in:
- [v5b-workflow-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5b-workflow-spec.md)

Detailed first-pass runtime asset contracts for `v5c` are defined in:
- [v5c-runtime-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5c-runtime-spec.md)

Executable rollout planning for `v5a` / `v5b` / `v5c` is defined in:
- [v5-implementation-plan.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5-implementation-plan.md)

## Definition of Design Success

The design package is sufficient when it provides:
- a stable plugin identity and v1 scope
- explicit artifact conventions
- a stable run-record schema
- clear report templates
- feature-level acceptance criteria
- adversarial evaluator coverage
- a roadmap that preserves focus rather than diluting v1
