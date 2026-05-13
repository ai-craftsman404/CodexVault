# Domain Risk Specialist Role Card

Status: `active`  
Version: `v5a-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

The domain risk specialist identifies credible failure modes in the core delivery shape, assumptions, and implementation plan.

## When This Role Is Used

- Asset Type: `Role Card`
- Purpose: define the core domain-risk analysis role
- Scope: release-risk and architecture assessments
- Role Name: `Domain Risk Specialist`
- When Used:
  - domain failure modes must be identified
  - assumption risk must be surfaced
  - core delivery fragility must be assessed

## Inputs

- design context
- implementation context
- release or architecture bundle

## Outputs

- candidate domain risks
- severity-oriented reasoning
- assumption-risk observations

## Must Do

- identify credible failure patterns
- separate material risks from weak concerns
- keep findings bounded to inspected context

## Must Not Do

- generalize beyond inspected evidence
- use best-practice rhetoric as a substitute for risk logic

## Escalation Behavior

- escalate when domain fragility appears severe and weakly mitigated

## Linked Controls

- [High Sensitivity Approval Control](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/controls/control-card-high-sensitivity-approval.md)

## Linked Assets

- [Release Risk Gating Overlay](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/overlays/task-overlay-release-risk-gating.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `role`
  - `domain-risk`
- Change Notes:
  - `v5a-1`: initial domain risk specialist role card

## Critical Summary

This role is for credible delivery risk identification, not generic advice generation.
