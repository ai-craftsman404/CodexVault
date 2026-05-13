# Agent Team Best Practices

## Purpose

Use Codex sub-agents or cloud agents to accelerate plugin development when work can be split into independent, bounded tasks.

Agent teams are optional. They should improve throughput without weakening architecture control or creating integration risk.

## Good Uses

- Researching current docs and ecosystem examples.
- Comparing similar plugins, skills, MCP servers, or GitHub repos.
- Reviewing architecture and skill boundaries.
- Implementing isolated files or folders.
- Running tests while development continues.
- Performing security, privacy, and release-readiness reviews.
- Running longer background tasks through cloud agents.

## Poor Uses

- Vague exploration with no concrete output.
- Delegating the core architecture decision before the main thread understands the problem.
- Assigning multiple agents to the same files.
- Splitting a small plugin where coordination overhead exceeds benefit.
- Letting agents make release decisions without main-thread review.
- Sending vague cloud-agent tasks without a handoff artifact.

## Standard Roles

- Research Scout: source-backed research and differentiation.
- Design Reviewer: architecture and scope critique.
- Build Worker: bounded implementation with explicit file ownership.
- Test Runner: verification, trigger tests, install checks, script checks.
- Security Reviewer: secrets, permissions, network, prompt-injection, data leakage.
- Release Reviewer: README, examples, changelog, license, public positioning.

## Coordination Rules

- Main thread owns final architecture.
- Each delegated task must be self-contained.
- Code-editing agents need explicit write ownership.
- Review agents should be read-only unless assigned documentation fixes.
- Do not duplicate work between agents and the main thread.
- Integrate outputs deliberately and rerun relevant checks after integration.
- Match each sub-agent model to task complexity and risk.
- Prefer lighter models for narrow research, checklist, and formatting tasks.
- Use stronger models for security review, unclear architecture, complex integration, and final release review.

## Cloud Agent Use

Cloud agents are useful when work can proceed independently in the background:

- large research sweeps
- ecosystem comparisons
- bounded implementation tasks
- test and verification passes
- release-readiness review
- security/privacy review

Cloud-agent tasks need a precise handoff:

- plugin name and repo path
- current lifecycle stage
- relevant templates or specs
- expected output format
- file ownership if edits are allowed
- verification expected

The main local session remains responsible for integrating results, resolving conflicts, and approving release.
