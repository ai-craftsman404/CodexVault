# Research Log

Use this log to track documentation checks and ecosystem research that affect plugin design.

| Date | Topic | Sources | Conclusion | Recheck Trigger |
| --- | --- | --- | --- | --- |
| 2026-04-30 | Documentation refresh cadence established | Project operating framework | Review official Codex/plugin/skills/security and Agent Skills documentation every four weeks by default; use bi-weekly checks during active release work. | Next scheduled refresh or before final plugin release |
| 2026-04-30 | Dynamic agent workflow governor pre-design doc check | OpenAI Academy: Plugins and skills; OpenAI blog: Introducing the Codex app; OpenAI Developers: Codex web; OpenAI Help: Using Codex with your ChatGPT plan | Current guidance supports a process-first skill model, team-shared skills, background parallel Codex work, and workspace controls for plugins. V1 should stay Codex-first, use skills for process governance, avoid external connectors in the initial release, and document local-execution assumptions clearly. | Recheck before implementation freeze or if Codex plugin/skills controls change |
| 2026-05-04 | PreMortemX ecosystem inspiration and runtime-isolation direction | `borghei/Claude-Skills` pre-mortem skill; `SuperagenticAI/metaharness`; Turso AgentFS docs and repository | PreMortemX should differentiate by combining evidence-backed pre-mortem reasoning with a lightweight harness model. AgentFS is a strong isolation/auditability reference, but should stay optional because it is beta. | Recheck before implementation if runtime isolation becomes a core dependency |
| 2026-05-04 | PreMortemX official Codex/plugin/security verification | OpenAI Academy: Plugins and skills; OpenAI Help: Using Codex with your ChatGPT plan; OpenAI Help: Codex Security; OpenAI Help: Skills in ChatGPT | Current guidance still supports a plugin package that uses skills for reusable process execution and keeps permissions/workspace controls human-governed. PreMortemX v1 remains aligned as a skill-plus-scripts local-first plugin with explicit approvals and human review. | Recheck before public release or on next documentation refresh |
| 2026-05-04 | Codex Last-Mile Verifier official Codex/plugin/skills verification | OpenAI Academy: Plugins and skills; OpenAI Help: Skills in ChatGPT; OpenAI Help: Using Codex with your ChatGPT plan | Current guidance supports packaging a reusable verification process as a plugin-bundled skill, while workspace controls and runtime UI differences justify a guided live-check workflow with explicit `blocked` outcomes instead of fake automation claims. | Recheck before public release or if Codex discovery/install surfaces change |

## Recurring Review Scope

- OpenAI Codex plugin docs
- OpenAI Codex build plugins guide
- OpenAI Codex skills docs
- OpenAI Codex security and approvals docs
- Agent Skills standard
- OpenAI Codex GitHub releases or notable changes
- relevant MCP, app connector, and marketplace changes

## Review Output

Each review should capture:

- sources checked
- date checked
- notable changes
- impact on this factory process
- recommended edits
- whether templates, `AGENTS.md`, `PROCESS.md`, or knowledge-base files need updates
