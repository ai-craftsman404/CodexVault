# VaultGPT Script Tests

Run from `plugins/vaultgpt/scripts/vaultgpt`:

```powershell
python -m unittest discover -s tests
```

Current synthetic fixture coverage includes:

- cross-platform vault path resolution
- vault initialization and append-only audit events
- prompt variables, rendering, import, and export
- selected-chat normalization with unknown model labels
- official ChatGPT export mapping-shape import
- JSON fallback search
- optional SQLite FTS5 rebuild/search when available
- folders, tags, pins, saved searches, and bulk dry-run plans
- Markdown, JSON, and ZIP export manifests
- heuristic privacy warnings and redaction
- manual prompt chains and chat-to-prompt candidates

Live Codex Chrome selected-chat capture still requires manual verification before release.
