# VaultGPT Plugin Design Spec

## Identity

- Plugin package name: vaultgpt
- Display name: VaultGPT
- Version: 0.1.0
- Description: Free ChatGPT power-extension features in a local-first Codex plugin with browser-assisted capture, search, organization, prompt workflows, privacy review, and audit logs.
- Repository: TBD
- License: TBD
- Keywords: chatgpt, archive, search, prompts, browser-capture, privacy, codex-plugin
- Category: productivity / knowledge-management

## Classification

- Type: skill plus scripts
- Reason: MVP needs Codex workflow guidance plus deterministic local operations for vault storage, indexing, search, export, and audit logs.

## MVP Workflows

| Workflow | Expected Behavior | Success Criteria |
| --- | --- | --- |
| Capture selected ChatGPT chat | Use Codex Chrome extension with explicit approval to capture current/selected chat content | User sees what is captured and content lands in local vault with provenance |
| Import export file | Import official ChatGPT export as fallback/batch source | Conversations normalize into vault without data loss for supported fields |
| Search vault | Full-text search across chats/prompts with filters | Results are fast, local, cited, and uncapped |
| Organize vault | Folders, tags, pins, bulk move/tag/archive/delete | Bulk actions support dry-run, confirmation, undo, and audit |
| Export/backup | Export selected/folder/all content to Markdown, JSON, ZIP | Export includes manifest and provenance |
| Prompt vault | Save prompts with variables and simple chains | Prompts can be searched, rendered, exported, and reused |
| Privacy review | Review sensitive content before capture/index/export | Findings are clear, cautious, and logged |

## Proposed Structure

```text
plugins/vaultgpt/
  .codex-plugin/plugin.json
  README.md
  CHANGELOG.md
  LICENSE
  skills/
    vaultgpt/
      SKILL.md
  scripts/
    vaultgpt/
  design/
  notes/
  tests/
```

## Scripts

| Script Area | Purpose |
| --- | --- |
| import | Parse official exports and selected captures |
| index | Build/rebuild local full-text index |
| search | Query vault index |
| organize | Manage folders, tags, pins, and bulk metadata |
| export | Produce Markdown, JSON, ZIP exports |
| prompt | Store/render prompt variables and simple chains |
| privacy | Detect sensitive data heuristically |
| audit | Append audit/provenance records |

## Agent Harness

- Use progressive visible governance.
- Show agent-team review for sensitive/bulk workflows only.
- Candidate roles: Archive Scout, Privacy Reviewer, Knowledge Curator, Search Indexer, Audit Agent.
- Main thread remains final planner and adjudicator.

## Definition Of Done For MVP

- Manifest valid and installable locally.
- Explicit and implicit skill triggers tested.
- Local vault can import sample data.
- Selected-chat capture path is documented and tested where available.
- Search, organization, export, prompt vault, privacy review, and audit workflows pass tests.
- Prompt-injection and sensitive-data leakage tests are included.
- Public README explains privacy model and limitations.
- `.gitignore` excludes private vault data and exports.

