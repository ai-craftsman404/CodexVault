# Release Risk Policy Resolver Record

Status: `active`  
Version: `v5c-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

This record shows how the runtime selected its policy, model posture, controls, and feature flags for the synthetic release-risk governed run.

## Task

- Asset Type: `Policy Resolver Record`
- Purpose: show how runtime policy and config selection was resolved
- Task: `release-risk gating`

## Selected Policy Pack

- Selected Policy Pack: `release-risk-core`

## Selected Model And Runtime

- Selected Model: `python-first local governed runtime`
- Selected Runtime: `python`

## Enabled Controls

- high-sensitivity approval control
- evidence-discipline control
- no-silent-broadening control

## Disabled Controls

- cloud-advisory specialist path
- calibration-driven threshold mutation

## Feature Flags Used

- `governanceAssets=true`
- `workflowAssets=true`
- `runtimeAssetPreview=true`

## Selection Rationale

- the task is a bounded local release-risk assessment
- the current slice prioritizes explicit local governance surfaces
- optional advisory paths remain off in the synthetic validation posture

## Linked Assets

- [Release Risk Core Policy Pack](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/policy-packs/policy-pack-release-risk-core.md)
- [Release Risk Boundary And Enforcement Panel](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/policies/boundary-enforcement-panel-release-risk-synthetic.md)
- [Default Release Risk Control Tower View](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/runtime/dashboards/control-tower-view-default-release-risk.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `runtime`
  - `policy-resolver`
  - `release-risk`
- Change Notes:
  - `v5c-1`: initial synthetic policy resolver record

## Critical Summary

This record should make policy/config selection explainable instead of magical. If a reader cannot see why the runtime chose its posture, the record is too thin.
