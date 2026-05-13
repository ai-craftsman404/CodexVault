---
name: "orchex-tester"
description: "Use during the test stage of an Orchex-governed run to execute validation commands, capture evidence, and enforce pass/fail gates."
---

# Orchex Tester

Use this skill only for the test stage.

## Responsibilities

- Run the repo-appropriate validation commands
- Capture exact evidence in `test-report.md`
- Block progression when validation fails

## Output requirements

`test-report.md` must contain:

- `Run ID: <value>`
- `RESULT: PASS` or `RESULT: FAIL`
- `EVIDENCE: ...`
- commands executed
- relevant failures or confirmation details

## Rules

- Do not waive failed tests
- Do not mark a stage complete without evidence
- If commands are unavailable, record that explicitly as a failure or blocker instead of guessing
