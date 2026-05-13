# Missing Evidence Re-entry Rule

Status: `active`  
Version: `v5b-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

This rule defines what happens when a case cannot be assessed cleanly because the required evidence bundle is materially incomplete.

## Trigger

- Asset Type: `Exception/Re-entry Rule`
- Purpose: define re-entry behavior for materially incomplete evidence
- Trigger:
  - required evidence bundle is absent, stale, or too incomplete to support a disciplined assessment

## Severity

- Severity: `medium-high`
- the case may remain live, but the confidence posture must degrade

## Re-entry Stage

- Re-entry Stage: `Assess`

## Required Owner

- Required Owner: `Human requester with orchestrator follow-up`

## Expected Follow-up

- supply the missing evidence class
- confirm the intended target scope if the gap changes case framing
- rerun assessment after the evidence bundle is materially improved

## Temporary Mitigation

- return a bounded partial result only if the missing evidence is called out explicitly
- do not silently upgrade confidence or completeness

## Linked Assets

- [Core Release Risk Lifecycle Map](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/lifecycle/lifecycle-map-core-release-risk.md)
- [Assess Stage Definition](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/stages/stage-definition-assess.md)
- [High-Sensitivity Release Decision Approval Playbook](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/workflow/approvals/approval-playbook-high-sensitivity-release-decision.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `workflow`
  - `exception`
  - `reentry`
- Change Notes:
  - `v5b-1`: initial missing-evidence re-entry rule

## Critical Summary

This rule prevents false decisiveness under weak evidence. Missing evidence should reopen the workflow explicitly instead of being absorbed into vague cautionary prose.
