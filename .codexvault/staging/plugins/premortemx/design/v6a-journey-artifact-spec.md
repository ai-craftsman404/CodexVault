# PreMortemX V6A Journey Artifact Spec

## Purpose

`v6a` should introduce the first real visual risk-journey artifact for `PreMortemX`.

This spec defines:
- exact output artifact names
- folder placement
- journey-builder input and output contract
- minimum rendering requirements
- first synthetic test coverage

`v6a` is intentionally narrow:
- `artifact-based first`
- `release-risk-gating` only
- derived from existing canonical run artifacts

## Scope

`v6a` must produce a per-run visual layer that sits above the existing summaries and machine-readable records.

It must not:
- replace `run-record.json`
- replace `approvals.json`
- replace `deliberation.json`
- introduce a standalone application surface
- attempt multi-mode generalization yet

## Folder Placement

The generated `v6a` artifacts should live in the run folder beside the existing run outputs.

Recommended placement:
- `<run>/journey-view.html`
- `<run>/journey-view.json`

Optional later additions:
- `<run>/journey-view.svg`
- `<run>/journey-view-assets/`

For `v6a`, keep the surface self-contained where practical:
- prefer one HTML file
- prefer inline SVG
- avoid external asset dependencies unless necessary

## Artifact Set

### 1. `journey-view.html`

Primary user-facing artifact.

Purpose:
- first visual landing surface for the governed journey
- render the lifecycle rail
- render the branch tree
- render the gate card
- support compact expand/collapse behavior

Minimum requirements:
- readable as a local file
- no required network dependency
- all critical journey information visible without opening JSON
- clear `current state`, `winning path`, and `next action`

### 2. `journey-view.json`

Canonical derived view-model artifact for `v6a`.

Purpose:
- make the visual layer testable
- separate derivation logic from rendering logic
- keep the generated HTML deterministic and inspectable

This file is not the primary source of truth for the run.
It is the primary source of truth for the derived journey surface.

## Journey Builder Contract

The `journey-view.json` artifact should be generated from the canonical run artifacts:
- `run-record.json`
- `approvals.json`
- `deliberation.json`

The builder may also read:
- `summary-short.md`
- `summary-standard.md`
- `summary-exec.md`

But markdown summaries are supportive only.
They must not override machine-readable run state.

### Builder responsibilities

- derive the current journey state
- identify the dominant/winning path
- identify blocked or re-entry paths
- derive one current gate card
- emit a compact view when the run is simple
- emit expanded branch information when the run is complex

### Builder must not

- invent new risk outcomes
- mutate canonical source artifacts
- silently ignore source-state contradictions

If contradictions are found, the builder should:
- prefer canonical machine-readable records
- emit a visible derivation warning in `journey-view.json`
- surface a compact warning in `journey-view.html`

## Derived JSON Contract

### Root object

Required top-level fields:
- `schemaVersion`
- `runId`
- `mode`
- `generatedAt`
- `currentNodeId`
- `winningNodeId`
- `isCompact`
- `derivationWarnings[]`
- `journey`
- `gateCard`

### `journey`

Required:
- `nodes[]`
- `edges[]`

### `nodes[]`

Required per node:
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

Recommended optional fields:
- `riskLevel`
- `residualRisk`
- `approvalStatus`
- `isCurrent`
- `isWinningPath`
- `isBlocked`
- `blockedBy[]`
- `displayOrder`

### `edges[]`

Required per edge:
- `id`
- `from`
- `to`
- `type`
- `label`
- `isWinningPath`
- `sourceRefs[]`

Recommended optional fields:
- `isBlockedEdge`
- `precedenceRank`

### `gateCard`

Required:
- `nodeId`
- `finalRecommendation`
- `approvalStatus`
- `gateStatus`
- `blockerPrecedence`
- `allowedNextStage`
- `decisionOwner`
- `nextOwner`
- `resumeGuidance`

Recommended optional fields:
- `boundaryStatus`
- `confirmationRequired`
- `confirmationReason`
- `currentAction`

## Node And Edge Rules

### Node identity

- use stable ids within a run
- ids must be deterministic from the source-state where practical
- ids must not depend on render order only

### Node kinds

Allowed `v6a` node kinds:
- `stage`
- `branch`
- `gate`
- `reentry`

### Path types

Allowed `v6a` path types:
- `mainline`
- `risk`
- `evidence-gap`
- `boundary`
- `approval`
- `remediation`
- `revisit`

### Edge types

Allowed `v6a` edge types:
- `progresses`
- `branches`
- `blocked-by`
- `reenters`
- `resolves-to`

## Compact Vs Expanded Behavior

`v6a` should default simple runs to compact mode.

A run should be considered compact when all of the following are true:
- one dominant mainline path exists
- no meaningful branch competition exists
- no active re-entry loop is present
- no unresolved blocker precedence ambiguity exists

If any of the above is false, the builder should emit:
- `isCompact = false`

Compact mode should still show:
- lifecycle rail
- current node
- winning path
- gate card
- next action

Expanded mode should additionally show:
- visible branch splits
- blocked branches
- re-entry pathing
- competing or losing paths

## HTML Rendering Contract

`journey-view.html` should:
- render the journey entirely from `journey-view.json`
- use `inline SVG` for the visual rail/tree layer
- remain readable without JavaScript-heavy dependencies

Required visible regions:
- title/header
- current-state summary strip
- lifecycle rail
- journey tree
- gate card
- source-artifact links

Minimum interactivity allowed in `v6a`:
- expand/collapse detail groups
- node selection highlighting
- reveal/hide derivation warnings

Do not require in `v6a`:
- complex animations
- drag/pan canvas controls
- real-time refresh
- server-side behavior

## Naming And Link Rules

The HTML should link back to the canonical artifacts where useful:
- `run-record.json`
- `approvals.json`
- `deliberation.json`
- `summary-short.md`
- `summary-standard.md`
- `summary-exec.md`

Labeling should use plain operator-facing language.

Prefer:
- `Current State`
- `Winning Path`
- `Blocked By`
- `Resume At`
- `Next Action`
- `Decision Owner`

Avoid raw schema labels in the primary visual surface unless needed for drill-down.

## Minimum Synthetic Test Matrix For V6A

`v6a` should ship with synthetic tests covering at least:

### 1. Clean pass compact run

Expected:
- compact mode
- one winning path
- no blocked branches
- clear proceed state

### 2. Warn with approval gate

Expected:
- expanded or semi-expanded path
- visible gate card
- approval posture visible
- next action visible

### 3. Block with boundary blocker

Expected:
- blocked branch visible
- blocker precedence visible
- resume guidance visible

### 4. Re-entry/remediation case

Expected:
- explicit re-entry edge
- resume stage visible
- path back into progression visible

### 5. Contradictory source-state case

Expected:
- derivation warning emitted
- canonical precedence honored
- HTML warning surface visible

## Acceptance Criteria

`v6a` is ready when:
- a fresh run can generate `journey-view.json`
- a fresh run can generate `journey-view.html`
- simple runs collapse correctly
- blocked and re-entry paths render clearly
- the gate card matches canonical run state
- synthetic tests pass for the minimum first-case set

## Recommended Next Step After This Spec

Build order:
1. journey derivation function
2. synthetic JSON contract tests
3. HTML renderer
4. end-to-end visual artifact tests
