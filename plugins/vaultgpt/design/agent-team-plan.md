# VaultGPT Agent Team Plan

## Plugin

- Plugin name: VaultGPT
- Date: 2026-05-21
- Main thread owner: Codex
- Reason for using agent team: Market research, security review, browser-capture feasibility, and test/release checks can be split safely.
- Execution mode: local sub-agent / forked session / worktree when implementation begins
- Overall complexity: high
- Default model tier: smaller models for bounded research/checklists; stronger models for architecture, security, and release review

## Workstreams

| Role | Task | Model Tier | File Ownership |
| --- | --- | --- | --- |
| Research Scout | Refresh competitor and official Codex docs | smaller/mid | read-only or design notes |
| Design Reviewer | Review MVP scope and plugin boundaries | mid/strong | read-only |
| Build Worker | Implement isolated script modules | mid | assigned module only |
| Test Runner | Run parser/index/export/trigger tests | mid | read-only unless assigned tests |
| Security Reviewer | Review prompt injection, privacy, permissions, data leakage | strong | read-only |
| Release Reviewer | Review public packaging and installability | mid/strong | read-only unless assigned docs |

## Coordination Rules

- Main thread owns final architecture and integration.
- Use worktrees/forked sessions for parallel implementation when file ownership is disjoint.
- No agent edits another agent's assigned files.
- Every agent reports changed files and verification.
- Security and release approval are never delegated as final decisions.

## Initial Parallelization Plan

- Main thread: plugin scaffold and architecture integration.
- Research Scout: official docs and competitor refresh.
- Security Reviewer: threat model and test requirements.
- Test Runner: test matrix and fixture strategy.
- Build Workers: split by import/index/export/prompt/audit only after design freeze.

