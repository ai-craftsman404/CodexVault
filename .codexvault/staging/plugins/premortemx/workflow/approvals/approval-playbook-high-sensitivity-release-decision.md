# High-Sensitivity Release Decision Approval Playbook

Status: `active`  
Version: `v5b-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

This playbook governs high-sensitivity release decisions where a `Warn` or `Block` outcome has material operational or permission consequences and must remain traceable.

## Applies To

- Asset Type: `Approval Playbook`
- Playbook Name: `High-Sensitivity Release Decision`
- Purpose: define how sensitive release outcomes are approved, blocked, or escalated
- Applies To:
  - release-risk cases with `Warn` or `Block` pressure
  - decisions with material operational impact

## Approval Tier

- Approval Tier: `Tier B`
- escalation to `Tier C` when broader permissions or weakened evidence posture would be required

## Decision Owner

- Decision Owner: `Human reviewer with orchestrator recommendation`
- linked stage:
  - `Approve/Block`

## Required Evidence

- inspected evidence bundle references
- structured adjudication rationale
- explicit evidence gap note when completeness is reduced
- linked ownership and next-action record

## Allowed Outcomes

- `approve pass with monitor path`
- `approve warn with owner and follow-up`
- `confirm block`
- `escalate for higher approval`

## Escalation Path

- unresolved critical uncertainty escalates to higher human review
- scope-broadening or permission-broadening escalates to `Tier C`
- conflicting evidence with high severity returns to `Deliberate`

## Audit Trail

- record decision owner
- record approval tier
- record rationale and evidence references
- record any escalation taken

## Linked Assets

- [Core Release Risk Lifecycle Map](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/lifecycle/lifecycle-map-core-release-risk.md)
- [High-Sensitivity Approval Control Card](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/controls/control-card-high-sensitivity-approval.md)
- [Release Risk Core Policy Pack](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/policy-packs/policy-pack-release-risk-core.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `workflow`
  - `approval`
  - `release-risk`
- Change Notes:
  - `v5b-1`: initial high-sensitivity approval playbook

## Critical Summary

This playbook keeps sensitive release outcomes human-governed and auditable. It should stay easy to scan even when later thresholds become more detailed.
