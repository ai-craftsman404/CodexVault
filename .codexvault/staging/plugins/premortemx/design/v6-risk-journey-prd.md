# PreMortemX V6 PRD

## Title

`v6` Risk Journey View

## Purpose

`v6` should introduce a visual risk-journey surface for `PreMortemX`.

The goal is to help users understand:
- how the governed assessment progressed
- where risk branched, escalated, narrowed, or paused
- why the final adjudication won
- what remediation or approval action re-opens progression

This feature is intended to strengthen the harness by turning governed workflow state into an intuitive mental model for complex cases.

## Problem

Current `PreMortemX` artifacts are strong for:
- decision quality
- auditability
- operator guidance
- structured governance

But they are still mostly report-shaped.

For complex cases, users may still struggle to quickly see:
- the full journey through the assessment
- the branch points that mattered
- the dominant blocker or gate at each point
- the path back into progression after remediation or escalation

This is especially important when:
- multiple blocker families interact
- risk accumulates across stages
- workflow and boundary state both matter
- users need a fast mental model before reading detailed artifacts

## Product Goal

Provide one governed visual surface that makes `PreMortemX` feel:
- clearer
- more intuitive
- more enterprise-usable
- more differentiated

This should not replace the current artifacts.

It should sit above them as a visual navigation and comprehension layer.

## Core User Outcomes

Users should be able to answer these questions quickly:
- Where is this run in the governed lifecycle?
- Which branch or branches caused the current risk posture?
- What blocker has precedence right now?
- Why did the final path win?
- What exact action re-opens progression?
- Which owner or approver is responsible next?

## Primary Feature Concept

Recommended shape:
- `lifecycle rail + expandable branch tree + gate card + audit drawer`

This is the preferred `v6` model.

## Locked Direction

The following `v6` shaping decisions are now locked for the first implementation pass:

- delivery model: `artifact-based first`
- rendering model: `HTML + inline SVG`
- state model: `derived-first journey schema`
- first-mode scope: `release-risk-gating`
- default behavior for simple runs: `auto-collapse to a compact view`

This means `v6a` should generate a per-run visual artifact rather than introduce a full interactive application surface first.

The visual journey must remain derived from canonical run artifacts, not become a competing source of truth.

## Core Feature Set

### 1. Lifecycle rail

A fixed governed stage rail:
- `Intake`
- `Assess`
- `Deliberate`
- `Approve/Block`
- `Monitor`
- `Revisit`

Purpose:
- anchor the user in the official workflow
- show current stage, completed stages, and next stage
- show resume/re-entry target when blocked

### 2. Expandable branch tree

A branch/tree visualization showing:
- branch points
- major risk paths
- evidence-gap paths
- blocked paths
- winning adjudicated path

Each node should support:
- stage
- branch title
- local risk state
- branch outcome
- visible status color/state

### 3. Gate / approval card

A central decision/gate card for the selected stage or active node showing:
- final recommendation
- approval status
- gate status
- blocker precedence
- current action
- allowed next stage
- decision owner / next owner

This is the canonical operator-action surface.

### 4. Branch detail side panel

When a node is selected, show:
- rationale summary
- risk accumulation or reduction
- evidence refs
- residual risk note
- remediation path
- owner
- adjudication note

### 5. Audit / evidence drawer

An expandable secondary layer for:
- evidence links
- approval events
- exception log
- decision path
- override notes
- trace notes

Purpose:
- keep the main surface readable
- preserve auditability without clutter

### 6. Re-entry loop map

Visible return arrows or resume links for:
- blocked approval
- active exception
- boundary violation
- monitoring-triggered revisit

Each loop should show:
- why the run paused
- what must be fixed
- where the run resumes

## Presentation Principles

The `v6` surface should be:
- summary-first
- action-oriented
- visually intuitive
- enterprise-serious
- governance-readable

It should avoid:
- exposing too much audit detail by default
- overly decorative charting
- replacing the canonical reports with pure visualization

## Harness Value

