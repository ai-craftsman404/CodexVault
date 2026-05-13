# PreMortemX V5B Workflow Asset Spec

## Purpose

This document defines the exact first-pass contract for `v5b` workflow assets.

It covers:
- workflow artifact types
- required fields
- optional fields
- presentation order
- naming and file-shape rules

This is the `v5b` contract layer for deterministic stage-gated workflow presentation.

## Design Goal

`v5b` must make workflow governance:
- visible
- legible
- traceable
- actionable

So the workflow should look like an explicit governed lifecycle, not hidden internal logic.

## Workflow Asset Families

`v5b` should initially define five workflow asset types:
- `Lifecycle Map`
- `Stage Definition`
- `Approval Playbook`
- `Handoff Summary`
- `Exception/Re-entry Rule`

## Common Workflow Asset Contract

All `v5b` workflow assets should share these common fields.

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

### Presentation order for all workflow assets

1. title
2. status/version line
3. skim summary
4. workflow contract body
5. linked assets and dependencies
6. change/review metadata
7. critical summary or next action

## 1. Lifecycle Map

### Purpose

Defines the visible end-to-end governed lifecycle for `PreMortemX`.

### Required fields

- `title`
- `assetType`: `Lifecycle Map`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `stages`
- `entryPoint`
- `terminalStates`
- `reentryPaths`

### Optional fields

- `appliesTo`
- `linkedStageDefinitions`
- `linkedApprovalPlaybooks`
- `linkedExceptionRules`

### Required presentation sections

- `Skim Summary`
- `Lifecycle Rail`
- `Entry Point`
- `Terminal States`
- `Re-entry Paths`
- `Linked Stage Definitions`
- `Critical Summary`

## 2. Stage Definition

### Purpose

Defines one explicit workflow stage and what it must produce.

### Required fields

- `title`
- `assetType`: `Stage Definition`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `stageName`
- `entryCriteria`
- `actions`
- `requiredInputs`
- `requiredOutputs`
- `approvalRequirement`
- `failurePath`
- `nextStage`

### Optional fields

- `retryBehavior`
- `timeExpectation`
- `linkedPlaybooks`
- `linkedPolicies`

### Required presentation sections

- `Skim Summary`
- `Entry Criteria`
- `Required Inputs`
- `Actions`
- `Required Outputs`
- `Approval Requirement`
- `Failure Path`
- `Next Stage`
- `Critical Summary`

## 3. Approval Playbook

### Purpose

Defines how one gated decision is approved, blocked, or escalated.

### Required fields

- `title`
- `assetType`: `Approval Playbook`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `playbookName`
- `appliesTo`
- `approvalTier`
- `decisionOwner`
- `requiredEvidence`
- `allowedOutcomes`
- `escalationPath`
- `auditTrail`

### Optional fields

- `linkedControls`
- `linkedStages`
- `exceptionHandling`
- `slaExpectation`

### Required presentation sections

- `Skim Summary`
- `Applies To`
- `Approval Tier`
- `Decision Owner`
- `Required Evidence`
- `Allowed Outcomes`
- `Escalation Path`
- `Audit Trail`
- `Critical Summary`

## 4. Handoff Summary

### Purpose

Defines the required handoff shape from one workflow stage to the next.

### Required fields

- `title`
- `assetType`: `Handoff Summary`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `fromStage`
- `toStage`
- `decisionMade`
- `decisionRationale`
- `evidenceUsed`
- `openIssues`
- `nextOwner`
- `nextRequiredAction`

### Optional fields

- `blockedDependencies`
- `followupDeadline`
- `linkedArtifacts`

### Required presentation sections

- `Skim Summary`
- `From And To`
- `Decision Made`
- `Decision Rationale`
- `Evidence Used`
- `Open Issues`
- `Next Owner`
- `Next Required Action`
- `Critical Summary`

## 5. Exception/Re-entry Rule

### Purpose

Defines when and how a case re-enters the lifecycle.

### Required fields

- `title`
- `assetType`: `Exception/Re-entry Rule`
- `purpose`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `trigger`
- `severity`
- `reentryStage`
- `requiredOwner`
- `expectedFollowup`

### Optional fields

- `temporaryMitigation`
- `linkedThresholds`
- `linkedPlaybooks`
- `linkedArtifacts`

### Required presentation sections

- `Skim Summary`
- `Trigger`
- `Severity`
- `Re-entry Stage`
- `Required Owner`
- `Expected Follow-up`
- `Temporary Mitigation`
- `Critical Summary`

## Naming Rules

### File naming

Use lower-case kebab-case for all asset files.

Recommended file name patterns:
- `lifecycle-map-<name>.md`
- `stage-definition-<name>.md`
- `approval-playbook-<name>.md`
- `handoff-summary-<name>.md`
- `exception-rule-<name>.md`

### Display naming

Use human-readable title case in the `title` field.

Examples:
- `Core Governance Lifecycle Map`
- `Assess Stage Definition`
- `High-Sensitivity Approval Playbook`
- `Assess To Deliberate Handoff Summary`

## Presentation Rules

### What good looks like

Each workflow asset should support:
- a `5-second skim`
- a `30-second operational read`
- a `2-minute governance review`

### Visual rules

- make stage names explicit
- show ownership clearly
- keep transitions visible
- show approval state clearly
- show next action clearly
- use short lists over long prose

### What to avoid

- hiding the next stage
- hiding the decision owner
- mixing approval logic into unrelated stage prose
- burying failure or escalation paths

## Initial File Skeleton Order

All first-pass `v5b` asset files should follow this skeleton:

1. `# Title`
2. status/version/owner/updated line
3. `## Skim Summary`
4. required workflow sections for that asset type
5. `## Linked Assets`
6. `## Change And Review Notes`
7. `## Critical Summary`

## Definition Of Success

`v5b` workflow specification is good enough when:
- every workflow asset type has a stable contract
- stage visibility is explicit
- approval and escalation logic are easy to find
- naming and presentation rules are fixed
- later implementation can create deterministic workflow artifacts without guessing
