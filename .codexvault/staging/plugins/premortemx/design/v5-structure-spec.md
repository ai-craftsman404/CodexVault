# PreMortemX V5 Structure Spec

## Purpose

This document defines the initial high-level structure for `PreMortemX v5`.

Its job is not to lock every field or wording detail yet.  
Its job is to provide a clear mental model of:
- what artifact families exist
- how they relate to each other
- how `v5a`, `v5b`, and `v5c` should feel and look at a high level

The design principle is:
- intuitive first
- governed second
- detailed third

That means every `v5` surface should be easy to skim before it becomes deep.

## V5 Mental Model

`PreMortemX v5` should look like a governed execution environment with three visible layers:

1. `Governance assets`
- what rules, roles, prompts, and controls exist

2. `Workflow assets`
- how a governed decision moves through stages and approvals

3. `Runtime assets`
- what policy/config/context was active, what happened, and why

Those map directly to:
- `v5a`: governance and template assets
- `v5b`: deterministic workflow asset layer
- `v5c`: policy/config and context pipeline

## Top-Level Artifact Families

### 1. Governance assets

Purpose:
- define behavior boundaries
- define role boundaries
- define reusable prompt and control logic

Main artifact types:
- `Governance Prompt`
- `Task Overlay`
- `Role Card`
- `Control Card`
- `Policy Pack`
- `Template Card`

Presentation model:
- factsheet-style asset cards
- summary-first
- role and control separation
- lifecycle/version visible

### 2. Workflow assets

Purpose:
- make execution stages visible
- make approvals explicit
- make handoffs traceable

Main artifact types:
- `Lifecycle Map`
- `Stage Definition`
- `Approval Playbook`
- `Handoff Summary`
- `Exception/Re-entry Rule`

Presentation model:
- lifecycle rail
- approval playbook cards
- trace-first handoff summaries
- breach/exception banners when relevant

### 3. Runtime assets

Purpose:
- show what was active at runtime
- show what boundaries applied
- show what evidence, controls, and approvals shaped the outcome

Main artifact types:
- `Control Tower View`
- `Governed Run Factsheet`
- `Boundary and Enforcement Panel`
- `Policy Resolver Record`
- `Context Contract`
- `Runtime Trace Summary`

Presentation model:
- operator dashboard
- governed per-run factsheet
- visible boundary and enforcement panel

## Proposed High-Level Folder Structure

```text
plugins/premortemx/
  governance/
    prompts/
    overlays/
    roles/
    controls/
    policy-packs/
    templates/

  workflow/
    lifecycle/
    stages/
    approvals/
    handoffs/
    exceptions/

  runtime/
    policies/
    context/
    traces/
    dashboards/
    factsheets/
```

This does not replace the current runtime/report folders yet.  
It gives `v5` a new explicit governance structure alongside the existing plugin runtime.

## V5A High-Level Structure

### Goal

Create a governed asset system that is easy to read and maintain.

### Core artifacts

#### `Governance Prompt`

Purpose:
- stable base behavior contract

Expected high-level sections:
- title
- purpose
- scope
- applies to
- key rules
- safety boundaries
- approval posture
- linked overlays
- version/status

#### `Task Overlay`

Purpose:
- specialize the base governance prompt for a task or mode

Expected high-level sections:
- title
- parent governance prompt
- task or mode
- extra rules
- exclusions
- evidence expectations
- escalation notes
- version/status

#### `Role Card`

Purpose:
- define a specialist or orchestrator role

Expected high-level sections:
- role name
- purpose
- when used
- inputs
- outputs
- must do
- must not do
- escalation behavior
- linked controls

#### `Control Card`

Purpose:
- define a control, threshold, approval gate, or restriction

Expected high-level sections:
- control name
- purpose
- trigger
- effect
- approval tier
- evidence requirement
- override rule
- audit expectation

#### `Policy Pack`

Purpose:
- group related controls into one policy object

Expected high-level sections:
- pack name
- purpose
- applies to
- included controls
- required templates
- approval model
- exceptions
- version/status

#### `Template Card`

Purpose:
- define a reusable prompt/output template

