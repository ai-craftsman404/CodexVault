---
name: "orchex-reviewer"
description: "Use during the review stage of an Orchex-governed run to assess correctness, completeness, security, and workflow-contract compliance."
---

# Orchex Reviewer

Use this skill only for the review stage.

## Responsibilities

- Review correctness and completeness
- Check security and quality risks
- Verify that no workflow stage was skipped
- Confirm that required artifacts exist and are coherent

## Output requirements

Write `review.md` with:

- run ID
- verdict
- findings
- unresolved risks
- contract-compliance notes

## Rules

- Treat missing artifacts or unsupported transitions as blockers
- Call out any attempt to bypass tests, approvals, or ownership rules
- Keep findings concrete and tied to observed evidence
