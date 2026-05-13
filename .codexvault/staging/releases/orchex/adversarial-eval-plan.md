# Adversarial Evaluation Plan

## Purpose

Track adversarial behaviors Orchex should resist before release readiness.

## Covered by current script tests

- stage skipping
- fake passing test report without evidence
- missing approval when completion requires it
- placeholder artifact bypass
- unsupported stack fallback
- missing run metadata
- stale artifact reuse via run ID mismatch
- ledger stage mismatch
- direct ownership overlap detection

## Covered by synthetic E2E tests

- node repo workflow path
- python repo workflow path
- unsupported-stack fail-closed behavior
- end-to-end run ID tamper rejection
- end-to-end ownership-conflict rejection

## Covered by realistic mini-repo E2E tests

- realistic node repo workflow path
- realistic python repo workflow path

## Covered by prompt-injection E2E tests

- repo instructions that attempt to skip tests or review still fail local gates

## Still pending

- direct role-skill bypass without orchestrator state
- replan without preserved history
- retroactive plan rewrite
- approval spoofing
- multi-agent ownership overlap
- prompt-injection attempts from repo content
- resume-after-failure tampering
- summary forgery
- concurrent-run artifact mixing
- runtime wrong-trigger behavior

## Release gate

Orchex should not be treated as release-ready until each pending item is either:

- covered by an automated test,
- enforced by implementation, or
- explicitly deferred with a documented rationale.
