# Codex Plugin Factory Process

This process is the standard operating framework for developing Codex plugins in this repository.

## 0. Complexity and Model Selection

Before substantial work, classify task complexity and choose the least expensive model tier that can handle the work reliably.

Use this step for:

- plugin idea assessment
- research
- design
- implementation
- reviews
- tests
- release preparation

Default principle: use stronger models for ambiguous architecture, security-sensitive work, complex code, or final reviews; use smaller or faster models for narrow, mechanical, low-risk tasks.

Record the decision when it materially affects cost, quality, or task delegation.

Use `templates/model-selection.md`.

## New Session Intake

When a new chat session starts in this project, begin with a short intake prompt for the next plugin idea. Ask for:

- brief concept
- target user
- desired Codex behavior

Do not require a full specification before starting the intake process.

## Progress Visibility

During active work, keep a short progress summary visible in the chat and refresh it when the status changes materially.

Default summary fields:

- status
- completed
- in progress
- pending
- latest verification result

When a file-backed tracker exists for the current plugin, treat that tracker as the source of truth and mirror it in chat updates.

## 1. Idea Intake

Capture the plugin concept before implementation:

- target user
- user problem
- expected Codex behavior
- required tools, APIs, apps, MCP servers, scripts, or assets
- public GitHub positioning
- MVP scope
- explicit non-goals

Use `templates/idea-intake.md`.

## 2. Research and Differentiation

Check current official Codex documentation and relevant ecosystem examples before design. Record:

- official docs reviewed
- similar OpenAI curated plugins
- similar GitHub repositories
- similar MCP servers or agent skills
- meaningful differentiator
- dated assumptions

Use `templates/research-notes.md`.

## 3. Viability Scoring

Score the plugin before building:

- usefulness
- uniqueness
- feasibility
- maintenance cost
- security and privacy risk
- GitHub visibility value

Use `templates/viability-assessment.md`.

## 4. Plugin Type Classification

Classify the plugin early:

- skill-only
- skill plus scripts
- skill plus MCP
- skill plus app connector
- full multi-capability plugin

Prefer the simplest type that solves the user problem.

## 5. Design Spec

Define the implementation contract:

- plugin name and display name
- manifest metadata
- bundled skills
- scripts and assets
- app or MCP configuration
- default prompts
- install and usage flow
- success criteria
- definition of done

Use `templates/plugin-design-spec.md`.

## 6. Agent Team Option

For larger or time-sensitive plugins, use a small agent team or cloud agents to parallelize bounded workstreams.

Use this option when:

- research questions are independent
- implementation can be split across different files or modules
- testing can run while build work continues
- security or release review can happen in parallel
- background work can continue while the main local session keeps architecture control

Avoid this option when:

- the plugin is small enough for one direct pass
- tasks are vague or tightly coupled
- multiple agents would need to edit the same files
- the main architecture is not yet clear

The main thread owns final architecture, prioritization, integration, and release decisions.

Standard roles:

- Research Scout: checks current docs, similar plugins, ecosystem examples, and differentiation.
- Design Reviewer: reviews plugin architecture, skill boundaries, manifest plan, and scope.
- Build Worker: implements a clearly bounded part of the plugin with explicit file ownership.
- Test Runner: runs install, manifest, trigger, script, and example-prompt tests.
- Security Reviewer: reviews secrets, permissions, network use, prompt-injection risk, and public leakage.
- Release Reviewer: reviews README, examples, changelog, license, GitHub positioning, and release readiness.

Cloud agents are appropriate for longer background tasks, large research sweeps, bounded implementation work, test passes, and independent reviews. The main local session remains responsible for architecture, integration, conflict resolution, and final release decisions.

Use `templates/agent-team-plan.md`.

## 7. Build

Scaffold and implement the plugin under `plugins/<plugin-name>/`.

During build, use `knowledge-base/testing-categories-policy.md` to decide which testing categories must shape the implementation, interfaces, safeguards, and definition of done. Do not wait until the end of the process to consider testing scope.

Expected plugin shape:

```text
plugins/<plugin-name>/
  .codex-plugin/plugin.json
  skills/
  .mcp.json
  .app.json
  assets/
```

Only `.codex-plugin/plugin.json` belongs inside `.codex-plugin/`. Keep skills, assets, MCP config, and app config at the plugin root.

## 8. Test Matrix

Validate behavior before release:

- manifest paths
- local install
- explicit plugin or skill invocation
- implicit skill trigger
- wrong-trigger prompts
- scripts and failure behavior
- app or MCP setup
- sandbox and no-network behavior
- Windows path behavior where relevant

Use `knowledge-base/testing-categories-policy.md` as the coverage baseline for the matrix:

- apply every relevant `Mandatory` category
- assess every `Recommended` category and record cover, defer, or not-applicable decisions
- add `Optional` categories where the plugin risk profile justifies them
- record why any category is out of scope instead of silently omitting it

Use `templates/test-matrix.md`.

## 9. Security and Privacy Review

Review:

- secrets
- external services
- network usage
- destructive actions
- local file access
- generated scripts
- app connector permissions
- MCP tool permissions
- prompt-injection exposure
- privacy and terms links

Use `templates/security-review.md`.

The security and privacy review must be consistent with the testing category decisions already made in `knowledge-base/testing-categories-policy.md`, especially for prompt attack, tool use, memory, retrieval, identity, data leakage, infrastructure, and compliance categories.

## 10. Public Release Packaging

Prepare the public-facing repository or release folder:

- `README.md`
- `LICENSE`
- `CHANGELOG.md`
- `.gitignore`
- `.env.example` if needed
- screenshots, icon, or logo where useful
- installation instructions
- example prompts
- limitations
- GitHub topics

Use `templates/release-checklist.md`.

## 11. Versioned Release

Default versioning:

- `0.1.0`: first usable MVP
- patch version: fixes and documentation corrections
- minor version: new skills, workflows, or capabilities
- major version: breaking changes

Every public release should update the changelog.

## 12. Maintenance Loop

After release:

- capture user feedback
- track known issues
- monitor Codex plugin documentation changes
- maintain compatibility notes
- schedule improvements
- log future ideas

Use `registry/released-plugins.md` and per-plugin notes under `releases/`.

## Documentation Refresh Cadence

Review current documentation and ecosystem changes every four weeks by default, or bi-weekly for active plugin releases.

Check:

- OpenAI Codex plugin docs
- OpenAI Codex build plugins guide
- OpenAI Codex skills docs
- OpenAI Codex security and approvals docs
- Agent Skills standard
- OpenAI Codex GitHub releases or notable changes
- relevant MCP, app connector, and marketplace changes

Record results in `registry/research-log.md`. If changes affect the factory process, update `PROCESS.md`, `AGENTS.md`, templates, or `knowledge-base/` files.
