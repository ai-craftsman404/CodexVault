# VaultGPT Competitor Pattern Backlog

## Purpose

Track additional competitor interaction patterns that VaultGPT may mirror later to reduce switching friction for paid-extension users.

## High-Value Patterns To Consider

### Unfiled Inbox

Newly captured chats land in an `Unfiled` or `Inbox` queue until the user organizes them.

Why it matters:

- Reduces capture friction.
- Matches how users expect unorganized items to behave.
- Avoids forcing folder choice during first save.

MVP consideration: strong candidate.

### Saved Searches / Smart Collections

Users save a query/filter as a reusable pseudo-folder.

Why it matters:

- Gives power users dynamic organization without duplicating files.
- Complements full-text search and tags.

MVP consideration: possible if search/filter implementation is simple.

### Recent Prompts And Recently Used Context

Surface recently used prompts, chains, chats, and context attachments.

Why it matters:

- Reduces repeated search.
- Mirrors common prompt/sidebar extension behavior.

MVP consideration: lightweight candidate.

### Export Progress And Failure Report

Bulk export should show progress, counts, skipped items, failed items, and retry options.

Why it matters:

- Builds trust in large-history operations.
- Differentiates from opaque browser extension exports.

MVP consideration: strong candidate.

### Convert Chat To Prompt Or Chain

User can turn a good chat exchange into a saved prompt template or simple chain.

Why it matters:

- Connects archive capture to productivity.
- Makes VaultGPT more than storage/search.

MVP consideration: strong candidate.

### Index Status

Show local index health and progress, such as `indexed 82/100 chats`.

Why it matters:

- Sets expectations for search completeness.
- Reduces confusion when results are missing.

MVP consideration: strong candidate.

### Keyboard Shortcuts And Aliases

Provide familiar shortcuts and aliases:

- `/prompt`
- `/chain`
- `/context`
- Save Chat
- Search Vault

Why it matters:

- Mirrors paid-extension power-user flows.
- Reduces switching friction.

MVP consideration: include where compatible with Codex plugin surface.

### Prompt Library Import/Export

Allow users to import/export prompt libraries in open formats.

Why it matters:

- Helps users migrate away from paid prompt tools.
- Reinforces local ownership.

MVP consideration: include export; import can be follow-on unless simple.

### Favorites Bar

Pinned folders, prompts, chats, and searches appear in a fast-access area.

Why it matters:

- Mirrors extension sidebar productivity.
- Makes active work faster to resume.

MVP consideration: follow-on unless easy.

### Prompt/Chain Usage History

Track last used, run count, duplicate/edit, and recent runs.

Why it matters:

- Helps users identify valuable reusable workflows.
- Supports auditability and productivity.

MVP consideration: follow-on; audit log provides foundation.

## Most Likely MVP Additions

1. Unfiled inbox
2. Export progress and failure report
3. Index status
4. Convert chat to prompt
5. Recent prompts/context

## Follow-Up Research Outcome

Additional MVP-worthy patterns from competitor research:

- No-signup instant start: VaultGPT should work immediately after install without account creation.
- Bulk actions from search/filter results: saved search results should be actionable, not just view-only.
- Prompt import/export: export prompts/chains in open formats; support import from VaultGPT schema first.
- Convert chat to prompt or manual chain: strong adoption bridge from captured chats to reusable workflows.
- Usage-history fields: track last used, run count, and last exported in prompt/audit records.

Patterns to defer until a richer browser UI/app exists:

- persistent favorites bar
- drag/drop folder tree
- global keyboard shortcuts
- always-visible recent-context panel
- browser-injected prompt/context chips
- rich analytics dashboard
- cloud sync

Rejected for MVP:

- zero-effort auto-capture, because it conflicts with VaultGPT's explicit approval and trust positioning
- team/share-ready prompt handoff, because it pulls the product toward collaboration and governance too early
