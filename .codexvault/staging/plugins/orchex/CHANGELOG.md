# Changelog

## 0.1.0 - 2026-04-30

- Initial Orchex MVP release candidate.
- Added deterministic `plan -> build -> test -> review` workflow governance.
- Added role skills for orchestrator, planner, coder, tester, and reviewer stages.
- Added script-backed validation for artifacts, stage transitions, run integrity, and ownership conflicts.
- Added synthetic and realistic mini-repo E2E coverage.

### Known limitations

- Live Codex UI/runtime discovery and trigger behavior are not yet verified from this workspace thread.
- Prompt-injection resistance is only partially enforced through local gates and documented workflow rules.
- V1 uses file-based approvals and run metadata rather than an MCP-backed coordinator.
