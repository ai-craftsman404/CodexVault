# Plugin Idea Intake

## Summary

- Working name: orchex
- One-line description: A Codex-first workflow-governance plugin that enforces staged agent execution, required artifacts, and validation gates while allowing stack-specific implementation strategies.
- Target user: Engineers and technical teams using Codex for non-trivial implementation work who want repeatable execution without building a full orchestration platform.
- User problem: Agent-driven development is inconsistent across repos, stacks, and tasks; teams need reusable workflow discipline without rigid hand-built pipelines for every case.
- Desired outcome: Codex follows a deterministic workflow contract, logs each stage, validates outputs, and adapts implementation details safely within defined constraints.

## Expected Codex Behavior

- What should Codex do differently when this plugin is installed?
  Codex should adopt an orchestrated `plan -> build -> test -> review` workflow, emit required artifacts, track task state, decompose complex tasks, and refuse to skip validation or approval gates.
- What should Codex avoid doing?
  Codex should avoid ad hoc execution, undefined stage transitions, silent replans, skipped tests, untracked work, and overlapping multi-agent ownership.
- Example user prompts:
  - `$orchex Implement this feature using the governed workflow.`
  - `$orchex Plan, build, test, and review this bug fix with strict gates.`
  - `$orchex Run a TDD workflow for this refactor and log each stage.`

## Scope

- MVP capabilities:
  - Deterministic stage contract for `plan -> build -> test -> review`
  - Required per-stage artifacts and run summary
  - Orchestrator-led task tracking and stage status
  - Controlled replan path with justification and approval
  - Stack adapter profiles for repo-specific test/lint/build commands
  - TDD-first execution guidance
  - Adversarial evaluation scenarios in the test matrix
  - Bounded multi-agent roles with non-overlapping ownership
- Out of scope for v1:
  - Full MCP-backed orchestration runtime
  - GUI dashboard
  - Broad cross-provider portability
  - CI/CD replacement
  - Autonomous merges or releases
- Future possibilities:
  - MCP coordinator for stronger runtime enforcement
  - Security scanning role
  - Cost-aware routing
  - Rich observability UI
  - Deeper multi-agent parallelism

## Inputs and Outputs

- Inputs Codex needs:
  - Task description
  - Repository path and detected stack profile
  - Constraints, approvals, and risk limits
  - Optional human review checkpoints
- Outputs Codex should produce:
  - Structured plan artifact
  - Task ledger and stage log
  - Build/test/review artifacts
  - Replan record when applicable
  - Final run summary with gate outcomes
- Files, services, or systems involved:
  - Local repository files
  - Plugin skill instructions
  - Local validation scripts
  - Optional test framework commands present in the target repo

## Dependencies

- Skills:
  - Orchestrator skill
  - Planner skill
  - Coder skill
  - Tester skill
  - Reviewer skill
- Scripts:
  - Artifact validator
  - Stage transition validator
  - Stack profile resolver
  - Run summary generator
- MCP servers:
  - None for v1
- App connectors:
  - None for v1
- External APIs:
  - None required for v1
- Secrets or credentials:
  - None required by the plugin itself beyond whatever the target repo already needs for its own tests

## Public Positioning

- GitHub repository name: code-plugin-guru
- Display name: Dynamic Agent Workflow Governor
- Short description: Govern Codex work with deterministic stages, required artifacts, validation gates, and stack-aware execution profiles.
- Target audience: Developers and teams who want more predictable agent execution in real repositories.
- Why this should exist: Current agent usage is often either too free-form or too engine-heavy; this plugin aims for a practical middle ground centered on governance and reproducibility.

## Open Questions

- Question: Should human approval be optional globally or only mandatory for selected high-risk transitions?
- Owner: Main thread
- Resolution: Open

- Question: Should V1 multi-agent mode be enabled by default or opt-in per workflow run?
- Owner: Main thread
- Resolution: Open

- Question: What is the minimal stack profile format that stays flexible without becoming a workflow DSL?
- Owner: Main thread
- Resolution: Open
