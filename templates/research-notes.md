# Research Notes

## Plugin

- Working name: PreMortemX
- Research date: 2026-05-04
- Researcher: Codex

## Official Sources Checked

- OpenAI Codex plugin docs: OpenAI Academy `Plugins and skills` checked on 2026-05-04
- OpenAI Codex skills docs: OpenAI Academy `Plugins and skills` checked on 2026-05-04
- OpenAI Codex security docs: OpenAI Help `Codex Security` checked on 2026-05-04
- Agent Skills standard: ChatGPT Help `Skills in ChatGPT` checked on 2026-05-04
- Other official docs:
  - OpenAI Help `Using Codex with your ChatGPT plan` checked on 2026-05-04

## Ecosystem Scan

- Similar OpenAI curated plugins: none recorded yet
- Similar GitHub repositories:
  - `borghei/Claude-Skills` pre-mortem skill
  - `SuperagenticAI/metaharness`
  - `tursodatabase/agentfs` as an optional isolation-pattern reference
- Similar MCP servers: none recorded yet
- Similar agent skills:
  - Pre-mortem facilitation and risk classification skills
- Similar commercial products: none recorded yet

## Differentiation

- What exists already:
  - Pre-mortem skills exist as facilitation or reasoning patterns.
  - Harness/optimization projects exist for improving agent support systems and execution scaffolding.
- Gap or opportunity:
  - The gap is a Codex-native plugin that turns pre-mortem reasoning into an evidence-backed, auditable, release-decision workflow rather than a workshop exercise or generic checklist.
- Proposed differentiator:
  - Combine pre-mortem reasoning with a lightweight harness model: structured evidence validation, registry-linked artifacts, adaptive guardrails, structured overrides, and later quality feedback.
- Why users would choose this plugin:
  - It offers clearer and more inspectable release-risk decisions than a plain prompt skill, while staying lighter and more usable than a full optimization platform.

## Technical Findings

- Required APIs: none required for v1
- Required CLIs or runtimes:
  - Codex skill execution environment
  - Local scripts/runtime for scoring, report generation, and registry updates
- Authentication model:
  - None required for baseline local use
  - Optional local-user-controlled secret or key source for encrypted retained artifacts
- Platform constraints:
  - V1 should assume a bounded local workspace and conservative permissions.
  - Optional AgentFS integration should remain a future or optional backend due to beta status.
  - Official OpenAI guidance still supports a plugin as a package that can combine skills and optional integrations, while skills remain the right fit for reusable process execution.
- Known limitations:
  - Secondary architecture-validation mode is defined but deferred from shipping in v1.

## Assumptions

| Assumption | Source | Date Checked | Confidence | Recheck Trigger |
| --- | --- | --- | --- | --- |
| Pre-mortem reasoning is useful but not sufficiently differentiated on its own | Ecosystem comparison and user direction | 2026-05-04 | High | Recheck during final positioning review |
| The harness concept is the likely standout differentiator for PreMortemX | User intake plus comparison to metaharness | 2026-05-04 | Medium | Recheck after official-doc review and design freeze |
| AgentFS is a strong reference for isolation and auditability, but should not be required in v1 because it is beta | Turso AgentFS docs and repository | 2026-05-04 | High | Recheck before implementation if runtime isolation becomes central |
| V1 should remain local-first with no mandatory external services | User intake decisions | 2026-05-04 | High | Recheck if future connectors or services are proposed |
| A plugin that packages a skill-first workflow with local scripts still fits current Codex plugin guidance | OpenAI Academy plugins/skills guidance plus Codex plan/help docs | 2026-05-04 | High | Recheck before public release if plugin packaging guidance changes |

## Recommendation

- Proceed, defer, or reject: proceed
- Rationale:
  - The concept is differentiated enough to justify spec work, especially through the combination of evidence-backed pre-mortem reasoning and a lightweight harness model.
- Required follow-up:
  - Finalize artifact schemas, file conventions, and release test scenarios during spec drafting.
