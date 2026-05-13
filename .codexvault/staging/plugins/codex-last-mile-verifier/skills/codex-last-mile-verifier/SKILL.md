---
name: "codex-last-mile-verifier"
description: "Use when the user wants a real-runtime verification workflow for a Codex plugin or skill, including discovery, installability, invocation smoke tests, reusable evidence, or pass/fail reporting."
---

# Codex Last-Mile Verifier

Codex Last-Mile Verifier standardizes the final live verification step for Codex plugins and skills.

Use it when the user wants:
- live Codex discovery verification
- real install flow verification
- post-install invocation smoke testing
- a reusable pass/fail checklist and evidence bundle
- a final verification report with issues and recommended fixes

## Core contract

- V1 is a guided live-verification workflow, not a fake runtime emulator.
- Do not claim discovery, installation, or invocation passed unless they were actually observed in the real Codex runtime.
- Separate what can be proven locally from what must be confirmed in the live UI/runtime.
- Be explicit when a step is blocked by missing access, disabled workspace controls, or unavailable UI tooling.
- Prefer reusable evidence: screenshots, notes, exact prompts, timestamps, and observed outcomes.

## Default workflow

1. Confirm the target extension details:
   - target type: `plugin` or `skill`
   - target name
   - local path
   - expected manifest or skill entrypoint
   - expected invocation method
   - expected display name
   - expected short description
2. Create a run with `scripts/New-CodexLastMileRun.ps1`.
3. Validate the run record with `scripts/Test-CodexLastMileRunRecord.ps1`.
4. Record preflight notes:
   - whether the local path exists
   - whether the manifest or skill entrypoint exists
   - any assumptions about workspace controls or plan limitations
5. Guide or perform the live verification steps in order:
   - discovery surface visibility
   - display name correctness
   - description correctness
   - install action availability
   - install completion
   - post-install invocation availability
   - smoke-test invocation behavior
6. After each step, record status with `scripts/Set-CodexLastMileStepStatus.ps1`.
7. Save screenshots or notes under the run `attachments/` directory when available.
8. Update the registry with `scripts/Update-CodexLastMileRegistry.ps1`.
9. Return a concise verification summary:
   - overall pass/fail
   - step results
   - evidence captured
   - issues found
   - recommended fixes

## Step status rules

- `pass`: the expected behavior was directly observed
- `fail`: the expected behavior was directly observed to be wrong or missing
- `blocked`: the step could not be completed because of environment or access constraints
- `not-run`: the step has not been attempted yet

Do not collapse `blocked` into `fail` unless the blocker itself is the product issue under test.

## Evidence rules

- Prefer short factual notes over long prose.
- Include the exact smoke-test prompt when invocation is tested.
- If screenshots exist, note their filenames in the run record.
- If browser or UI automation is unavailable, document the manual observation path clearly.
- If the user supplies screenshots later, attach them to the existing run instead of inventing a new one.

## Report style

The final report should be easy to scan:
- overall result first
- step-by-step pass/fail/blocked table next
- issues and recommended fixes after that
- assumptions and gaps last

Keep the wording operational, not promotional.

## Failure behavior

- If required intake is missing, gather the minimum missing fields before creating the run.
- If the runtime cannot be accessed, produce a blocked report rather than pretending to complete the flow.
- If the local package is inconsistent with the expected metadata, log that as a preflight issue before live testing.
- If smoke testing reveals unexpected behavior, capture the exact prompt and observed result.
