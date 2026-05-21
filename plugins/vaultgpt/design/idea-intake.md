# VaultGPT Idea Intake

## Summary

- Working name: VaultGPT
- One-line description: Free Codex-native replacement for paid ChatGPT power extensions, with local-first vaulting, browser-assisted capture, search, organization, prompt workflows, privacy review, and auditability.
- Target user: ChatGPT power users currently using or considering third-party browser extensions such as Superpower ChatGPT, ChatGPT Toolbox, AIPRM, Sider, Monica, Merlin, or similar tools.
- User problem: Users want paid-extension power features but do not want to trust opaque third-party browser extensions with their AI history, browser context, and private ChatGPT sessions.
- Desired outcome: Let users replace paid ChatGPT extensions with a free, Codex-native, local-first plugin that offers cancellation-worthy features and visible governance.

## Expected Codex Behavior

- Use Codex Chrome selected-chat capture for visible, user-approved capture from signed-in ChatGPT.
- Maintain a local VaultGPT archive with unlimited folders, tags, pins, prompts, and search.
- Provide bulk export/backup to Markdown, JSON, and ZIP.
- Provide prompt vault workflows with variables and simple chains.
- Run privacy review before capture, indexing, or export.
- Produce audit logs and provenance manifests for sensitive or bulk operations.
- Use subagents/agent-team review only when it adds trust or value.

## Scope

### MVP Capabilities

- Full-text local search across captured/imported chat content.
- Unlimited folders, subfolders, tags, and pins.
- Bulk export and backup.
- Bulk move, archive, delete, and tag with dry-run, undo, and confirmation.
- Prompt vault with saved prompts and variables.
- Simple saved prompt chains.
- Codex Chrome selected-chat capture with explicit approval.
- Official ChatGPT export import as reliable fallback and batch source.
- Privacy review before capture, indexing, or export.
- Audit log and provenance manifest.

### Out Of Scope For MVP

- Full unattended ChatGPT account crawl.
- Always-on hidden browser scraping.
- Cloud sync.
- Prompt marketplace.
- Multi-model subscription gateway.
- Team admin/SSO.
- Media/audio gallery.
- Usage analytics.
- Semantic search and knowledge graph.

## Dependencies

- Codex plugin packaging.
- Codex skills.
- Local scripts for deterministic vault/index/export operations.
- Codex Chrome extension for selected-chat capture workflows.
- No mandatory external API or cloud service for MVP.

## Public Positioning

- GitHub repository name: vaultgpt
- Display name: VaultGPT
- Short description: Free ChatGPT power-extension features in a local-first Codex plugin.
- Business pitch: VaultGPT gives ChatGPT power-extension features for free, without forcing users to trust a third-party browser extension with their AI history.

## Open Questions

- Exact Codex Chrome extension capture interface and testability.
- Whether MVP should support PDF/HTML export in addition to Markdown/JSON/ZIP.
- Whether prompt chains should execute or only render structured steps in MVP.
- Exact vault schema and search index implementation.

