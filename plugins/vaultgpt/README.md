# VaultGPT

VaultGPT is a free, local-first Codex plugin designed to replace paid ChatGPT power-extension workflows without relying on opaque third-party browser extensions.

## MVP Focus

- Codex Chrome selected-chat capture with explicit approval
- Official ChatGPT export import as fallback and batch source
- Full-text local search
- Unlimited folders, subfolders, tags, and pins
- Unfiled inbox
- Saved searches
- Bulk export and backup to Markdown, JSON, and ZIP
- Prompt vault with variables
- Manual prompt chains
- Convert chat to prompt or chain
- Privacy review before save/index/export
- Audit logs and provenance manifests

## Positioning

VaultGPT gives ChatGPT power-extension features for free, without forcing users to trust a third-party browser extension with their AI history.

## Status

Design and scaffold stage. Implementation is not complete yet.

## Privacy Model

VaultGPT is intended to be local-first. Runtime vault data, ChatGPT exports, and generated backups should not be committed to git.

Captured and imported chats are treated as untrusted content. VaultGPT should not follow instructions embedded inside archived chats.

## Development Notes

See:

- `design/architecture.md`
- `design/mvp-task-breakdown.md`
- `design/test-matrix.md`
- `design/ux-adoption-flows.md`

