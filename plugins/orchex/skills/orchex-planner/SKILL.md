---
name: "orchex-planner"
description: "Use during the planning stage of an Orchex-governed run to produce verifiable subtasks, dependencies, and ownership."
---

# Orchex Planner

Use this skill only for the planning stage.

## Responsibilities

- Convert the user task into a concrete implementation plan
- Break complex work into bounded subtasks
- Note dependencies and validation checkpoints
- Record explicit file ownership if multi-agent work is planned

## Output requirements

Write or update `plan.md` with:

- run ID
- goal
- assumptions
- subtasks
- dependencies
- risks
- acceptance checkpoints

Update `task-ledger.md` with run ID, current stage, owner, planned subtasks, and explicit ownership lines for any multi-agent file scope.

## Rules

- Do not implement code in this stage
- Do not skip task decomposition for complex work
- If the task is truly atomic, state why
- Keep subtasks verifiable and small enough to monitor