Expected high-level sections:
- template name
- purpose
- used by
- variables
- output contract
- linked policy pack
- version/status

Exact first-pass field contracts for these `v5a` assets are defined in:
- [v5a-governance-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5a-governance-spec.md)

## V5B High-Level Structure

### Goal

Make the governed workflow visible, explicit, and easy to follow.

### Core artifacts

#### `Lifecycle Map`

Purpose:
- show the full governed execution flow at a glance

Expected high-level stages:
- `Intake`
- `Assess`
- `Deliberate`
- `Approve/Block`
- `Monitor`
- `Revisit`

#### `Stage Definition`

Purpose:
- define what each stage does

Expected high-level sections:
- stage name
- purpose
- entry criteria
- actions
- outputs
- approval need
- failure path
- next stage

#### `Approval Playbook`

Purpose:
- define how a gated decision is approved, blocked, or escalated

Expected high-level sections:
- playbook name
- applies to
- approval tier
- owner
- required evidence
- allowed outcomes
- escalation path
- audit trail

#### `Handoff Summary`

Purpose:
- make one stage’s output easy for the next stage to consume

Expected high-level sections:
- stage completed
- what was decided
- why
- evidence used
- open issues
- next owner
- next required action

#### `Exception/Re-entry Rule`

Purpose:
- define when a case re-enters the workflow

Expected high-level sections:
- trigger
- severity
- re-entry stage
- owner
- expected follow-up

Exact first-pass field contracts for these `v5b` assets are defined in:
- [v5b-workflow-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5b-workflow-spec.md)

## V5C High-Level Structure

### Goal

Make runtime governance visible, inspectable, and intuitive for operators.

### Core artifacts

#### `Control Tower View`

Purpose:
- one operator-facing overview

Expected high-level sections:
- active policy profile
- runtime mode
- approval posture
- open breaches/exceptions
- recent adjudications
- monitored runs needing attention

#### `Governed Run Factsheet`

Purpose:
- compact governed record for one run

Expected high-level sections:
- run identity
- task type
- scope
- active config/policy version
- approval events
- thresholds triggered
- final adjudication
- linked artifacts

#### `Boundary and Enforcement Panel`

Purpose:
- show what the runtime was allowed to do and not do

Expected high-level sections:
- trusted instructions
- allowed evidence classes
- blocked or excluded context
- runtime restrictions
- approval tier
- escalation path

#### `Policy Resolver Record`

Purpose:
- show how runtime policy/config was resolved

Expected high-level sections:
- task
- selected policy pack
- selected model/runtime
- enabled controls
- disabled controls
- feature flags used
- reason for selections

#### `Context Contract`

Purpose:
- define what context may flow between stages/roles

Expected high-level sections:
- source context class
- allowed downstream target
- required transformation
- prohibited carry-forward
- retention expectation

#### `Runtime Trace Summary`

Purpose:
- concise trace-first runtime history

Expected high-level sections:
- key runtime events
- approvals triggered
- controls triggered
- override checks
- final adjudication path

Exact first-pass field contracts for these `v5c` assets are defined in:
- [v5c-runtime-spec.md](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/design/v5c-runtime-spec.md)

## Presentation Rules Across All V5 Assets

Every major `v5` artifact should follow this high-level pattern:

1. `Title and status at the top`
2. `Fast skim summary immediately below`
3. `Detailed core sections in the middle`
4. `Critical summary or next action at the bottom`

Common display fields:
- title
- purpose
- scope
- owner
- version
- status
- last updated

Tone:
- crisp
- operational
- evidence-oriented
- not academic

## Initial Development Order

Recommended order:

1. define the `v5a` governance asset family
2. define the `v5b` workflow asset family
3. define the `v5c` runtime visibility asset family
4. then refine field-level detail inside each

This keeps the work mentally manageable and avoids premature low-level design.

## Definition Of Success For This Spec

This high-level structure is good enough if it gives us:
- one coherent mental model
- named artifact families
- named core artifact types
- a believable folder structure
- a clear split between `v5a`, `v5b`, and `v5c`
- enough structure to begin low-level detailing next
