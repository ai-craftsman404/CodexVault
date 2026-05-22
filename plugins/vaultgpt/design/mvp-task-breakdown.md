# VaultGPT MVP Task Breakdown

## Build Principle

Use TDD where practical. Each task should add tests or fixtures before implementation.

## Phase 0: Scaffold

- Create `.codex-plugin/plugin.json`.
- Create `README.md`, `CHANGELOG.md`, `LICENSE`.
- Create `skills/vaultgpt/SKILL.md`.
- Create `scripts/vaultgpt/` structure.
- Create test fixture directories.

Acceptance:

- Manifest parses.
- Plugin paths are relative and valid.
- Skill file exists with correct trigger description.

## Phase 1: Vault Core

- Implement vault initialization.
- Implement JSON record read/write.
- Implement schema version field.
- Implement append-only audit log.

Tests:

- initializes empty vault
- writes conversation/prompt/audit event
- rejects invalid schema version
- keeps runtime vault outside plugin source by default

## Phase 2: Prompt Vault

- Save prompt templates.
- Detect variables from `{field}` and `{{field}}`.
- Render prompt with provided values.
- Track usage count and last-used timestamp.
- Export/import prompt records using VaultGPT schema.

Tests:

- variable detection
- missing required variable failure
- render preview
- prompt import/export roundtrip
- prompt usage audit event

## Phase 3: Import And Search

- Add official-export fixture parser.
- Normalize conversations.
- Build local full-text index.
- Return snippets and source IDs.
- Report index status: indexed, skipped, stale, failed.

Tests:

- parses sample export
- handles malformed export
- searches title/body/tags
- reports skipped records
- index rebuild is idempotent

## Phase 4: Organization

- Add folders/subfolders metadata.
- Add tags and pins.
- Add unfiled inbox default.
- Add saved searches.
- Allow bulk operations from filtered results.

Tests:

- captured/imported item defaults to unfiled
- move/tag/pin single item
- bulk tag/move from search results
- saved search reruns correctly
- audit records metadata changes

## Phase 5: Export And Backup

- Export selected/folder/tag/search/all scopes.
- Write Markdown, JSON, and ZIP.
- Include manifest, counts, hashes, skipped/failed items.
- Add failure report and retry list.

Tests:

- export selected records
- export folder as ZIP
- manifest includes counts and hashes
- skipped/failed items reported
- private vault data not written into repo

## Phase 6: Privacy Review

- Detect likely API keys, tokens, emails, local paths, private URLs.
- Categorize findings.
- Support redaction preview.
- Require confirmation for high-risk override.

Tests:

- detects common secrets
- detects local paths
- false-positive fixture
- redaction preview does not mutate original
- override audited

## Phase 7: Manual Prompt Chains

- Save ordered chain steps.
- Resolve variables across steps.
- Track manual run state.
- Convert chat to candidate prompt/chain with confirmation.

Tests:

- create chain
- detect chain variables
- run one step at a time
- stop/resume run state
- convert fixture chat to prompt/chain proposal

## Phase 8: Codex Chrome Capture Path

- Define normalized selected-chat capture payload.
- Add capture normalization script.
- Add manual verification guide for Codex Chrome selected-chat capture.
- Keep official export import as fallback.

Tests:

- normalize selected-chat fixture
- duplicate capture offers update/copy behavior
- privacy review gates save
- audit event records capture source

## Phase 9: Release Readiness

- Fill full test matrix.
- Complete security review.
- Complete release checklist.
- Validate public README.
- Check no private data is committed.

Acceptance:

- all mandatory relevant testing categories are covered or justified
- local install/discovery verified
- explicit and implicit skill triggers verified
- public packaging is self-contained under `plugins/vaultgpt/`

## MVP Finish-Line Scope

The local engine is implemented, but the product MVP is not over the line until the installed plugin experience passes these items.

### 1. Codex Chrome Save-Chat Workflow

- Use Codex Chrome extension as a core MVP capture path.
- Capture only the intended selected/current ChatGPT browser conversation.
- Do not capture broad Codex project context, workspace instructions, terminal output, or environment metadata unless explicitly selected as the source.
- Show preview before save: title, source, message count, scope, model label if available, folder/status, and privacy findings.
- Require explicit confirmation before writing.

Acceptance:

- installed plugin can save a real or synthetic ChatGPT browser conversation through the Chrome capture path
- audit log records source as constrained browser capture
- no project/environment paths appear unless they were present inside the selected chat

### 2. Installed-Plugin UX

- Verify the new starter action menu after reinstall/reload.
- Verify explicit invocation.
- Verify implicit invocation.
- Verify should-not-trigger behavior.
- Ensure Save Chat does not default to broad visible Codex context.

Acceptance:

- first-run user sees clear options, not one ambiguous save prompt
- user can choose save/import/search/export/prompt/privacy actions
- skill only activates when VaultGPT-relevant intent is present

### 3. Core Workflows Through Plugin Surface

- Import official ChatGPT export through plugin guidance.
- Search local vault through plugin guidance.
- Export or back up vault through plugin guidance.
- Create/render prompt with variables through plugin guidance.
- Run privacy review before save/export.

Acceptance:

- each workflow is tested from installed plugin prompt to local artifact/result
- results are concise and show what was read/written
- failures are reported without silent data loss

### 4. Safety And Release Gates

- Add redacted real-export edge-case fixture or document why unavailable.
- Complete final test matrix.
- Replace public manifest URL/email placeholders.
- Update README with install, first-run menu, and known limitations.
- Run final public-file scan.

Acceptance:

- release checklist has no unresolved MVP blockers
- public repo metadata is final
- no runtime vault data, private paths, exports, screenshots, or secrets are committed
