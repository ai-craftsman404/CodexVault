# CodexVault

CodexVault is a workspace resilience and restoration plugin for Codex.

Current roadmap line: `v1a`

It is designed to:

- discover workspace and environment state
- generate normalized manifests
- create integrity-checked snapshot artifacts
- guide restore planning and validation
- use Codex agent-team orchestration as a core QA and simulation differentiator
- use Codex subagents and agent-team workflows wherever they materially improve build and testing throughput

## MVP rules

- secrets are redacted by default
- destructive restore actions require human approval
- scheduling is out of MVP
- validation is tiered and does not overstate restore success
- temp-dir partial restore is allowed only in isolated, plugin-managed space
- agent-team simulation is part of the product value proposition

## Structure

```text
plugins/codexvault/
  .codex-plugin/plugin.json
  skills/
  assets/
```

## Status

This plugin is scaffolded for spec and test work. Implementation work should follow the agreed MVP rules in `research/codexvault/`.

## Release wording

Use concise, release-safe wording such as:

- highlights-only, action-first, human-gated restore workflow
- simulation exposes failure modes without performing destructive actions
- strict allowlist and isolated temp-dir restore behavior
