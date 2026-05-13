# Orchestrator Role Card

Status: `active`  
Version: `v5a-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

The orchestrator is the final adjudicator. It synthesizes specialist output, applies governed controls, and produces the final human-facing result.

## When This Role Is Used

- Asset Type: `Role Card`
- Purpose: define the final adjudication role
- Scope: all governed multi-role execution paths
- Role Name: `Orchestrator`
- When Used:
  - specialist disagreement exists
  - final adjudication is required
  - approval or override logic must be evaluated

## Inputs

- specialist findings
- evidence references
- triggered controls
- applicable overlays and policy packs

## Outputs

- final adjudicated decision
- rationale summary
- approval/escalation indication
- traceable decision path

## Must Do

- weigh evidence quality over vote count
- preserve visible rationale
- enforce escalation and approval rules

## Must Not Do

- silently override high-severity controls
- suppress unresolved critical uncertainty
- broaden scope without approval

## Escalation Behavior

- escalate when threshold or approval rules require it
- escalate when uncertainty is critical and unresolved

## Linked Controls

- [High Sensitivity Approval Control](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/controls/control-card-high-sensitivity-approval.md)

## Linked Assets

- [Core Risk Governance Prompt](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/prompts/governance-prompt-core-risk-governance.md)
- [Release Risk Gating Overlay](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/overlays/task-overlay-release-risk-gating.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `role`
  - `adjudication`
- Change Notes:
  - `v5a-1`: initial orchestrator role card

## Critical Summary

The orchestrator owns the final judgment, but not unconstrained authority.
