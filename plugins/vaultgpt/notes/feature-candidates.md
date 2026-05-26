# VaultGPT Candidate Features

## Feature Selection Strategy

Candidate features should be judged against two business objectives:

1. Does this reduce the user's reliance on unsafe or opaque third-party ChatGPT browser extensions?
2. Does this provide a power feature that competitors commonly cap or charge for?

Features that satisfy both objectives should receive the highest priority.

Revised feature lens: remove features that Codex can already approximate as one-off local folder work unless VaultGPT adds a persistent, ChatGPT-specific product workflow. The next target is Selective Async ChatGPT Export, centered on Codex Chrome and user-selected ChatGPT conversation URLs.

Public-preview focus: ship the selected-export workflow. Do not spend near-term effort on ChatGPT App integration, direct ChatGPT-to-Codex invocation, generic RAG, or cloud delegation.

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

## Revised High-Volume Archive Candidate List

Superseded by the Selective Async ChatGPT Export target. Some items remain useful as supporting infrastructure, but the main wedge is not official-export import or generic local archive management.

## Selective Async ChatGPT Export Candidate List

Preserve these candidates because they put Codex Chrome at the center and solve ChatGPT's all-or-nothing export limitation:

1. URL-list selected export
   - User provides selected ChatGPT conversation URLs by chat paste or `.txt`/`.csv`/`.md` file.
   - One URL per line preferred.
   - Lines beginning with `#` are comments.

2. Async export job system
   - Creates a job ID immediately.
   - Tracks queued, capturing, reviewing, exporting, complete, failed, cancelled.
   - Prevents the user session from hanging while selected captures run.

3. Codex Chrome per-URL capture
   - Opens or claims each selected ChatGPT URL through the signed-in Chrome session.
   - Captures title, URL, visible messages, roles, confidence, and limitations.
   - Sequential in v1 for browser reliability.

4. Batch dry-run preview
   - Shows URL count, candidate titles, capture confidence, missing/incomplete warnings, privacy risk, and expected output before final export.

5. Agent-team supervised pipeline
   - Orchestrator, capture worker, fidelity reviewer, privacy reviewer, packager, and user gatekeeper coordinate the job.
   - Browser capture can be sequential while review/packaging can become parallel later.

6. Retry/resume failed captures
   - Failed URLs stay visible with reason and retry action.
   - Successful captures are not repeated unnecessarily.

7. Selected export package
   - Writes Markdown, JSON, and ZIP.
   - Includes manifest, hashes, source URLs, per-URL status, skipped/failed records, privacy summary, fidelity summary, and audit log.

8. Progress indicator surface
   - Codex plugin v1 can expose status commands and job files.
   - Future ChatGPT App can show spinner/progress panel, but this is not public-preview scope.

## Public Preview Defaults

- Menu-driven chat interaction.
- 25 URLs per v1 job.
- ZIP-only user-facing export artifact, containing Markdown and JSON internally.
- High-risk privacy findings block by default.
- User can redact, exclude, cancel, or explicitly override with audit logging.
- Hybrid approval: batch approval for clean results, per-item approval for warnings or ambiguity.
- Sequential Chrome capture in v1.
- Agent-team supervision is a design principle for orchestration, review, privacy, packaging, and user gates.

Supporting candidates from the older archive direction:

1. High-volume ChatGPT export importer
   - Purpose-built parser for official `conversations.json`.
   - Handles thousands or tens of thousands of chats reliably.
   - Reports skipped, malformed, duplicate, and incomplete records.

2. Persistent VaultGPT index
   - Stable metadata/index layer for chats, messages, models, dates, tags, folders, privacy status, and provenance.
   - Rebuildable and reusable across Codex sessions.

3. Query/date filtered bulk export with dry-run
   - Filters by date range, keyword/search query, folder, tag, status, and model/GPT where available.
   - Dry-run shows count, estimated size, and sample titles before writing.

4. Saved export rules
   - Saves repeatable filters such as `all coding chats from 2025` or `privacy-risk chats older than 1 year`.
   - Lets users rerun curated exports without rebuilding the workflow.

5. Resumable chunked export jobs
   - Exports 10,000+ chats in batches with manifests and recovery state.
   - Supports safe retry after interruption.

6. Archive health report
   - Summarizes imported chats, skipped chats, duplicates, missing fields, failed parses, index status, and privacy-risk counts.

7. Duplicate and near-duplicate detection
   - Detects repeated exports, copied chats, and repeated conversations.

8. Bulk privacy triage
   - Flags likely secrets, personal data, local paths, tokens, and risky chats.
   - Enables export/delete/review by risk level with audit logs.

Deprioritize as standalone wedges:

- Basic keyword search because Codex can already search local files.
- Manual folder/tag organization because Codex can organize files manually.
- Simple Markdown/JSON export because Codex can script it.
- Prompt library/variables/chains because Codex can approximate them.
- Single active-tab save because it is only an entry point, not the selected-export product.
- Topic clustering/summaries until the deterministic archive/export loop is strong.

## MVP Candidate Set

The MVP should prioritize the Market Intel Summary features before broader archive or knowledge-management capabilities.

### Tier 1: Core MVP

- URL-list selected export from pasted chat text or `.txt`/`.csv`/`.md` file
- Async job record/status/progress
- Sequential Codex Chrome per-URL capture
- Batch dry-run preview
- Retry failed URLs
- Agent-team supervised review pipeline
- Selected Markdown/JSON/ZIP export package
- Local audit log and provenance manifest

### Tier 2: Strong Follow-On

- Codex Chrome active-tab capture refinement
- Open-tab collection
- ChatGPT App intent/progress UI
- Saved selected export baskets
- Resumable chunked capture jobs
- Prompt vault with saved prompts and variables
- Simple saved prompt chains
- Context mentions from vault into current ChatGPT/Codex workflows
- Smart tags or auto-categorization
- Notes and bookmarks
- Rebuildable local search index
- Redaction preview

### Tier 3: Later / Not MVP

- full unattended account crawl
- direct ChatGPT-to-Codex-plugin invocation without a safe bridge
- ChatGPT App integration for public preview
- cloud Codex delegation for public preview
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

- Selective URL-list export solves the native all-or-nothing ChatGPT export limitation.
- Async jobs prevent long selected-export runs from hanging the user session.
- Codex Chrome per-URL capture keeps the user's signed-in browser session central without handing access to an opaque third-party extension.
- Batch dry-run preview reduces accidental over-export.
- Retry/resume behavior makes large selected URL lists practical.
- Agent-team supervision makes capture, fidelity, privacy, and packaging explicit rather than hidden.
- Privacy review and audit logs make the free replacement more trustworthy than opaque third-party extensions.
