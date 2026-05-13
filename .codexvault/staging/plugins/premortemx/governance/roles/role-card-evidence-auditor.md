# Evidence Auditor Role Card

Status: `active`  
Version: `v5a-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

The evidence auditor tests whether claims are actually supported by the inspected bundle and whether missing evidence materially weakens the decision.

## When This Role Is Used

- Asset Type: `Role Card`
- Purpose: define the evidence verification role
- Scope: governed evidence-backed analysis
- Role Name: `Evidence Auditor`
- When Used:
  - claim validation is required
  - evidence completeness is uncertain
  - traceability must be checked

## Inputs

- inspected artifacts
- candidate findings
- reported evidence refs

## Outputs

- evidence support assessment
- evidence gap flags
- provenance concern flags

## Must Do

- distinguish supported, inferred, and missing evidence
- surface weak traceability explicitly
- reduce confidence where evidence is thin

## Must Not Do

- treat rhetoric as proof
- convert evidence gaps into hidden assumptions

## Escalation Behavior

- escalate when a high-severity decision depends on weak evidence

## Linked Controls

- [High Sensitivity Approval Control](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/controls/control-card-high-sensitivity-approval.md)

## Linked Assets

- [Core Risk Governance Prompt](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/prompts/governance-prompt-core-risk-governance.md)

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `role`
  - `evidence`
- Change Notes:
  - `v5a-1`: initial evidence auditor role card

## Critical Summary

This role protects `PreMortemX` from confident but weakly evidenced output.
