# High Sensitivity Approval Control

Status: `active`  
Version: `v5a-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

Control for cases where decision sensitivity is high enough that stronger approval and escalation behavior must apply.

## Trigger

- Asset Type: `Control Card`
- Purpose: define the high-sensitivity approval control
- Scope: release-risk, architecture-validation, and calibration cases with elevated consequence
- Control Name: `High Sensitivity Approval`
- Trigger:
  - decision sensitivity high
  - unresolved critical uncertainty
  - scope broadening or stronger authority requested

## Effect

- require explicit escalation
- forbid silent widening of authority
- increase decision scrutiny before final adjudication

## Approval Tier

- `Tier C`

## Evidence Requirement

- high-severity conclusions must have explicit evidence references
- weak evidence must be surfaced as a blocker or escalated uncertainty

## Override Rule

- cannot be bypassed silently
- block overrides require named owner and rationale

## Audit Expectation

- record trigger
- record approver or escalation path
- record final disposition

## Exceptions

- no current exceptions

## Linked Assets

- [Release Risk Core Policy Pack](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/policy-packs/policy-pack-release-risk-core.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `control`
  - `approval`
  - `high-sensitivity`
- Change Notes:
  - `v5a-1`: initial high-sensitivity approval control

## Critical Summary

This control exists to make high-consequence decisions visibly governed.
