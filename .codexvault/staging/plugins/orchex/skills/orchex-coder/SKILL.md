---
name: "orchex-coder"
description: "Use during the build stage of an Orchex-governed run to implement the approved plan under TDD-first and artifact-logging rules."
---

# Orchex Coder

Use this skill only for the build stage.

## Responsibilities

- Implement the approved plan
- Prefer TDD where feasible
- Keep changes bounded to the planned scope
- Record key decisions in `build-log.md`

## TDD rules

- Add or update a failing test before implementation when feasible
- Record the failing condition in `build-log.md`
- After implementation, rerun the relevant tests and record the outcome

If TDD is not feasible, explain why in `build-log.md`.

Include `Run ID: <value>` in `build-log.md`.

## Rules

- Do not silently replan
- If blocked, create `replan-request.md` and stop for approval
- Do not claim tests passed without handing off to the test stage
- Keep ownership boundaries intact in any multi-agent run
