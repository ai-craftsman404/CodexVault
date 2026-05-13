# Assess Stage Definition

Status: `active`  
Version: `v5b-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

The assess stage turns a bounded case into a structured evidence-backed risk picture, with explicit outputs ready for deliberation or exception handling.

## Entry Criteria

- Asset Type: `Stage Definition`
- Stage Name: `Assess`
- Purpose: inspect the evidence bundle and produce a structured risk picture
- Entry Criteria:
  - bounded case exists
  - evidence bundle is named and reachable
  - task mode is resolved

## Required Inputs

- bounded case scope
- evidence bundle reference
- active release-risk overlay and policy pack

## Actions

- inspect the available evidence bundle
- identify initial risk themes and evidence gaps
- separate severity, confidence, and completeness signals
- prepare a structured handoff for `Deliberate`

## Required Outputs

- evidence-backed initial risk picture
- evidence gap note when required
- assess-to-deliberate handoff summary

## Approval Requirement

- Approval Requirement: `none`
- the stage may recommend escalation, but does not own the final decision

## Failure Path

- if evidence is materially incomplete, trigger the missing-evidence re-entry rule
- if the target is mis-scoped, return to `Intake`

## Next Stage

- `Deliberate`
- Linked Playbooks:
  - [High-Sensitivity Release Decision Approval Playbook](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/approvals/approval-playbook-high-sensitivity-release-decision.md)

## Linked Assets

- [Core Release Risk Lifecycle Map](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/lifecycle/lifecycle-map-core-release-risk.md)
- [Assess To Deliberate Handoff Summary](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/handoffs/handoff-summary-assess-to-deliberate.md)
- [Release Risk Gating Overlay](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/overlays/task-overlay-release-risk-gating.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `workflow`
  - `stage`
  - `assess`
- Change Notes:
  - `v5b-1`: initial assess stage definition

## Critical Summary

The assess stage exists to produce a usable decision substrate. If evidence is weak, that weakness must be one of the outputs, not hidden operationally.
