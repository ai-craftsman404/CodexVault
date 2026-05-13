# PreMortemX V5A Governance Asset Spec

## Purpose

This document defines the exact first-pass contract for `v5a` governance assets.

It covers:
- artifact types
- required fields
- optional fields
- presentation order
- naming and file-shape rules

This is the `v5a` contract layer that later implementation should follow.

## Design Goal

`v5a` must make governance assets:
- easy to skim
- easy to compare
- easy to maintain
- hard to misunderstand

So every governance asset should feel like a `factsheet`, not like a loose design memo.

## Governance Asset Families

`v5a` should initially define six governed asset types:
- `Governance Prompt`
- `Task Overlay`
- `Role Card`
- `Control Card`
- `Policy Pack`
- `Template Card`

## Common Asset Contract

All `v5a` governance assets should share these common fields:

### Required common fields

- `title`
- `assetType`
- `purpose`
- `scope`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`

### Optional common fields

- `appliesTo`
- `dependencies`
- `linkedAssets`
- `changeNotes`
- `reviewCadence`
- `tags`

### Allowed `status` values

- `draft`
- `active`
- `deprecated`
- `superseded`

### Presentation order for all governance assets

1. title
2. status/version line
3. skim summary
4. core contract body
5. dependencies and linked assets
6. change/review metadata
7. critical summary or next action

## 1. Governance Prompt

### Purpose

Defines the stable base behavior contract for a governed execution mode or family.

### Required fields

- `title`
- `assetType`: `Governance Prompt`
- `purpose`
- `scope`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `identity`
- `tone`
- `decisionPriorities`
- `safetyBoundaries`
- `approvalPosture`
- `evidenceDiscipline`
- `defaultFailureBehavior`

### Optional fields

- `appliesTo`
- `linkedOverlays`
- `nonGoals`
- `examples`
- `changeNotes`

### Required presentation sections

- `Skim Summary`
- `Identity And Role`
- `Decision Priorities`
- `Safety Boundaries`
- `Approval Posture`
- `Evidence Discipline`
- `Default Failure Behavior`
- `Linked Overlays`
- `Change And Review Notes`
- `Critical Summary`

## 2. Task Overlay

### Purpose

Specializes a base governance prompt for one mode, task, or bounded context.

### Required fields

- `title`
- `assetType`: `Task Overlay`
- `purpose`
- `scope`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `parentPrompt`
- `taskMode`
- `extraRules`
- `exclusions`
- `evidenceExpectations`
- `escalationBehavior`

### Optional fields

- `allowedTools`
- `disallowedTools`
- `specialistRoles`
- `examples`
- `linkedControls`

### Required presentation sections

- `Skim Summary`
- `Parent Prompt`
- `Task Mode`
- `Extra Rules`
- `Explicit Exclusions`
- `Evidence Expectations`
- `Escalation Behavior`
- `Linked Controls`
- `Critical Summary`

## 3. Role Card

### Purpose

Defines one specialist or orchestrator role clearly and separately from policy.

### Required fields

- `title`
- `assetType`: `Role Card`
- `purpose`
- `scope`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `roleName`
- `whenUsed`
- `inputs`
- `outputs`
- `mustDo`
- `mustNotDo`
- `escalationBehavior`

### Optional fields

- `rubricFocus`
- `linkedControls`
- `sampleQuestions`
- `handoffTargets`

### Required presentation sections

- `Skim Summary`
- `When This Role Is Used`
- `Inputs`
- `Outputs`
- `Must Do`
- `Must Not Do`
- `Escalation Behavior`
- `Linked Controls`
- `Critical Summary`

## 4. Control Card

### Purpose

Defines one enforceable control, threshold, approval rule, or restriction.

### Required fields

- `title`
- `assetType`: `Control Card`
- `purpose`
- `scope`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `controlName`
- `trigger`
- `effect`
- `approvalTier`
- `evidenceRequirement`
- `overrideRule`
- `auditExpectation`

### Optional fields

- `thresholdLogic`
- `appliesTo`
- `exceptionPath`
- `linkedRoles`
- `linkedPolicyPacks`

### Required presentation sections

- `Skim Summary`
- `Trigger`
- `Effect`
- `Approval Tier`
- `Evidence Requirement`
- `Override Rule`
- `Audit Expectation`
- `Exceptions`
- `Critical Summary`

## 5. Policy Pack

### Purpose

Groups related control cards and governance intent into one reusable governed package.

### Required fields

- `title`
- `assetType`: `Policy Pack`
- `purpose`
- `scope`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `packName`
- `appliesTo`
- `includedControls`
- `approvalModel`
- `requiredTemplates`

### Optional fields

- `exceptions`
- `linkedPrompts`
- `linkedOverlays`
- `linkedRunFactsheets`

### Required presentation sections

- `Skim Summary`
- `Applies To`
- `Included Controls`
- `Approval Model`
- `Required Templates`
- `Exceptions`
- `Linked Assets`
- `Critical Summary`

## 6. Template Card

### Purpose

Defines a reusable prompt or output template as a governed asset.

### Required fields

- `title`
- `assetType`: `Template Card`
- `purpose`
- `scope`
- `owner`
- `status`
- `version`
- `lastUpdated`
- `summary`
- `templateName`
- `usedBy`
- `variables`
- `outputContract`

### Optional fields

- `linkedPolicyPack`
- `linkedPrompt`
- `linkedOverlay`
- `examples`
- `validationNotes`

### Required presentation sections

- `Skim Summary`
- `Used By`
- `Variables`
- `Output Contract`
- `Linked Governance Assets`
- `Validation Notes`
- `Critical Summary`

## Naming Rules

### File naming

Use lower-case kebab-case for all asset files.

Recommended file name patterns:
- `governance-prompt-<name>.md`
- `task-overlay-<name>.md`
- `role-card-<name>.md`
- `control-card-<name>.md`
- `policy-pack-<name>.md`
- `template-card-<name>.md`

### Display naming

Use human-readable title case in the `title` field.

Examples:
- `Release Governance Prompt`
- `Architecture Validation Overlay`
- `Evidence Auditor Role Card`
- `High-Sensitivity Approval Control`

## Presentation Rules

### What good looks like

Each asset should support:
- a `5-second skim`
- a `30-second informed read`
- a `2-minute detailed review`

### Visual rules

- summary first
- short sections
- explicit labels
- minimal prose paragraphs
- bullets for operational rules
- critical summary at the bottom

### What to avoid

- giant narrative blocks
- mixing role and control logic in one artifact
- hiding status/version metadata
- burying the critical rule in the middle of the file

## Initial File Skeleton Order

All first-pass `v5a` asset files should follow this skeleton:

1. `# Title`
2. status/version/owner/updated line
3. `## Skim Summary`
4. required core sections for that asset type
5. `## Linked Assets`
6. `## Change And Review Notes`
7. `## Critical Summary`

## Definition Of Success

`v5a` governance specification is good enough when:
- every governance asset type has a stable contract
- required fields are explicit
- presentation order is fixed
- naming rules are fixed
- later implementation can create files from this without guessing
