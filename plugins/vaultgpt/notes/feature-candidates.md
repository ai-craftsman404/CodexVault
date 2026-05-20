# VaultGPT Candidate Features

## Feature Selection Strategy

Candidate features should be judged against two business objectives:

1. Does this reduce the user's reliance on unsafe or opaque third-party ChatGPT browser extensions?
2. Does this provide a power feature that competitors commonly cap or charge for?

Features that satisfy both objectives should receive the highest priority.

## Market Intel Summary

This is the primary feature priority list for VaultGPT. These features are popular in current ChatGPT productivity extensions and are commonly capped, paid, or bundled into premium tiers.

1. Full-text search across all chat content
2. Unlimited folders, subfolders, tags, and pins
3. Bulk export and backup
4. Bulk move, archive, delete, and tag
5. Prompt vault with variables
6. Simple prompt chains
7. Codex Chrome selected-chat capture
8. Privacy review before save, indexing, export, or sharing
9. Audit log and provenance manifest

## MVP Candidate Set

The MVP should prioritize the Market Intel Summary features before broader archive or knowledge-management capabilities.

### Tier 1: Core MVP

- Full-text local search without result caps
- Unlimited folders, subfolders, tags, and pins
- Bulk export and backup to Markdown, JSON, and ZIP
- Bulk move, archive, delete, and tag with dry-run, undo, and confirmation
- Prompt vault with saved prompts and variables
- Simple saved prompt chains
- Codex Chrome selected-chat capture with explicit user approval
- Privacy review before capture/export
- Local audit log and provenance manifest

### Tier 2: Strong Follow-On

- Context mentions from vault into current ChatGPT/Codex workflows
- Smart tags or auto-categorization
- Notes and bookmarks
- Rebuildable local search index
- Duplicate detection
- Redaction preview

### Tier 3: Later / Not MVP

- full unattended account crawl
- semantic search
- knowledge graph
- prompt marketplace
- multi-provider support
- team admin and SSO
- cloud sync
- image/video generation features

## Archive and Export

- Supporting infrastructure, not headline positioning.
- Import official ChatGPT export files
- Import selected conversation files
- Export selected chats
- Bulk export
- Folder or project export
- Markdown export
- JSON export
- TXT export
- HTML or PDF export
- Export previews
- Export integrity report
- Delta or incremental export

## Organization

- High-priority market feature.
- Folders and subfolders
- Tags and labels
- Pins and favorites
- Notes and bookmarks
- Project or GPT grouping
- Bulk rename
- Safe delete/archive workflows

## Search

- High-priority market feature.
- Full-text local search
- Metadata search
- Date filters
- GPT or project filters
- Tag filters
- Attachment or media filters
- Saved searches
- Index rebuild

## Prompt Workflows

- High-priority market feature.
- Prompt library
- Prompt variables
- Prompt chaining
- Prompt import/export
- Prompt tagging
- Prompt folders

## Knowledge Layer

- Defer broad knowledge management. Keep only lightweight extraction where it strengthens prompt/workflow productivity.
- Chat summaries
- Action item extraction
- Decision extraction
- Reusable instruction extraction
- Topic clustering
- Semantic search
- Knowledge graph

## Safety and Trust

- Core differentiator supporting the extension-replacement strategy.
- Local-only mode
- No telemetry by default
- Explicit confirmations
- Dry-run mode
- Audit logs
- Export logs
- PII and sensitive-content warnings
- Redaction preview
- Protected or excluded chats

## Reliability

- Supporting infrastructure for trust and repeatability.
- Resume interrupted imports
- Duplicate detection
- Archive validation
- Rebuild search index
- Corruption detection
- Parser and manifest version metadata

## Codex-Native Differentiators

- Agent-team review for risky operations
- Governed workflow harness
- Visible approval gates
- Local filesystem ownership
- Reduced browser-extension attack surface

## Highest-Priority Candidate Features For The Business Strategy

- unlimited folders and subfolders
- unlimited pins or favorites
- unlimited saved prompts
- full-text local search without result caps
- bulk export
- bulk archive/delete with dry-run and confirmation
- prompt chaining
- tags or labels
- privacy review before capture/export
- local audit logs
- Codex-browser-assisted selected-chat capture
- portable local vault as a sync alternative

## Cancellation-Worthy MVP Feature Rationale

These are the features most likely to make users cancel or avoid paid ChatGPT extensions if VaultGPT offers them free:

- Full-text search solves the daily retrieval pain that native ChatGPT and free extension tiers do not solve well.
- Unlimited folders, subfolders, tags, and pins replace paid organization caps.
- Bulk export and backup replace paid ownership/portability workflows.
- Bulk move, archive, delete, and tag replace high-friction manual cleanup workflows.
- Prompt vault with variables replaces paid prompt-management limits.
- Simple prompt chains provide paid workflow value without building a full automation engine.
- Codex Chrome selected-chat capture proves VaultGPT is not only an import/export utility.
- Privacy review and audit logs make the free replacement more trustworthy than opaque third-party extensions.
