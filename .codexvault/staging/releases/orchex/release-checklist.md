# Release Checklist

## Plugin

- Plugin name: orchex
- Version: 0.1.0
- Release date: 2026-04-30
- Release owner: Codex main thread

## Required Files

- [x] `.codex-plugin/plugin.json`
- [x] `README.md`
- [x] `LICENSE`
- [x] `CHANGELOG.md`
- [x] `.gitignore`
- [ ] `.env.example` if secrets are required
- [x] Skills under `skills/` if applicable
- [x] Scripts under `scripts/` if applicable
- [x] Assets under `assets/` if applicable
- [ ] `.mcp.json` if MCP servers are included
- [ ] `.app.json` if app connectors are included

Notes:
- `.env.example` is not required because Orchex does not require plugin-owned secrets.
- `.mcp.json` and `.app.json` are intentionally absent in V1.

## Documentation

- [x] Clear description
- [x] Installation instructions
- [x] Usage examples
- [x] Example prompts
- [x] Configuration instructions
- [x] Known limitations
- [x] Security and privacy notes
- [x] Troubleshooting section

## Quality Gates

- [x] Complexity and model selection considered.
- [x] Viability assessment complete
- [x] Design spec complete
- [ ] Test matrix passed
- [ ] Security review complete
- [x] No secrets or private data
- [x] License and attribution clear
- [x] Version and changelog updated

## GitHub Presentation

- [x] Repository description
- [x] Topics
- [x] README opening is clear
- [x] Screenshots or diagrams where useful
- [x] Public examples do not depend on private resources

Notes:
- Repository description and topic recommendations are prepared in `releases/orchex/github-metadata.md`.
- A workflow diagram is now included in the plugin README.
- Live Codex screenshots are still pending runtime verification.

## Release Notes

```markdown
## v0.1.0

- Initial release candidate.
- Includes:
  - deterministic workflow governance
  - role skills
  - artifact, stage, run-integrity, and ownership validation
  - synthetic and realistic E2E coverage
- Known limitations:
  - live Codex runtime verification still pending
  - prompt-injection coverage incomplete
```
