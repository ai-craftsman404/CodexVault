# Security And Privacy Review

## Scope

Codex Last-Mile Verifier is local-first and stores verification artifacts on disk. V1 does not require external APIs, connectors, or secrets.

## Reviewed areas

- secrets: none required for baseline operation
- external services: none required
- network usage: none required by scripts
- filesystem writes: confined to the plugin `runs/` and `registry/` folders
- destructive actions: none
- prompt-injection exposure: moderate when verifying untrusted extension metadata or smoke-test output; treat observations as evidence, not truth
- privacy exposure: screenshots and notes may contain workspace or extension details if the operator includes them

## Controls

- Scripts write only under the local plugin workspace.
- Verification outcomes are operator-observed, not auto-asserted.
- Evidence capture is optional and human-controlled.
- The workflow distinguishes `blocked` from `fail` to avoid false defect claims caused by admin or plan restrictions.

## Risks

- Operators may record screenshots with sensitive workspace data.
- Manual evidence notes can be inconsistent if the workflow is not followed.
- A user could overstate a pass without actually running the live steps.

## Mitigations

- Keep evidence notes factual and scoped to the tested step.
- Store screenshots only when useful and review them before sharing publicly.
- Use the generated checklist and run record as the source of truth for pass/fail decisions.
