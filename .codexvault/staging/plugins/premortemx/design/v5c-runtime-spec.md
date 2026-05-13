# PreMortemX V5C Runtime Asset Spec

## Purpose

This document defines the exact first-pass contract for `v5c` runtime assets.

It covers:
- runtime artifact types
- required fields
- optional fields
- presentation order
- naming and file-shape rules

This is the `v5c` contract layer for runtime visibility, policy/config resolution, context boundaries, and operator-facing governance surfaces.

## Design Goal

`v5c` must make runtime governance:
- visible
- inspectable
- bounded
- operator-friendly

So the runtime should feel governed in plain sight, not governed behind the scenes.

## Runtime Asset Families

`v5c` should initially define six runtime asset types:
- `Control Tower View`
- `Governed Run Factsheet`
- `Boundary And Enforcement Panel`
- `Policy Resolver Record`
- `Context Contract`
- `Runtime Trace Summary`

## Common Runtime Asset Contract

All `v5c` runtime assets should share these common fields.

### Required common fields

- `title`
- `assetType`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`

### Optional common fields

- `scope`
- `linkedAssets`
- `linkedPolicies`
- `changeNotes`
- `reviewCadence`
- `tags`

### Allowed `status` values

- `draft`
- `active`
- `deprecated`
- `superseded`

### Presentation order for all runtime assets

1. title
2. status/version line
3. skim summary
4. runtime contract body
5. linked assets and dependencies
6. change/review metadata
7. critical summary or next action

## 1. Control Tower View

### Purpose

Provides one operator-facing overview of runtime governance state.

### Required fields

- `title`
- `assetType`: `Control Tower View`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `activePolicyProfile`
- `runtimeMode`
- `approvalPosture`
- `openBreaches`
- `recentAdjudications`
- `attentionQueue`

### Optional fields

- `environment`
- `linkedDashboards`
- `linkedFactsheets`
- `linkedPolicies`

### Required presentation sections

- `Skim Summary`
- `Active Policy Profile`
- `Runtime Mode`
- `Approval Posture`
- `Open Breaches And Exceptions`
- `Recent Adjudications`
- `Attention Queue`
- `Critical Summary`

## 2. Governed Run Factsheet

### Purpose

Provides the compact governed record for one run.

### Required fields

- `title`
- `assetType`: `Governed Run Factsheet`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `runId`
- `taskType`
- `scope`
- `activePolicyVersion`
- `activeConfigVersion`
- `approvalEvents`
- `triggeredThresholds`
- `finalAdjudication`
- `linkedArtifacts`

### Optional fields

- `environment`
- `runtimeMode`
- `reviewState`
- `exceptionState`

### Required presentation sections

- `Skim Summary`
- `Run Identity`
- `Scope`
- `Active Policy And Config`
- `Approval Events`
- `Triggered Thresholds`
- `Final Adjudication`
- `Linked Artifacts`
- `Critical Summary`

## 3. Boundary And Enforcement Panel

### Purpose

Shows what the runtime was allowed to do, what it was not allowed to do, and what enforcement logic applied.

### Required fields

- `title`
- `assetType`: `Boundary And Enforcement Panel`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `trustedInstructions`
- `allowedEvidenceClasses`
- `blockedContextClasses`
- `runtimeRestrictions`
- `approvalTier`
- `escalationPath`

### Optional fields

- `redactionRules`
- `sensitivityClass`
- `linkedControls`
- `linkedContextContracts`

### Required presentation sections

- `Skim Summary`
- `Trusted Instructions`
- `Allowed Evidence Classes`
- `Blocked Or Excluded Context`
- `Runtime Restrictions`
- `Approval Tier`
- `Escalation Path`
- `Critical Summary`

## 4. Policy Resolver Record

### Purpose

Shows how runtime policy/config was selected and applied.

### Required fields

- `title`
- `assetType`: `Policy Resolver Record`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `task`
- `selectedPolicyPack`
- `selectedModel`
- `selectedRuntime`
- `enabledControls`
- `disabledControls`
- `featureFlagsUsed`
- `selectionRationale`

### Optional fields

- `environment`
- `costProfile`
- `reasoningEffort`
- `linkedResolverInputs`

### Required presentation sections

- `Skim Summary`
- `Task`
- `Selected Policy Pack`
- `Selected Model And Runtime`
- `Enabled Controls`
- `Disabled Controls`
- `Feature Flags Used`
- `Selection Rationale`
- `Critical Summary`

## 5. Context Contract

### Purpose

Defines what context can flow where, under what transformation, and with what retention boundary.

### Required fields

- `title`
- `assetType`: `Context Contract`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `sourceContextClass`
- `allowedDownstreamTarget`
- `requiredTransformation`
- `prohibitedCarryForward`
- `retentionExpectation`

### Optional fields

- `redactionRequirement`
- `linkedBoundaries`
- `linkedStages`
- `linkedRoles`

### Required presentation sections

- `Skim Summary`
- `Source Context Class`
- `Allowed Downstream Target`
- `Required Transformation`
- `Prohibited Carry-forward`
- `Retention Expectation`
- `Critical Summary`

## 6. Runtime Trace Summary

### Purpose

Provides a concise trace-first account of what happened during runtime.

### Required fields

- `title`
- `assetType`: `Runtime Trace Summary`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `keyRuntimeEvents`
- `approvalsTriggered`
- `controlsTriggered`
- `overrideChecks`
- `finalAdjudicationPath`

### Optional fields

- `exceptionsRaised`
- `monitorSignals`
- `linkedArtifacts`
- `linkedPolicies`

### Required presentation sections

- `Skim Summary`
- `Key Runtime Events`
- `Approvals Triggered`
- `Controls Triggered`
- `Override Checks`
- `Final Adjudication Path`
- `Critical Summary`

## Naming Rules

### File naming

Use lower-case kebab-case for all asset files.

Recommended file name patterns:
- `control-tower-view-<name>.md`
- `governed-run-factsheet-<name>.md`
- `boundary-enforcement-panel-<name>.md`
- `policy-resolver-record-<name>.md`
- `context-contract-<name>.md`
- `runtime-trace-summary-<name>.md`

### Display naming

Use human-readable title case in the `title` field.

Examples:
- `Default Control Tower View`
- `Release Risk Governed Run Factsheet`
- `High-Sensitivity Boundary And Enforcement Panel`

## Presentation Rules

### What good looks like

Each runtime asset should support:
- a `5-second skim`
- a `30-second operator read`
- a `2-minute audit-oriented review`

### Visual rules

- make active state obvious
- make policy/config version visible
- make restrictions and approvals easy to spot
- keep the summary factual and operational
- use short sections and explicit labels
- surface breaches or exceptions prominently

### What to avoid

- hiding runtime restrictions
- hiding which policy/config was active
- burying approval events or threshold triggers
- mixing context-boundary logic into unrelated narrative prose

## Initial File Skeleton Order

All first-pass `v5c` asset files should follow this skeleton:

1. `# Title`
2. status/version/owner/updated line
3. `## Skim Summary`
4. required runtime sections for that asset type
5. `## Linked Assets`
6. `## Change And Review Notes`
7. `## Critical Summary`

## Definition Of Success

`v5c` runtime specification is good enough when:
- every runtime asset type has a stable contract
- operator-facing surfaces are explicit
- policy/config and boundary state are easy to inspect
- naming and presentation rules are fixed
- later implementation can create runtime-governance artifacts without guessing
