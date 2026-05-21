# VaultGPT Research Notes

## Plugin

- Working name: VaultGPT
- Research date: 2026-05-21
- Researcher: Codex with agent-panel research branches

## Official Sources Checked

- OpenAI Codex build plugins guide, checked 2026-05-21: https://developers.openai.com/codex/plugins/build
- OpenAI Codex skills docs, checked 2026-05-21: https://developers.openai.com/codex/skills
- OpenAI Codex Chrome extension docs, checked 2026-05-21: https://developers.openai.com/codex/app/chrome-extension
- OpenAI Codex in-app browser docs, checked 2026-05-21: https://developers.openai.com/codex/app/browser
- OpenAI Codex approvals and security docs, checked 2026-05-21: https://developers.openai.com/codex/agent-approvals-security
- OpenAI Codex subagents docs, checked 2026-05-21: https://developers.openai.com/codex/subagents

## Market Sources Reviewed In Chat

- AI Toolbox / ChatGPT Toolbox pricing and feature pages
- Superpower ChatGPT website and Chrome Web Store listing
- AIPRM pricing and prompt-management documentation
- Sider, Monica, Merlin, MaxAI, and ChatHub public pricing/feature pages
- Reddit/user-comment signals around chat search, folders, export, and prompt workflows

## Key Findings

- Cancellation-worthy paid features cluster around workflow and ownership, not generic AI.
- Highest-value targets are full-text search, unlimited organization, bulk export/backup, bulk actions, prompt vaults, variables, prompt chains, and context/capture workflows.
- Privacy and trust are switch drivers, especially for users wary of high-privilege extensions.
- Codex Chrome selected-chat capture is the correct novelty wedge, but should be constrained and user-approved.
- Official ChatGPT export import remains the reliable batch/fallback ingestion path.
- Official Codex plugin docs support packaging a stable reusable workflow as a plugin when distribution, team sharing, integrations, or stable packaging matter.
- Official skills docs support a skill-first design: skills are reusable workflow authoring units, while plugins are the installable distribution unit.
- Official Chrome extension docs confirm Chrome is the right Codex surface for signed-in browser state, but it requires website approvals and carries broad Chrome permissions.
- Official in-app browser docs confirm it is not suitable for signed-in ChatGPT capture because it does not support authentication flows, regular browser profiles, cookies, extensions, or existing tabs.
- Official approvals/security docs reinforce the need for sandboxing, approvals, and network controls around side-effecting or sensitive operations.
- Official subagents docs support parallel specialized agents, but only when explicitly requested; subagents add token cost and should be used selectively.

## Differentiation

- Free paid-extension feature parity.
- Reduced reliance on opaque third-party extensions.
- Codex-native plugin packaging.
- Local-first vault and index.
- Privacy review and audit/provenance logs.
- Progressive visible agent-team governance.
- Future-compatible skill/script packaging and versioned schemas.

## Assumptions

| Assumption | Confidence | Recheck Trigger |
| --- | --- | --- |
| Paid extension users value full-text search and unlimited organization enough to switch | High | Before MVP scope freeze |
| Codex Chrome selected-chat capture can support a constrained MVP workflow | Medium | Before implementation |
| Full unattended account crawl is too fragile for MVP | High | If official APIs/capabilities change |
| Skill plus scripts is sufficient for MVP | High | If Chrome capture requires a stronger integration model |

## Design Impact

- Keep VaultGPT packaged as an installable plugin, not only loose notes or a standalone script.
- Build the core workflow as a skill plus local scripts.
- Treat Codex Chrome selected-chat capture as a constrained, explicit, user-approved workflow.
- Keep in-app browser out of the signed-in ChatGPT capture path.
- Keep official ChatGPT export import as reliable fallback/batch source.
- Keep subagent/agent-team usage progressive and explicit, not automatic for every action.
