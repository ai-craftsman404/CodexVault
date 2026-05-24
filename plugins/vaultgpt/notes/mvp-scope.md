# VaultGPT MVP Scope

## MVP Principle

Choose moderate-complexity, high-value, popular workflows that map to competitor paid features and reduce reliance on unsafe third-party browser extensions.

The MVP should not be framed as a generic archive/search tool. It should be framed as a free, trusted Codex-native replacement for paid ChatGPT extension workflows.

Revised priority: VaultGPT's real MVP target is Selective Async ChatGPT Export. Users should be able to export exactly the ChatGPT conversations they choose, not their entire account.

The core pain to solve is ChatGPT's all-or-nothing native export. VaultGPT should let users provide selected ChatGPT conversation URLs, then run a governed Codex Chrome export job with preview, retry, privacy review, fidelity checks, manifest, and audit trail.

The current package should be treated as an MVP-RC foundation, not the final release target. It proves local vault, privacy, audit, export packaging, and active-tab capture primitives that can be repurposed for selective async export.

Public-preview focus: this selected-export feature set is the core product focus now and for the near future. ChatGPT App integration, direct ChatGPT-to-Codex invocation, and cloud Codex delegation are not part of the current public-preview target.

## Recommended MVP Features

1. URL-list input via chat paste or `.txt`/`.csv`/`.md` file
2. Async selected export job record with status, progress, cancellation, and retry state
3. Codex Chrome capture for each selected ChatGPT URL
4. Dry-run preview before saving/exporting, including title, URL, visible message count, roles, capture confidence, privacy status, and expected output
5. Sequential browser capture for v1, with agent-team orchestration supervising the end-to-end job
6. Lightweight fidelity review for each capture
7. Privacy review before final export package creation
8. Retry failed or incomplete URL captures
9. Markdown/JSON/ZIP package with manifest, hashes, per-URL status, skipped/failed records, and audit log
10. Current active-tab capture and official ChatGPT export import as supporting paths, not the main wedge

## Public Preview Defaults

- User interaction is menu-driven through chat.
- Maximum v1 job size is 25 ChatGPT conversation URLs.
- Export output is one ZIP package.
- ZIP contains Markdown, JSON, manifest, privacy report, fidelity report, failure report, hashes, and audit/events.
- High-risk privacy findings block export by default.
- High-risk resolutions are redact, exclude, cancel, or explicit override.
- Overrides must be audit-logged.
- Preview approval is hybrid: clean batches can be approved together, but warnings, redirects, auth ambiguity, fidelity mismatch, or message-count mismatch escalate to per-item approval.

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

Use user-supplied selected ChatGPT conversation URLs as the primary ingestion path for the real MVP target. This avoids full-account crawling while solving the native all-or-nothing export limitation.

Use Codex-browser-assisted capture for each selected URL. The user chooses the scope; VaultGPT handles capture, review, packaging, and audit.

Use official ChatGPT export files as a fallback/batch support path, not as the main product wedge.

Avoid unattended full-account crawling in MVP. The reliable v1 browser promise should be visible, selected, user-approved capture.

## Cancellation-Worthy MVP Thesis

VaultGPT MVP should be strong enough that a current paid extension user can reasonably cancel or avoid a paid subscription because VaultGPT offers the core paid workflow for free:

- provide a selected list of ChatGPT conversation URLs
- preview what VaultGPT will capture before anything is written
- run the selected export asynchronously without blocking the user session
- retry failed or incomplete captures
- export only chosen conversations to Markdown/JSON/ZIP
- receive a manifest showing exactly what was captured, skipped, failed, and why
- review privacy and fidelity status before final package creation
- avoid handing browser-session access to an opaque third-party extension

## Target User

Start personal-first for power users, builders, consultants, researchers, and people who want selected ChatGPT exports without downloading their entire account archive. Enterprise positioning can come later after the selected-export loop is proven.

## MVP Success Test

A current user of Superpower ChatGPT or ChatGPT Toolbox should see that VaultGPT offers the core paid features they care about for free, with a stronger trust story because the workflow is local-first, Codex-native, and auditable.

Updated success test: a user can paste or upload a list of ChatGPT conversation URLs, start a background VaultGPT job, review progress and per-URL results, retry failures, and receive a clean selected export package without manually opening/exporting each chat.

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
- True parallel Chrome capture across multiple browser profiles
- ChatGPT App progress UI
- ChatGPT App intent broker
- Direct ChatGPT-to-Codex plugin invocation
- Cloud Codex delegation for capture/review/packaging
- Open-tab discovery
- Deep agent-team beautification

## Finish-Line MVP Items Still In Scope

These are not deferrals. They are required before VaultGPT can be called a finished publishable MVP.

1. Selective Async ChatGPT Export workflow
   - primary target: user-provided list of ChatGPT conversation URLs
   - supported input: pasted chat text or `.txt`/`.csv`/`.md` file
   - URL comments ignored when line starts with `#`
   - async job record with status/progress
   - sequential Codex Chrome capture in v1
   - retry failed URLs
   - Markdown/JSON/ZIP output package
   - manifest, hashes, per-URL status, skipped/failed records, privacy summary, fidelity summary, and audit log

2. Codex Chrome save-chat workflow
   - secondary target: current active ChatGPT tab
   - constrained current or selected ChatGPT browser conversation capture
   - preview and explicit confirmation before write
   - privacy review and audit log
   - no broad Codex project/environment context capture

3. Installed-plugin UX
   - starter action menu verified after reinstall/reload
   - explicit and implicit invocation verified
   - should-not-trigger prompt verified
   - save/import/search/export/prompt/privacy actions visible and intuitive

4. Core workflows through plugin surface
   - URL-list import
   - async selected export job status
   - vault search
   - selected export package creation
   - prompt variables
   - privacy review
   - lightweight pass/warn/block fidelity review

5. Agent-team orchestration principle
   - Orchestrator owns job state, progress, retries, and final merge
   - Capture worker handles Codex Chrome URL capture
   - Fidelity reviewer checks capture completeness signals
   - Privacy reviewer scans sensitive content before export
   - Packager creates Markdown/JSON/ZIP and manifest
   - User gatekeeper pauses for approval on risky or incomplete outputs

Cloud Codex note: cloud sessions may be useful later for post-capture review, formatting, packaging, and tests, but they cannot access the user's local logged-in Chrome session or Codex Chrome extension. Keep v1 local-first.

6. Bulk-friendly review principle
   - use counts, hashes, manifests, privacy summaries, and samples
   - do not deep-review every item by default
   - escalate only anomalies or user-requested deep checks

7. Final release gates
   - real or redacted export edge-case validation
   - completed test matrix and release checklist
   - public manifest URL/contact metadata
   - final public-file scan

Current state: VaultGPT has a working local engine and installable plugin foundation. It is not the final MVP target. The next release target is Selective Async ChatGPT Export.
