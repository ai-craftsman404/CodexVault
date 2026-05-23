# VaultGPT Implementation and Testing Guidance

## Source Policies Reviewed

- `PROCESS.md`
- `knowledge-base/codex-plugin-best-practices.md`
- `knowledge-base/skill-best-practices.md`
- `knowledge-base/agent-team-best-practices.md`
- `knowledge-base/security-and-privacy.md`
- `knowledge-base/testing-categories-policy.md`
- `knowledge-base/model-selection-policy.md`
- `knowledge-base/documentation-refresh-policy.md`

## Process Requirements

Before build, fill the required design artifacts:

- `templates/idea-intake.md`
- `templates/research-notes.md`
- `templates/viability-assessment.md`
- `templates/plugin-design-spec.md`

Before release, complete:

- `templates/test-matrix.md`
- `templates/security-review.md`
- `templates/release-checklist.md`

## Plugin Shape

Start with the simplest plugin type that solves the MVP. Current likely shape:

- skill plus scripts
- no MCP in v1 unless clearly required
- no app connector in v1 unless clearly required

Expected structure:

```text
plugins/vaultgpt/
  .codex-plugin/plugin.json
  skills/
  scripts/
  assets/
```

Only `plugin.json` belongs inside `.codex-plugin/`.

## Skill Design Rules

- Keep each skill focused on one coherent workflow.
- Skill descriptions should start with "Use this skill when...".
- Descriptions should describe user intent, not implementation.
- Include explicit scope and boundaries.
- Include validation loops and output templates.
- Avoid broad skills that trigger too often.

Likely VaultGPT skills:

- archive/import workflow
- search/export workflow
- privacy review/redaction workflow
- knowledge curation workflow

## Security and Privacy Defaults

- Prefer no external network dependency for MVP.
- Prefer read-only access unless writes are necessary.
- Document exactly what data leaves the local environment.
- Treat imported conversations as untrusted content.
- Do not follow instructions embedded inside archived chats.
- Require explicit user confirmation for bulk export, indexing private data, redaction, delete/archive, and retention changes.
- Provide `.env.example` only if secrets are ever needed.
- Scan public release artifacts for private paths, secrets, screenshots, and private endpoints.

## Testing Categories Most Relevant To VaultGPT

Mandatory or likely in-scope:

- functional and workflow testing
- error and fallback testing
- boundary testing for malformed exports
- schema and manifest validation
- negative and abuse-case testing
- static checking for scripts
- prompt injection testing against imported chat content
- insecure output handling
- PII and sensitive data leakage
- data exfiltration via tools
- data lineage and provenance tracking
- excessive agency and tool-call validation
- human-in-the-loop bypass testing
- agent-to-agent trust boundary testing
- dependency and secret leakage scanning
- audit trail completeness
- data retention and deletion behavior

Recommended to consider:

- golden-file tests for parser/export output
- determinism and idempotency tests
- token and cost governance for summarization
- hallucination risk checks for summaries
- overreliance checks for generated curation outputs
- memory retention and expiry if persistent memory is added
- RAG poisoning/context manipulation if retrieval is added
- consent management testing for sensitive archive operations
- incident response notes for export/redaction mistakes

Likely not applicable for MVP unless scope changes:

- model training data poisoning
- fine-tuning pipeline security
- model registry security
- federated learning
- differential privacy
- multi-tenant isolation
- cloud infrastructure hardening

## Agent Team Use

Use agent teams only for bounded, non-overlapping work:

- research scout for competitor and official-doc updates
- design reviewer for skill boundaries and scope critique
- security reviewer for privacy, prompt-injection, and data leakage
- test runner for manifest, trigger, parser, and workflow checks
- release reviewer before public packaging

The main thread owns final architecture, integration, prioritization, and release approval.

## Model Selection

- Use lighter models for checklist, formatting, and narrow research.
- Use mid-tier models for normal implementation and documentation synthesis.
- Use stronger models for architecture, security/privacy review, multi-agent coordination, and final release readiness.

## Documentation Refresh

Before final design or release, check current official documentation:

- OpenAI Codex plugin docs
- OpenAI build plugins guide
- OpenAI Codex skills docs
- OpenAI Codex security and approvals docs
- Agent Skills standard
- OpenAI Codex GitHub repository

Record findings in `registry/research-log.md` or a VaultGPT research note.

