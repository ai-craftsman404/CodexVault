# Default Release Risk Control Tower View

Status: `active`  
Version: `v5c-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

Operator-facing runtime overview for the synthetic release-risk governed run. It makes the active policy, runtime mode, approval posture, and attention queue visible without opening the underlying run artifacts first.

## Active Policy Profile

- Asset Type: `Control Tower View`
- Purpose: show the active runtime-governance state for the current synthetic release-risk surface
- Active Policy Profile: `release-risk-core`

## Runtime Mode

- Runtime Mode: `python-first local runtime`
- environment: `local synthetic validation`

## Approval Posture

- medium-risk decisions remain bounded by human-governed `Tier B` approvals
- scope-broadening cases escalate beyond the current synthetic path

## Open Breaches And Exceptions

- no active breaches
- no active exceptions
- one monitored synthetic case is available for inspection

## Recent Adjudications

- `pmx-synthetic-release-v5c-001`: `Warn`

## Attention Queue

- verify the monitored owner follow-up remains assigned
- confirm the evidence gap note stays visible in downstream artifacts

## Linked Assets

- [Release Risk Governed Run Factsheet](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/factsheets/governed-run-factsheet-release-risk-synthetic.md)
- [Release Risk Policy Resolver Record](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/policies/policy-resolver-record-release-risk-synthetic.md)
- [Release Risk Runtime Trace Summary](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/traces/runtime-trace-summary-release-risk-synthetic.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `runtime`
  - `dashboard`
  - `control-tower`
- Change Notes:
  - `v5c-1`: initial synthetic control tower view

## Critical Summary

This view should let an operator answer “what policy was active, what happened, and what still needs attention?” in under thirty seconds.
