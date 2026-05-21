# VaultGPT Research Notes

## Plugin

- Working name: VaultGPT
- Research date: 2026-05-21
- Researcher: Codex with agent-panel research branches

## Official Sources To Recheck Before Build

- OpenAI Codex plugin docs
- OpenAI Codex build plugins guide
- OpenAI Codex skills docs
- OpenAI Codex Chrome extension docs
- OpenAI Codex browser docs
- OpenAI Codex approvals and security docs
- Agent Skills standard

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

