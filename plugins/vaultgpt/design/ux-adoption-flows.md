# VaultGPT UX Adoption Flows

## Goal

VaultGPT should feel familiar to users of paid ChatGPT browser extensions while offering a safer, free, Codex-native workflow.

The product should minimize switching friction by mirroring familiar actions:

- save current chat
- organize into folders/tags/pins
- search everything
- bulk export or backup
- save and reuse prompts
- use variables
- run simple prompt chains
- attach/reference prior context
- review privacy before saving/exporting

## Competitor Patterns To Mirror

| Pattern | Competitor Signal | VaultGPT Design |
| --- | --- | --- |
| Sidebar/panel workflow | ChatGPT Toolbox, Superpower, Sider, Monica, Merlin, MaxAI | Use clear command/panel sections: Capture, Search, Prompts, Chains, Exports, Privacy, Audit |
| Folder tree and drag/drop | ChatGPT Toolbox, Superpower | Support folders/subfolders, breadcrumbs, counts, unfiled inbox, and bulk move |
| Checkboxes for bulk operations | ChatGPT Toolbox, Superpower | Use explicit bulk mode with selection tray, dry-run, undo, and confirmation |
| Global search shortcut | ChatGPT Toolbox, Superpower | Make search central with snippets, filters, and exact-message provenance |
| Folder-level ZIP export | ChatGPT Toolbox | Export selection, folder, tag, saved search, or full vault with manifest |
| Slash/typed prompt shortcuts | Superpower, Monica, Sider | Support simple aliases such as Save Chat, Search Vault, New Prompt, Use Prompt |
| Prompt variables as forms | AIPRM, Monica, ChatGPT Toolbox | Detect `{field}` or `{{field}}`, show compact form, preview final prompt |
| Prompt chains as steppers | ChatGPT Toolbox, Superpower | Use manual step-by-step chains with preview, pause, retry, and run log |
| Context chips | ChatGPT Toolbox, Sider, Monica | Make attached context visible, removable, and auditable |
| Selected text actions | Sider, MaxAI, Monica | Later support right-click/selection-first actions when feasible |

## MVP Command Surface

Use predictable command names:

- `vault.captureSelectedChat`
- `vault.search`
- `vault.organize`
- `vault.export`
- `vault.backup`
- `vault.prompt.new`
- `vault.prompt.use`
- `vault.prompt.chain`
- `vault.prompt.chain.run`
- `vault.privacyReview`
- `vault.auditLog`

User-facing aliases:

- Save Chat
- Search Vault
- Organize Vault
- Export Vault
- Backup Vault
- New Prompt
- Use Prompt
- New Chain
- Run Chain
- Privacy Check
- Activity Log

## First-Time User Journey

1. User opens ChatGPT in Chrome with Codex Chrome extension available.
2. User chooses `Save Chat`.
3. VaultGPT previews detected title, source, message count, estimated size, and capture scope.
4. User accepts default metadata or adds folder/tags.
5. VaultGPT runs privacy review.
6. User confirms save.
7. VaultGPT stores the chat locally and shows next actions: Search Vault, Create Prompt, Export, Audit Log.

Acceptance criterion:

```text
A first-time user can save a useful chat in under 30 seconds without reading documentation.
```

## Search Journey

1. User chooses `Search Vault`.
2. User enters a query.
3. Results are grouped by chats, prompts, chains, and exports.
4. Results show snippets, tags, source, date, and privacy status.
5. User opens the exact source or reuses the item.

Acceptance criterion:

```text
A returning user can find a saved chat or prompt in under 20 seconds.
```

## Organization Journey

1. User opens Organize Vault or selects items from search.
2. User creates folder/subfolder or chooses existing destination.
3. User applies tags or pins.
4. Bulk operation shows affected items and dry-run summary.
5. User confirms.
6. VaultGPT records audit event and offers undo for reversible changes.

## Export / Backup Journey

1. User chooses Export Vault or Backup Vault.
2. User chooses scope: selected items, folder, tag, saved search, prompts only, chats only, or full vault.
3. User chooses format: Markdown, JSON, ZIP.
4. VaultGPT runs privacy review.
5. User confirms export.
6. VaultGPT writes output with manifest, counts, skipped items, and audit event.

Acceptance criterion:

```text
A user can create a local backup in under 60 seconds with clear privacy status.
```

## Prompt Vault Journey

1. User chooses New Prompt or Save Current Prompt.
2. VaultGPT captures name, body, tags, and variables.
3. Variables are detected from `{field}` or `{{field}}`.
4. User saves prompt.
5. User later chooses Use Prompt, fills variable form, previews output, and inserts/copies/runs.

## Prompt Chain Journey

1. User chooses New Chain.
2. User adds prompt templates as ordered steps.
3. VaultGPT detects variables across all steps.
4. User previews chain.
5. User runs chain manually step by step.
6. Each step can pause, retry, skip, or stop.
7. VaultGPT records chain run in audit log.

## Privacy And Audit Journey

1. Any capture, export, backup, or destructive bulk action triggers privacy/safety review.
2. VaultGPT reports high/medium/low findings.
3. User can redact, exclude, save anyway, or cancel.
4. Override decisions are recorded.
5. Audit logs record actions without duplicating full sensitive content.

## Adoption Risks

- Capture ambiguity: users need to know exactly what is saved.
- Too much metadata slows first use.
- Search must be fast and trustworthy.
- Privacy warnings must avoid alert fatigue.
- Prompt variables must stay simpler than programming.
- Prompt chains must be transparent and manually confirmable.
- Export formats must be open and inspectable.
- Audit logs must not leak full sensitive content.

## Sources

- AI Toolbox Chrome Web Store: https://chromewebstore.google.com/detail/ai-toolbox-folders-prompt/jlalnhjkfiogoeonamcnngdndjbneina
- AI Toolbox site: https://www.ai-toolbox.co/
- AI Toolbox folders guide: https://www.ai-toolbox.co/chatgpt-folders
- AI Toolbox prompt guide: https://www.ai-toolbox.co/chatgpt-management-and-productivity/chatgpt-prompt-management-guide-2026
- AI Toolbox export guide: https://www.ai-toolbox.co/export-chatgpt-conversations
- Superpower Chat site: https://spchatgpt.com/
- Superpower Chrome Web Store: https://chromewebstore.google.com/detail/superpower-chat/amhmeenmapldpjdedekalnfifgnpfnkc
- Superpower release notes: https://www.superpowerdaily.com/p/superpower-chatgpt-5-0-0
- AIPRM variables: https://www.aiprm.com/en-au/tutorials/create-prompts/how-to-use-variables-in-prompts/
- Sider Context Menu: https://sider.ai/en/help-center//feature-guides/Context-Menu
- Monica Chat and Prompt Library: https://monica.im/help/Features/Chat
- Monica Webpage Summarization: https://monica.im/help/Features/Summarize/Summarize-Webpage

