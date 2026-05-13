# Core Release Risk Lifecycle Map

Status: `active`  
Version: `v5b-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

Visible governed lifecycle for release-risk work. It starts at intake, moves through assess and deliberate, gates high-sensitivity outcomes through approval, then records monitoring and re-entry paths instead of hiding follow-up as implicit logic.

## Lifecycle Rail

- Asset Type: `Lifecycle Map`
- Purpose: define the explicit end-to-end governed release-risk workflow
- Summary: one deterministic path with visible approval and re-entry handling
- Stages:
  - `Intake`
  - `Assess`
  - `Deliberate`
  - `Approve/Block`
  - `Monitor`
  - `Revisit`

## Entry Point

- Entry Point: `Intake`
- Applies To:
  - release-risk gating
  - bounded synthetic validation flows

## Terminal States

- `Pass recorded with monitor path`
- `Warn recorded with owner and follow-up`
- `Block recorded with approval evidence and revisit trigger`

## Re-entry Paths

- missing evidence returns the case to `Assess`
- approval exceptions return the case to `Deliberate`
- material follow-up findings return the case to `Revisit`

## Linked Stage Definitions

- [Intake Stage Definition](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/stages/stage-definition-intake.md)
- [Assess Stage Definition](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/stages/stage-definition-assess.md)
- [High-Sensitivity Release Decision Approval Playbook](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/approvals/approval-playbook-high-sensitivity-release-decision.md)
- [Missing Evidence Re-entry Rule](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/exceptions/exception-rule-missing-evidence-reentry.md)

## Linked Assets

- [Release Risk Gating Overlay](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/overlays/task-overlay-release-risk-gating.md)
- [Release Risk Core Policy Pack](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/policy-packs/policy-pack-release-risk-core.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `workflow`
  - `lifecycle`
  - `release-risk`
- Change Notes:
  - `v5b-1`: initial governed lifecycle map

## Critical Summary

This lifecycle map makes the release-risk path inspectable at a glance. Later stage assets should refine it, not create alternate hidden lifecycles.
