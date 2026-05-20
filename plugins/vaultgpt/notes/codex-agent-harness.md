# VaultGPT Codex Agent Harness

## Design Principle

Make Codex subagents, agent-team orchestration, and governed AI harness behavior part of the product surface when they add trust, safety, or value.

Do not show agents for every small action. Use progressive visible governance.

## Strategic Goal

Use recent Codex capabilities as a core VaultGPT differentiator:

- subagents
- agent-team orchestration
- governed AI harness workflows
- Codex Chrome selected-chat capture
- Codex plugin packaging

These capabilities should make VaultGPT easier to trust, easier to audit, easier to update, and easier to repurpose for future ChatGPT/Codex model releases.

## Progressive Governance Rule

Simple operations should stay simple:

- search
- view
- export one chat
- browse tags

Sensitive or high-impact operations should show the governed workflow:

- bulk import
- bulk export
- redaction
- indexing private archives
- knowledge pack generation
- delete/archive operations
- retention rule changes

## Agent Roles

### Archive Scout

Validates import/export structure, detects unsupported fields, checks duplicates, and reports archive coverage.

### Privacy Reviewer

Flags PII, secrets, credentials, confidential content, and sensitive topics before indexing or export.

### Knowledge Curator

Extracts summaries, decisions, action items, reusable prompts, and project notes with citations back to source conversations.

### Search Indexer

Builds and rebuilds the local search index, reports skipped items, corrupt records, and index coverage.

### Audit Agent

Produces manifests, checksum reports, activity logs, export logs, and provenance records.

## Evidence Cards

Each visible agent should produce concise evidence cards:

- finding
- source
- confidence
- action taken
- approval needed

## Human Approval Gates

Require explicit confirmation for:

- indexing private folders
- exporting bulk archive content
- redacting or deleting content
- changing retention rules
- sharing or moving archive bundles

## Constraint

The agent team should not become an overbuilt pseudo-orchestrator. The main Codex thread remains final planner and adjudicator. Local artifacts, manifests, checksums, and audit logs are the source of truth.

## Future Compatibility Rules

- Do not hardcode behavior to a single model release.
- Keep prompts and agent-role instructions versioned.
- Keep vault schemas and export formats versioned.
- Keep browser capture logic isolated from archive, search, prompt, and export logic.
- Keep model-assisted curation optional and reproducible where possible.
- Make plugin packaging the update boundary for new workflows and model-specific improvements.
- Use the agent harness to review compatibility when ChatGPT/Codex browser behavior or model behavior changes.

