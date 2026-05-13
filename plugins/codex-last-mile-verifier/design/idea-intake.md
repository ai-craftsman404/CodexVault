# Plugin Idea Intake

## Summary

- Working name: Codex Last-Mile Verifier
- One-line description: Reusable live verification workflow for Codex plugins and skills that confirms real discovery, installation, and smoke-test invocation behavior.
- Target user: Internal Codex plugin builders, skill builders, and maintainers of many reusable Codex extensions.
- User problem: Static validation can prove package shape but not whether a real Codex runtime discovers, installs, and exposes the extension correctly.
- Desired outcome: A consistent last-mile verification process with reusable evidence and a standard pass/fail summary.

## Expected Codex Behavior

- What should Codex do differently when this plugin is installed?
  - Create a verification run for a target plugin or skill.
  - Separate local preflight checks from live runtime checks.
  - Guide the operator through discovery, install, and invocation verification in a fixed order.
  - Record notes, evidence references, issues, and fixes in reusable artifacts.
  - Produce a concise final report with a per-step outcome.
- What should Codex avoid doing?
  - Avoid pretending local validation equals runtime success.
  - Avoid claiming a pass without observed evidence.
  - Avoid publishing plugins or making product decisions for the user.
- Example user prompts:
  - "Use Codex Last-Mile Verifier to test whether this plugin is discoverable and installable."
  - "Run a live verification for this skill and give me a pass/fail report."
  - "Guide me through the final runtime smoke test for this local Codex extension."

## Scope

- MVP capabilities:
  - verification intake for plugin or skill targets
  - dated run bundles with checklist and report artifacts
  - structured status tracking for each live verification step
  - registry indexing for repeated runs
  - concise issues and recommended-fixes reporting
- Out of scope for v1:
  - fully automated Codex UI control as a hard dependency
  - fake runtime emulation
  - plugin publishing
  - portfolio dashboards or scheduled re-verification
- Future possibilities:
  - screenshot capture helpers
  - regression comparison across prior runs
  - scheduled portfolio-wide rechecks

## Inputs and Outputs

- Inputs Codex needs:
  - plugin or skill name
  - target type
  - local path
  - expected manifest or skill entrypoint
  - expected invocation method
  - expected display name
  - expected short description
- Outputs Codex should produce:
  - per-step pass/fail/blocked results
  - evidence log
  - issues-found list
  - recommended fixes
  - final summary
- Files, services, or systems involved:
  - local plugin package
  - Codex runtime or UI for the live check
  - optional screenshots supplied manually or via UI tooling

## Dependencies

- Skills:
  - Codex Last-Mile Verifier core workflow skill
- Scripts:
  - run creation
  - step status updates
  - run record validation
  - registry updates
- MCP servers:
  - none required for v1
- App connectors:
  - none required for v1
- External APIs:
  - none required for v1

## Public Positioning

- GitHub repository name: codex-last-mile-verifier
- Display name: Codex Last-Mile Verifier
- Short description: Standardize real Codex discovery, install, and smoke-test verification for plugins and skills.
- Target audience: Codex builders and maintainers who need a repeatable final runtime validation process.
- Why this should exist: Real runtime verification is the gap left by local file validation, and teams need a reusable way to close that gap consistently.
