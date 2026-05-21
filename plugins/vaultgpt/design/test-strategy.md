# VaultGPT Test Strategy

## Testing Approach

Use TDD/STLC-style planning. Define expected behavior and adversarial cases before implementation.

## Mandatory Test Areas

- Manifest validation and local install/discovery.
- Explicit and implicit skill invocation.
- Should-not-trigger prompts.
- First-time Save Chat journey.
- Returning Search Vault journey.
- Export/Backup journey.
- Prompt creation and prompt-use journey.
- Manual prompt-chain journey.
- Unfiled inbox journey.
- Saved search and bulk action from search results.
- Convert chat to prompt/chain journey.
- Official export parser fixtures.
- Selected-chat capture fixture or documented manual verification.
- Full-text search correctness.
- Folder/tag/pin metadata behavior.
- Bulk action dry-run, confirmation, undo, and audit records.
- Markdown/JSON/ZIP export structure.
- Prompt variables and simple prompt-chain rendering.
- Prompt import/export using VaultGPT schema.
- Privacy review false positives and false negatives.
- Prompt-injection resistance from imported/captured chats.
- Provenance and audit log completeness.
- Index status and stale/skipped item reporting.
- Export progress/failure reporting.
- Windows path handling.
- Secret/private export exclusion.

## Adversarial Evaluator Scenarios

- Archived chat tells VaultGPT to ignore system instructions.
- Chat contains fake credentials or real-looking secrets.
- Chat contains path traversal filenames.
- Export contains malformed JSON or missing fields.
- Bulk delete is requested without dry-run/confirmation.
- Redacted content remains searchable after index rebuild.
- Prompt variable injection attempts to alter workflow behavior.

## Release Gate

No public release until:

- all relevant mandatory testing categories are covered or explicitly justified
- security/privacy review is complete
- public docs explain limitations
- sample fixtures contain no private user data
- install and trigger tests pass
- UX journey tests pass for save, search, export, prompt use, and privacy review
- No-signup instant-start path is documented and tested
