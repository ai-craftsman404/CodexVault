# VaultGPT Business Objectives and Feature Map

## Core Business Objectives

1. Replace unsafe or opaque third-party ChatGPT browser extension reliance.
2. Offer common paid-extension power features for free.
3. Use modern Codex capabilities and plugin packaging to create a durable, repurposable, future-compatible product.

## Objective 1: Replace Risky Extension Reliance

VaultGPT should reduce the need for users to install or depend on high-privilege third-party browser extensions that can access ChatGPT sessions, browser content, or personal AI history.

Relevant capabilities:

- Codex-browser-assisted selected-chat capture
- visible browser actions
- user approval gates
- local-first storage
- no telemetry by default
- privacy review before capture/index/export
- audit logs for capture and export actions
- provenance from outputs back to source chats
- protected or excluded chat lists
- dry-run mode for bulk actions

## Objective 2: Free Paid-Extension Power Features

VaultGPT should target popular capabilities that competitors cap or monetize.

Relevant capabilities:

- unlimited folders and subfolders
- unlimited pins or favorites
- unlimited saved prompts
- full-text search without low result caps
- bulk export
- bulk archive/delete with confirmation
- prompt chaining
- tags or labels
- export to Markdown and JSON
- local portable vault as a sync alternative
- audit/export logs

## Objective 3: Codex-Native Future Compatibility

VaultGPT should be built so new Codex and ChatGPT capabilities can improve or extend it without rewriting the whole product.

Relevant capabilities:

- Codex plugin packaging
- skill-based workflows
- local scripts for deterministic operations
- subagents for bounded review and curation
- agent-team orchestration for risky or high-value workflows
- governed AI harness checkpoints
- versioned prompt templates
- versioned vault schemas
- versioned export formats
- isolated browser capture adapter
- model-agnostic search, archive, prompt, and export layers

## Highest-Priority Overlap Features

These features support both objectives and should be MVP candidates:

- Codex-browser-assisted selected-chat capture with explicit approval
- local archive/vault with folders, tags, pins, and saved prompts
- full-text local search
- bulk export with dry-run preview
- bulk move, archive, delete, and tag with undo/confirmation
- prompt library with variables
- simple prompt chaining
- privacy review before indexing/export
- audit log and provenance manifest

## Cancellation-Worthy MVP Set

VaultGPT should initially target the smallest feature set likely to replace a paid extension subscription:

1. Full-text search across all chat content
2. Unlimited folders, subfolders, tags, and pins
3. Bulk export and backup to Markdown, JSON, and ZIP
4. Bulk move, archive, delete, and tag
5. Prompt vault with variables
6. Simple prompt chains
7. Codex Chrome selected-chat capture
8. Privacy review and audit/provenance logs

## Strategic Filter

Prioritize a feature when:

- current extension users already understand it
- a competitor caps or charges for it
- it reduces trust in third-party extensions
- Codex can make the workflow more transparent, auditable, or local-first

Deprioritize a feature when:

- it is only generic archive management
- it does not help replace paid extension workflows
- it requires fragile unattended full-account crawling
- it adds governance theater without user-visible value
