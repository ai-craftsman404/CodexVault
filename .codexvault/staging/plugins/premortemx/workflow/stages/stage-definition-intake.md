# Intake Stage Definition

Status: `active`  
Version: `v5b-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

The intake stage creates a bounded case, validates the requested task mode, and ensures the evidence bundle is identifiable before deeper assessment begins.

## Entry Criteria

- Asset Type: `Stage Definition`
- Stage Name: `Intake`
- Purpose: ensure the case is well-framed before assessment starts
- Entry Criteria:
  - user requested a release-risk review
  - target artifact bundle or evidence set is named
  - runtime can create a governed run record

## Required Inputs

- requested task mode
- target project or artifact identifier
- initial evidence bundle reference

## Actions

- create governed case identity
- record task mode and requested scope
- reject ambiguous or missing target selection
- route a valid case to `Assess`

## Required Outputs

- bounded case scope
- evidence bundle reference
- next-stage handoff record for `Assess`

## Approval Requirement

- Approval Requirement: `none`
- intake is administrative, not adjudicative

## Failure Path

- if scope is ambiguous, pause and request clarification
- if evidence bundle is absent, move to the missing-evidence exception path

## Next Stage

- `Assess`
- Linked Playbooks:
  - none

## Linked Assets

- [Core Release Risk Lifecycle Map](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/lifecycle/lifecycle-map-core-release-risk.md)
- [Missing Evidence Re-entry Rule](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/exceptions/exception-rule-missing-evidence-reentry.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `workflow`
  - `stage`
  - `intake`
- Change Notes:
  - `v5b-1`: initial intake stage definition

## Critical Summary

The intake stage should keep poor scoping from contaminating downstream assessment. It exists to make the rest of the workflow cleaner, not heavier.
