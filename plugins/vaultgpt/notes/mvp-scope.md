# VaultGPT MVP Scope

## MVP Principle

Choose moderate-complexity, high-value, popular workflows that map to competitor paid features and reduce reliance on unsafe third-party browser extensions.

The MVP should not be framed as a generic archive/search tool. It should be framed as a free, trusted Codex-native replacement for paid ChatGPT extension workflows.

## Recommended MVP Features

1. Full-text search across all captured/imported chat content
2. Unlimited folders, subfolders, tags, and pins
3. Bulk export and backup to Markdown, JSON, and ZIP
4. Bulk move, archive, delete, and tag with dry-run, undo, and confirmation
5. Prompt vault with saved prompts and variables
6. Simple saved prompt chains
7. Codex Chrome selected-chat capture with explicit user approval
8. Official ChatGPT export import as fallback and batch source
9. Privacy review before capture, indexing, or export
10. Audit log and provenance manifest
11. Local archive/vault structure with checksums and schema version
12. Duplicate detection
13. Rebuild search index

## Initial Non-Goals

- Unattended full account traversal through the ChatGPT UI
- Always-on hidden browser scraping
- Cloud sync
- Multi-user SaaS
- Enterprise admin console
- Semantic search
- Knowledge graph
- Multi-provider support
- Autonomous deletion or restore

## Ingestion Direction

Use Codex-browser-assisted selected-chat capture as a core differentiating workflow, with official export files as the fallback and batch-import path.

Avoid unattended full-account crawling in MVP. The reliable v1 browser promise should be visible, selected, user-approved capture.

## Cancellation-Worthy MVP Thesis

VaultGPT MVP should be strong enough that a current paid extension user can reasonably cancel or avoid a paid subscription because VaultGPT offers the core paid workflow for free:

- unlimited local organization
- unlimited full-text search
- bulk export and backup
- bulk organization actions
- prompt vault and variables
- simple prompt chains
- selected-chat browser capture
- privacy review and audit trail

## Target User

Start personal-first for power users, builders, consultants, researchers, and people with large ChatGPT archives. Enterprise positioning can come later after the archive/search/export loop is proven.

## MVP Success Test

A current user of Superpower ChatGPT or ChatGPT Toolbox should see that VaultGPT offers the core paid features they care about for free, with a stronger trust story because the workflow is local-first, Codex-native, and auditable.

## Explicit Deferrals

- Cloud sync
- Prompt marketplace
- Full unattended account crawl
- Rich context mentions
- Team admin and SSO
- Media/audio gallery
- Usage analytics
- Multi-model gateway
- Browser-side injected UI

## Finish-Line MVP Items Still In Scope

These are not deferrals. They are required before VaultGPT can be called a finished publishable MVP.

1. Codex Chrome save-chat workflow
   - primary target: current active ChatGPT tab
   - fallback target: specific ChatGPT URL
   - deferred: selected-tabs or multi-tab capture
   - constrained current ChatGPT browser conversation capture
   - preview and explicit confirmation before write
   - privacy review and audit log
   - no broad Codex project/environment context capture

2. Installed-plugin UX
   - starter action menu verified after reinstall/reload
   - explicit and implicit invocation verified
   - should-not-trigger prompt verified
   - save/import/search/export/prompt/privacy actions visible and intuitive

3. Core workflows through plugin surface
   - official export import
   - vault search
   - export/backup
   - prompt variables
   - privacy review
   - lightweight pass/warn/block fidelity review

4. Bulk-friendly review principle
   - use counts, hashes, manifests, privacy summaries, and samples
   - do not deep-review every item by default
   - escalate only anomalies or user-requested deep checks

5. Final release gates
   - real or redacted export edge-case validation
   - completed test matrix and release checklist
   - public manifest URL/contact metadata
   - final public-file scan

Current state: VaultGPT has a working local engine and installable plugin foundation. It is not yet a finished MVP product because the browser-capture workflow and installed-plugin end-to-end UX still need acceptance testing and refinement.