This feature matters because it operationalizes the harness visually.

It turns:
- workflow state
- boundary state
- approval state
- exception state
- adjudication state

into one understandable journey.

That strengthens the moat because the value is not just:
- “an AI did risk analysis”

but:
- “the governed harness made the whole journey understandable, resumable, and auditable”

## Likely Inputs

The initial `v6` view should derive from existing artifacts where possible:
- `run-record.json`
- `approvals.json`
- `deliberation.json`
- `summary-*`
- workflow and runtime governed assets

This reduces rework and keeps the new feature harness-native.

## Rendering Strategy

The preferred first implementation is:
- one generated `HTML` artifact per run
- `inline SVG` for the journey view itself
- lightweight local interactivity only where it improves comprehension:
  - expand/collapse
  - node selection
  - audit-drawer reveal

Why this is preferred:
- stays local-first and file-based
- fits the existing run-folder artifact model
- is easy to inspect, archive, and test
- is richer than static markdown while avoiding a premature standalone UI

Rejected first-pass alternatives:
- `SVG-first` single-file output only
- `Markdown + Mermaid` as the primary rendering layer

Those may remain secondary export or fallback options later, but should not lead `v6a`.

## Derived Journey Schema

`v6` should use a derived journey view model layered over the existing canonical run artifacts.

The canonical record remains:
- `run-record.json`
- `approvals.json`
- `deliberation.json`

The visual layer should derive a dedicated `journey` object with this minimum shape:

### Journey

- `schemaVersion`
- `runId`
- `mode`
- `currentNodeId`
- `winningNodeId`
- `generatedAt`

### Nodes

Each node should include:
- `id`
- `parentId`
- `kind`
- `stage`
- `title`
- `status`
- `pathType`
- `decision`
- `gateStatus`
- `boundaryStatus`
- `summary`
- `owner`
- `nextAction`
- `resumeStage`
- `sourceRefs[]`

Recommended node kinds:
- `stage`
- `branch`
- `gate`
- `reentry`

Recommended path types:
- `mainline`
- `risk`
- `evidence-gap`
- `boundary`
- `approval`
- `remediation`
- `revisit`

### Edges

Each edge should include:
- `id`
- `from`
- `to`
- `type`
- `label`
- `isWinningPath`
- `sourceRefs[]`

Recommended edge types:
- `progresses`
- `branches`
- `blocked-by`
- `reenters`
- `resolves-to`

### Gate Card

The run should expose one derived gate-card object with:
- `nodeId`
- `finalRecommendation`
- `approvalStatus`
- `blockerPrecedence`
- `allowedNextStage`
- `decisionOwner`
- `nextOwner`
- `resumeGuidance`

This is the operator-facing action surface for the selected or current node.

## Non-Goals For First V6 Slice

Do not require:
- a full standalone dashboard product
- real-time collaborative editing
- every audit artifact visible on first load
- heavy visualization for trivial runs

The first slice should focus on:
- complex-run comprehension
- governed journey clarity
- blocker and resume clarity
- one fully worked primary mode before multi-mode generalization

## Release Shape

Recommended split:

### `v6a`
- lifecycle rail
- gate card
- branch tree foundation
- derived node/state schema
- generated `HTML + inline SVG` artifact
- compact auto-collapsed default for simple runs
- scope limited to `release-risk-gating`

### `v6b`
- detail side panel
- audit drawer
- re-entry loop presentation
- tighter artifact integration

### `v6c`
- richer control-tower/operator aggregation
- cross-run journey comparison
- stronger enterprise oversight surfaces

## Success Criteria

`v6` should be considered successful if:
- users can identify the current blocker and next action faster than with reports alone
- complex runs are easier to understand at a glance
- resume/re-entry logic is visually clearer
- the feature feels harness-native, not bolted on
- it improves perceived differentiation of `PreMortemX`

## Open Questions For Later

- how much branch scoring should be visualized explicitly
- whether cross-run comparison belongs in `v6` or later
