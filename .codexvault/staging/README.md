# Code Plugin Guru

Code Plugin Guru is a Codex plugin factory line: a repeatable workspace for turning plugin ideas into high-quality, public-ready Codex plugins.

The project is designed to support frequent plugin development across different purposes while keeping the process consistent, auditable, and easy to improve.

## Factory Workflow

Every plugin idea moves through the same lifecycle:

0. Complexity and Model Selection
1. Idea Intake
2. Research and Differentiation
3. Viability Scoring
4. Plugin Type Classification
5. Design Spec
6. Agent Team Option
7. Build
8. Test Matrix
9. Security and Privacy Review
10. Public Release Packaging
11. Versioned Release
12. Maintenance Loop

## New Session Intake

Each new chat session should begin by asking for the next Codex plugin idea in a concise way:

```text
Ready for the next Codex plugin idea. Please share the brief concept, target user, and what you want Codex to do differently when the plugin is installed.
```

## Repository Structure

```text
Code-Plugin-Guru/
  PROCESS.md
  templates/
  knowledge-base/
  registry/
  plugins/
  research/
  releases/
```

- `templates/` contains reusable intake, design, review, and release templates.
- `knowledge-base/` captures Codex plugin, skill, security, and publishing guidance.
- `registry/` tracks candidate plugins, released plugins, and research assumptions.
- `plugins/` is the workspace for plugin implementations.
- `research/` stores per-plugin research notes.
- `releases/` stores per-plugin public-readiness notes.

## Model Efficiency

The factory dynamically assesses task complexity and chooses an appropriate ChatGPT/Codex model. The goal is to preserve quality while avoiding unnecessary token and model-cost spend.

Use stronger models for high-ambiguity design, security/privacy review, complex implementation, and final release review. Use lighter models for narrow research, formatting, checklist completion, simple documentation, and mechanical edits.

## Agent Teams

For larger plugins, the factory can use Codex sub-agents or cloud agents as a small production team. Typical roles are Research Scout, Design Reviewer, Build Worker, Test Runner, Security Reviewer, and Release Reviewer.

Agent teams and cloud agents are optional. The main local session owns final architecture, integration, and release decisions.

## Default Strategy

Build skill-first where possible. Package as a Codex plugin when the workflow benefits from installable distribution, multiple skills, app integrations, MCP server configuration, scripts, assets, or public GitHub release positioning.

Finished plugins may remain in this factory repo during development, then move into dedicated public GitHub repositories when they are polished enough to stand alone.

## Documentation Refresh

Codex plugin capabilities and related documentation change over time. Review official docs and relevant ecosystem changes every four weeks by default, or bi-weekly during active release work, and record findings in `registry/research-log.md`.
