# Model Selection Policy

## Principle

Use the least expensive model tier that can complete the task reliably. Escalate when ambiguity, risk, or complexity makes a stronger model materially more likely to produce a correct result.

This repository also relies on user-level Codex preferences in `C:\Users\georg\.codex\AGENTS.md` for general model and token efficiency. Project-specific rules in this repository remain the source of truth for the plugin factory workflow.

## Lightweight Tasks

Use a smaller or faster model for:

- formatting
- checklist completion
- simple file creation
- manifest field cleanup
- straightforward documentation edits
- narrow research lookups
- simple validation summaries

## Mid-Tier Tasks

Use a balanced model for:

- normal plugin implementation
- drafting skill instructions
- synthesizing research
- designing a simple plugin
- writing README sections
- reviewing small changes

## Strong-Model Tasks

Use a stronger model for:

- ambiguous product direction
- architecture and decomposition
- security or privacy review
- MCP/app integration design
- complex scripts
- multi-agent coordination
- final public-release review
- tasks where a mistake would create public embarrassment, data exposure, or significant rework

## Escalation Rules

Escalate when:

- requirements become unclear
- the task touches secrets, auth, permissions, or external services
- multiple systems interact
- test failures are hard to diagnose
- review identifies non-obvious risks
- public release quality is being judged

De-escalate when:

- the remaining work is mechanical
- the design is already decided
- the task has clear inputs and outputs
- verification is simple and local

## Agent Team Use

When using sub-agents, match each agent to its task:

- Research Scout can often use a lighter or mid-tier model.
- Design Reviewer usually needs mid-tier or strong depending on ambiguity.
- Build Worker depends on code complexity.
- Test Runner can often use mid-tier.
- Security Reviewer should use a strong model for non-trivial plugins.
- Release Reviewer should use mid-tier or strong depending on public visibility risk.

For cloud agents, use the same matching principle. Assign lighter models to background checklist or research tasks and stronger models to complex implementation, security review, or final release review.
