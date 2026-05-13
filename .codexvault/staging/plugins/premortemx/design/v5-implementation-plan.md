# PreMortemX V5 Implementation Plan

## Purpose

This document turns the `v5` architecture and artifact specs into a buildable rollout plan.

It assumes the following are already agreed:
- `v5a`, `v5b`, and `v5c` ship as separate releases
- each slice gets its own synthetic e2e validation
- development starts `docs/config first`
- runtime wiring happens incrementally after the asset layer is stable
- testing should follow the existing strict discipline, including adversarial evaluator coverage

## Rollout Model

### `v5a`

Focus:
- governance and template assets

Primary outcome:
- `PreMortemX` gains explicit governed prompt, overlay, role, control, policy-pack, and template assets as real files

Implementation style:
- docs/config first
- no major runtime dependency on these assets yet
- generator/runtime may still use legacy paths while the governed asset family is stabilized

### `v5b`

Focus:
- deterministic workflow asset layer

Primary outcome:
- governed lifecycle, stage definitions, approval playbooks, handoff contracts, and re-entry rules become explicit build artifacts

Implementation style:
- docs/config first
- runtime remains minimally coupled until lifecycle assets are stable
- start introducing workflow-aware verification after the asset set is complete

### `v5c`

Focus:
- policy/config and context pipeline

Primary outcome:
- static policy manifest, runtime resolver contract, context contracts, boundary panels, trace summaries, and operator-facing runtime views become explicit assets

Implementation style:
- docs/config first
- runtime integration happens after the policy/context surfaces are stable and testable

## Build Order

Recommended order:

1. `v5a` asset creation
2. `v5a` synthetic e2e and adversarial evaluator pass
3. `v5b` asset creation
4. `v5b` synthetic e2e and adversarial evaluator pass
5. `v5c` asset creation
6. `v5c` synthetic e2e and adversarial evaluator pass
7. only then: incremental runtime wiring by slice

## Minimal First Implementation Strategy

The first implementation of each slice should stay narrow.

That means:
- create the artifacts
- make their contracts explicit
- validate structure and coherence
- avoid premature runtime coupling

The goal of the first pass is:
- stable governed assets
- stable presentation
- stable contracts

Not:
- fully dynamic runtime behavior on day one

## V5A Build Tasks

### Docs/config tasks

- create `governance/prompts/` asset files
- create `governance/overlays/` asset files
- create `governance/roles/` asset files
- create `governance/controls/` asset files
- create `governance/policy-packs/` asset files
- create `governance/templates/` asset files
- add a small index/home file for each governance subfolder

### Validation tasks

- verify all required fields exist
- verify naming rules
- verify role/control separation
- verify version/status metadata
- verify linked asset references are not broken

### Synthetic e2e

Use a small synthetic governed case to test:
- governance prompt selection
- overlay linkage
- role-card linkage
- policy-pack linkage
- template-card linkage

### Adversarial evaluator focus

- prompt drift
- role/control mixing
- missing version/status
- broken linked assets
- unreadable summary-first layout

## V5B Build Tasks

### Docs/config tasks

- create lifecycle map asset
- create stage definition assets
- create approval playbook assets
- create handoff summary assets
- create exception/re-entry rule assets

### Validation tasks

- verify every stage has inputs, outputs, next stage, and failure path
- verify approval playbooks include owner, evidence, and escalation
- verify handoff summaries always specify next owner and next action
- verify exception rules specify re-entry stage and owner

### Synthetic e2e

Use a small synthetic decision flow to test:
- lifecycle coverage from intake to revisit
- stage-to-stage artifact handoff
- approval gate behavior in documentation form
- exception re-entry behavior

### Adversarial evaluator focus

- missing next-stage logic
- hidden approval owner
- unclear failure path
- vague handoff summaries
- workflow artifacts that read like prose instead of operations

## V5C Build Tasks

### Docs/config tasks

- create control tower view asset
- create governed run factsheet asset
- create boundary and enforcement panel assets
- create policy resolver record assets
- create context contract assets
- create runtime trace summary assets

### Validation tasks

- verify active policy/config state is visible
- verify approval posture is visible
- verify restrictions are visible
- verify context boundaries are explicit
- verify trace summaries show approvals, controls, and adjudication path

### Synthetic e2e

Use a small synthetic governed run to test:
- policy/config selection documentation
- context boundary representation
- runtime restriction representation
- factsheet completeness
- trace summary completeness

### Adversarial evaluator focus

- hidden restriction logic
- hidden approval state
- weak context boundary definition
- missing triggered-threshold record
- runtime artifact that is too dense to scan

## Runtime Wiring Strategy After Asset Stabilization

After the asset layer is stable:

### `v5a` runtime wiring

- make the runtime load governance prompt and overlay assets explicitly
- bind specialist roles and templates to governed files instead of implicit logic

### `v5b` runtime wiring

- make stage definitions and handoff contracts part of execution flow
- make approval playbooks inform gating decisions

### `v5c` runtime wiring

- make policy manifest and runtime resolver active in execution
- make context contracts and boundary panels reflect actual runtime behavior
- make trace summaries reflect actual runtime decisions

## Release Bar Per Slice

Each slice should not be called complete until:
- required assets exist
- contracts are respected
- synthetic e2e passes
- adversarial evaluator cases pass
- docs/readability are reviewed
- change is reflected in status and release docs

## Definition Of Success

This plan is good enough when it provides:
- a clean build order
- a minimal-first implementation strategy
- per-slice task groupings
- per-slice synthetic e2e expectations
- per-slice adversarial evaluator expectations
- a clear handoff from planning into build execution
