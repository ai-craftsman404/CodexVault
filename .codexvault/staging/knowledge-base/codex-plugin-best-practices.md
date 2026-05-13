# Codex Plugin Best Practices

## Source Priority

Prefer current official documentation when designing plugins:

- OpenAI Codex plugin documentation: https://developers.openai.com/codex/plugins
- OpenAI Codex build plugins guide: https://developers.openai.com/codex/plugins/build
- OpenAI Codex skills documentation: https://developers.openai.com/codex/skills
- OpenAI Codex security and approvals documentation: https://developers.openai.com/codex/agent-approvals-security
- Agent Skills standard: https://agentskills.io/
- OpenAI Codex GitHub repository: https://github.com/openai/codex

Record research dates because Codex plugin publishing and capabilities are evolving.

## Design Principles

- Start skill-first when a reusable workflow is the core value.
- Package as a plugin when distribution, install metadata, app integrations, MCP servers, assets, or multiple skills matter.
- Use the smallest plugin type that solves the real problem.
- Make the manifest public-ready even for early releases.
- Keep plugin names stable, lower-case, and kebab-case.
- Keep manifest paths relative to the plugin root and starting with `./`.

## Structure

```text
plugin-name/
  .codex-plugin/plugin.json
  skills/
  assets/
  .mcp.json
  .app.json
```

Only `plugin.json` belongs inside `.codex-plugin/`.

## Manifest Checklist

- `name`
- `version`
- `description`
- `author`
- `repository`
- `license`
- `keywords`
- `skills`
- `mcpServers` if applicable
- `apps` if applicable
- `interface.displayName`
- `interface.shortDescription`
- `interface.longDescription`
- `interface.developerName`
- `interface.category`
- `interface.capabilities`
- `interface.defaultPrompt`
- visual assets when useful

## Public Release Notes

Self-serve publishing to the official Codex Plugin Directory should be treated as evolving. Until that path is fully available, public GitHub packaging is the main distribution and visibility channel.
