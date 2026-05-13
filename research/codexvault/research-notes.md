# Research Notes

## Plugin

- Working name: CodexVault
- Research date: 2026-05-13
- Researcher: Codex

## Official Sources Checked

- OpenAI Codex docs landing page and related Codex pages on platform.openai.com, checked 2026-05-13
- OpenAI Docs MCP page on platform.openai.com, checked 2026-05-13
- OpenAI codex cloud / local shell / shell pages on platform.openai.com, checked 2026-05-13
- OpenAI model pages for current Codex-oriented models, checked 2026-05-13

## Ecosystem Scan

- Similar OpenAI curated plugins: none confirmed yet
- Similar GitHub repositories: none confirmed yet
- Similar MCP servers: none required for v1
- Similar agent skills: workspace discovery, validation, recovery workflows, and persona-driven rehearsal harnesses are the closest analogs

## Differentiation

- What exists already:
  - Generic backup and archive tools.
  - Environment bootstrap scripts and restore guides.
  - Agent workflows that can inspect code and run shell commands.
- Gap or opportunity:
  - There is room for a Codex-native plugin that records enough structured environment state to make workspace reconstruction safer and more deterministic than a plain file export.
- Proposed differentiator:
  - Treat the workspace as a recoverable operating environment, not a folder to compress.
  - Combine manifesting, integrity checks, and restore validation into one guided flow.
  - Add persona-based agent simulation so Codex can rehearse recovery and expose failure modes before destructive actions run.
- Why users would choose this plugin:
  - It can reduce rebuild time and restore uncertainty while keeping humans in control of destructive or cross-machine actions.

## Technical Findings

- Required APIs: none for baseline v1
- Required CLIs or runtimes:
  - Codex plugin packaging/runtime support
  - Archive tooling and local validation scripts
- Authentication model:
  - None required for baseline local use
  - Optional local key for encrypted snapshots if added later
- Platform constraints:
  - Cross-platform behavior is feasible only if the plugin scope stays at workspace-level discovery and portable artifact generation.
  - OS-level scheduling and deep system integration should be treated as optional or phase-2 additions.
  - Full deterministic recovery cannot be promised for external services, local secrets, or host-specific software installed outside the workspace boundary.
- Known limitations:
  - Snapshotting can only be deterministic to the extent that the discovered environment is enumerable and reproducible.
  - MCP topology and local tool availability can drift between capture and restore.
  - Agent-team simulations improve diagnosis but do not make a non-deterministic restore deterministic.

## Assumptions

| Assumption | Source | Date Checked | Confidence | Recheck Trigger |
| --- | --- | --- | --- | --- |
| Codex plugin guidance still favors skill-first packaging with optional scripts and integrations | Official OpenAI docs and plugin factory guidance | 2026-05-13 | High | Recheck before build freeze |
| A local-first plugin can meaningfully improve restore reliability without requiring cloud services | PRD scope and current plugin guidance | 2026-05-13 | High | Recheck if cloud sync or team features are introduced |
| Workspace reconstruction is a tractable problem when limited to normalized manifests, integrity checks, and guided restoration | PRD and technical scope review | 2026-05-13 | Medium | Recheck after design spec and test matrix |
| Deep host-level backup is too broad for v1 and should be explicitly excluded | PRD risk review | 2026-05-13 | High | Recheck if user wants host recovery or system imaging |
| Persona-based agent orchestration can be used safely if destructive actions remain human-gated | PRD update and Codex agent-team intent | 2026-05-13 | High | Recheck if auto-execution or autonomous repair is proposed |

## Recommendation

- Proceed, defer, or reject: proceed
- Rationale:
  - The idea is useful and differentiated, but only if v1 stays at workspace-level resilience and does not expand into full host backup or universal deterministic recovery.
- Required follow-up:
  - Freeze the v1 boundary around workspace discovery, manifesting, snapshot integrity, and guided restore.
  - Define what is explicitly excluded from the restore guarantee.
  - Define the agent persona roster and the exact non-destructive simulation boundaries.
