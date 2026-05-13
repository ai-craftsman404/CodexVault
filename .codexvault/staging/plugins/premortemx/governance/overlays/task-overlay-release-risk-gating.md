# Release Risk Gating Overlay

Status: `active`  
Version: `v5a-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

Task overlay for release-risk gating. It narrows the base governance prompt to ship/no-ship decision support, release evidence inspection, and explicit release-blocking logic.

## Parent Prompt

- Asset Type: `Task Overlay`
- Purpose: specialize the base governance prompt for release-risk gating
- Scope: bounded release-decision assessments
- Parent Prompt:
  - [Core Risk Governance Prompt](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/prompts/governance-prompt-core-risk-governance.md)

## Task Mode

- `release-risk-gating`

## Extra Rules

- always produce a clear `Pass`, `Warn`, or `Block`
- prioritize release evidence, test signals, and operational readiness
- capture blocker logic explicitly

## Explicit Exclusions

- do not drift into generic architecture brainstorming unless routed there
- do not treat vague best-practice concerns as blockers without evidence

## Evidence Expectations

- release plan or change summary
- relevant implementation context
- test/build evidence where available
- operational readiness signals where relevant

## Escalation Behavior

- escalate when credible high-severity release risk exists
- escalate when evidence completeness is too low for a safe pass
- require explicit human ownership for block overrides

## Linked Controls

- [High Sensitivity Approval Control](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/controls/control-card-high-sensitivity-approval.md)

## Linked Assets

- [Release Risk Core Policy Pack](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/policy-packs/policy-pack-release-risk-core.md)
- [Release Risk Standard Summary Template](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/templates/template-card-release-risk-standard-summary.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `overlay`
  - `release-risk`
- Change Notes:
  - `v5a-1`: initial release-risk overlay asset

## Critical Summary

This overlay is the minimal governed specialization for release-risk gating and should remain narrower than the base prompt.
