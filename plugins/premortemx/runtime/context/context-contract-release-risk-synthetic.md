# Release Risk Context Contract

Status: `active`  
Version: `v5c-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

This contract defines what context can flow into and across the synthetic release-risk run, how it must be transformed, and what may not be carried forward.

## Source Context Class

- Asset Type: `Context Contract`
- Purpose: define governed context flow for the synthetic release-risk path
- Source Context Class: `bounded run evidence and workflow artifacts`

## Allowed Downstream Target

- orchestrator and specialist deliberation roles
- governed run factsheet
- runtime trace summary

## Required Transformation

- convert raw inputs into structured evidence references
- summarize only after evidence traceability is preserved
- redact unneeded ambient context before carry-forward

## Prohibited Carry-forward

- unrelated prior-case narrative
- unvalidated user assertions
- hidden state from external advisory paths

## Retention Expectation

- retain only the governed run record and explicitly linked artifacts
- discard ambient context that is not promoted into the governed artifact set

## Linked Assets

- [Release Risk Boundary And Enforcement Panel](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/policies/boundary-enforcement-panel-release-risk-synthetic.md)
- [Release Risk Runtime Trace Summary](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/traces/runtime-trace-summary-release-risk-synthetic.md)
- [Role Card Orchestrator](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/roles/role-card-orchestrator.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `runtime`
  - `context`
  - `retention`
- Change Notes:
  - `v5c-1`: initial synthetic context contract

## Critical Summary

This contract should stop context sprawl from turning into silent authority creep. Only deliberately governed context should survive stage-to-stage movement.
