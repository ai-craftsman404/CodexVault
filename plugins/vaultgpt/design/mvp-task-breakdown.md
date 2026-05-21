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

