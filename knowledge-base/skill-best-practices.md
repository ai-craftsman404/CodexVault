# Skill Best Practices

## Purpose

Skills are the authoring format for reusable Codex workflows. Plugins are the installable distribution unit.

## Trigger Description

The `description` field is critical because Codex uses it to decide whether to load the skill.

Good descriptions:

- start with "Use this skill when..."
- describe user intent, not internal implementation
- include common trigger words
- define scope and boundaries
- stay concise

## Scope

- A skill should cover one coherent workflow.
- Avoid broad skills that activate too often.
- Avoid tiny skills that require many skills to load for one task.
- Include project-specific or domain-specific knowledge that Codex would otherwise miss.

## Content

Use:

- step-by-step procedures
- gotchas
- output templates
- validation loops
- explicit defaults
- references loaded only when needed
- scripts for repeatable logic

Avoid:

- generic best-practice filler
- long background explanations
- large copied documentation
- menus of equal options without a default

## Testing

Create trigger test prompts:

- should trigger
- should not trigger
- explicit invocation
- ambiguous but relevant
- similar but out-of-scope

For output quality, run the skill against real tasks and revise based on execution traces, not only final answers.

