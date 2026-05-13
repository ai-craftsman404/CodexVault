# Release Risk Governed Run Factsheet

Status: `active`  
Version: `v5c-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

Compact governed record for one synthetic release-risk run. It shows the exact run identity, active policy/config, approval events, thresholds triggered, and final adjudication in a single operational view.

## Run Identity

- Asset Type: `Governed Run Factsheet`
- Purpose: capture one governed run in a compact operator-facing form
- Run ID: `pmx-synthetic-release-v5c-001`
- Task Type: `release-risk gating`

## Scope

- Scope: synthetic release decision for a bounded feature rollout
- runtime mode: `python-first local runtime`

## Active Policy And Config

- Active Policy Version: `release-risk-core@v5c-1`
- Active Config Version: `runtime-default@v5c-1`

## Approval Events

- `Tier B` review expected for the synthetic `Warn` outcome
- no scope-broadening request was triggered

## Triggered Thresholds

- evidence completeness degraded below preferred level
- residual operational risk remained above `Pass` comfort

## Final Adjudication

- Final Adjudication: `Warn`
- monitored follow-up required before a clean unrestricted release posture can be claimed

## Linked Artifacts

- [Release Risk Policy Resolver Record](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/policies/policy-resolver-record-release-risk-synthetic.md)
- [Release Risk Boundary And Enforcement Panel](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/policies/boundary-enforcement-panel-release-risk-synthetic.md)
- [Release Risk Runtime Trace Summary](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/traces/runtime-trace-summary-release-risk-synthetic.md)

## Linked Assets

- [Default Release Risk Control Tower View](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/dashboards/control-tower-view-default-release-risk.md)
- [Assess To Deliberate Handoff Summary](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/handoffs/handoff-summary-assess-to-deliberate.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `runtime`
  - `factsheet`
  - `release-risk`
- Change Notes:
  - `v5c-1`: initial synthetic governed run factsheet

## Critical Summary

This factsheet should remain the fastest trustworthy single-run view. If an operator has to open multiple files before understanding the run state, it is not doing its job.
