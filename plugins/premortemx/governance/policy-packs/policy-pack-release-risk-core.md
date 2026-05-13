# Release Risk Core Policy Pack

Status: `active`  
Version: `v5a-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

Core policy pack for release-risk gating. It bundles the minimal controls, governed prompt linkage, and output template needed for the first synthetic case.

## Applies To

- Asset Type: `Policy Pack`
- Purpose: group the core governed assets for release-risk gating
- Scope: bounded release-risk cases
- Pack Name: `Release Risk Core`
- Applies To:
  - release-risk-gating

## Included Controls

- [High Sensitivity Approval Control](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/controls/control-card-high-sensitivity-approval.md)

## Approval Model

- medium-risk approval remains bounded
- high-sensitivity paths escalate through the linked control

## Required Templates

- [Release Risk Standard Summary Template](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/templates/template-card-release-risk-standard-summary.md)

## Exceptions

- no current exceptions

## Linked Assets

- [Core Risk Governance Prompt](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/prompts/governance-prompt-core-risk-governance.md)
- [Release Risk Gating Overlay](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/overlays/task-overlay-release-risk-gating.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `policy-pack`
  - `release-risk`
- Change Notes:
  - `v5a-1`: initial release-risk policy pack

## Critical Summary

This pack is the smallest governed package that still expresses release-risk policy as linked assets rather than prose.
