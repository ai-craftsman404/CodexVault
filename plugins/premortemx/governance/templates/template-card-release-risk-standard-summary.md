# Release Risk Standard Summary Template

Status: `active`  
Version: `v5a-1`  
Owner: `PreMortemX Maintainers`  
Last Updated: `2026-05-09`

## Skim Summary

Governed template card for the standard human-facing release-risk summary artifact.

## Used By

- Asset Type: `Template Card`
- Purpose: define the reusable standard release-risk summary template
- Scope: human-facing release-risk reports
- Template Name: `Release Risk Standard Summary`
- Used By:
  - release-risk-gating
  - release-risk policy pack

## Variables

- `runId`
- `projectName`
- `decision`
- `confidence`
- `topConcerns`
- `evidenceRefs`
- `nextActions`

## Output Contract

- title at the top
- detailed bullet-point body
- critical summary at the bottom
- decision and confidence must be explicit
- evidence references must be present where material claims are made

## Linked Governance Assets

- [Release Risk Core Policy Pack](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/policy-packs/policy-pack-release-risk-core.md)
- [Release Risk Gating Overlay](C:/Users/georg/codex-project/Code-Plugin-Guru/plugins/premortemx/governance/overlays/task-overlay-release-risk-gating.md)

## Validation Notes

- validate required variables before use
- preserve the summary-first presentation shape

## Change And Review Notes

- Review Cadence: `per v5 slice`
- Tags:
  - `template`
  - `summary`
  - `release-risk`
- Change Notes:
  - `v5a-1`: initial release-risk standard summary template card

## Critical Summary

This template exists to keep human-facing output governed and predictable, not merely stylistically similar.
