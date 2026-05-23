# VaultGPT Cancellation-Worthy MVP Research

## Research Question

Which paid or capped third-party ChatGPT extension features are most likely to make users cancel, avoid, or switch away from paid extensions if VaultGPT offers them free?

## Core Finding

The most cancellation-worthy features are workflow and ownership features, not generic AI features:

- finding old chats
- organizing large chat histories
- exporting and backing up selected work
- performing bulk cleanup
- reusing prompts
- referencing captured work safely

## Ranked MVP Features

### 1. Full-Text Search Across Chat Content

High priority. Users with many conversations need retrieval, not sidebar scrolling. Competitors gate or cap full-history search.

MVP decision: include.

### 2. Unlimited Folders, Subfolders, Tags, and Pins

High priority. Organization is a headline feature for ChatGPT productivity extensions and is commonly capped in free tiers.

MVP decision: include.

### 3. Bulk Export and Backup

High priority. Users value selective, readable, immediate exports more than raw native data dumps.

MVP decision: include Markdown, JSON, and ZIP.

### 4. Bulk Move, Archive, Delete, and Tag

High priority, but requires safety. This replaces tedious one-at-a-time operations.

MVP decision: include with dry-run, undo, and confirmation.

### 5. Prompt Vault With Variables

High priority. Prompt organization is a proven paid category through tools like AIPRM and extension prompt libraries.

MVP decision: include saved prompts, variables, folders/tags, and search.

### 6. Simple Prompt Chains

Medium-high priority. Paid tools market prompt chains and reusable workflows.

MVP decision: include minimal saved ordered steps. Defer autonomous execution.

### 7. Codex Chrome Selected-Chat Capture

High strategic priority. This proves VaultGPT is not merely an import/export utility and connects the product to the newest Codex browser capability.

MVP decision: include constrained, visible, user-approved selected-chat capture. Do not promise full account crawl.

### 8. Privacy Review and Audit/Provenance Logs

High strategic priority. These are not the paid features themselves, but they are the trust reason to choose VaultGPT over opaque third-party extensions.

MVP decision: include.

## Deferred Features

- cloud sync
- prompt marketplace
- full unattended account crawl
- rich context mentions
- team admin and SSO
- media/audio gallery
- usage analytics
- multi-model gateway
- browser-side injected UI

## Architecture Implication

Use official ChatGPT export import as the reliable batch/fallback path, but keep Codex Chrome selected-chat capture as a visible core differentiator.

The MVP should not rely on unattended ChatGPT UI crawling.

