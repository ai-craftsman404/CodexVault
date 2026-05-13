# Code Plugin Guru Instructions

This repository is a Codex plugin factory line. Use it to evaluate, design, build, test, review, and prepare public-ready Codex plugins.

## Operating Model

For each plugin idea, follow the process in `PROCESS.md`:

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

## New Session Greeting

At the start of a new chat session in this project, greet the user briefly and ask for the next Codex plugin idea. Keep the prompt concise and intake-oriented.

Suggested greeting:

```text
Ready for the next Codex plugin idea. Please share the brief concept, target user, and what you want Codex to do differently when the plugin is installed.
```

If the user provides only a partial idea, proceed with intake and identify gaps rather than asking for a full specification upfront.

## Defaults

- Dynamically assess task complexity and choose the least expensive model tier that can complete the task reliably.
- Prefer skill-first designs unless the plugin clearly needs MCP, apps, scripts, or assets.
- Use the simplest plugin type that solves the problem.
- Keep each plugin under `plugins/<plugin-name>/` during factory development.
- Use lower-case kebab-case plugin package names.
- Treat every plugin as potentially public from the start.
- Do not commit secrets, private paths, private screenshots, or private service details.
- Use agent teams only when the work can be split into bounded, non-overlapping tasks.

## Testing Categories Rule

All development in this project must consider the testing categories in `knowledge-base/testing-categories-policy.md`.

Apply them intelligently:

- every relevant `Mandatory` category must be covered or explicitly justified as not applicable
- every `Recommended` category must be considered and either covered, deferred with reason, or marked not applicable
- `Optional` categories should be used when the plugin context, release risk, or deployment model justifies them
- testing decisions must be reflected in the test matrix and other release artifacts where relevant

Do not treat this as a box-ticking exercise. The rule is comprehensive relevance assessment, not blind execution of every category on every change.

## Progress Summary Rule

Keep a compact progress summary visible in the chat during active work and refresh it as status changes materially.

The in-chat summary should normally include:

- current status
- completed work
- work in progress
- pending work
- latest verification result

Use the file-backed tracker as the source of truth when available, and mirror its current state in the chat rather than inventing a separate status system.

## Required Artifacts

Before building a plugin, create or fill:

- `templates/idea-intake.md`
- `templates/research-notes.md`
- `templates/viability-assessment.md`
- `templates/plugin-design-spec.md`

Before release, complete:

- `templates/test-matrix.md`
- `templates/security-review.md`
- `templates/release-checklist.md`

## Quality Bar

A plugin is not release-ready until:

- the manifest is valid
- local install or discovery has been tested
- explicit and implicit skill invocation are tested where applicable
- relevant mandatory testing categories from `knowledge-base/testing-categories-policy.md` have been covered or explicitly justified as not applicable
- public documentation is clear
- security and privacy review is complete
- release version and changelog are updated

## Research Rule

Codex plugin capabilities are evolving. Before final design or release, check current official OpenAI Codex plugin, skills, and security documentation, then record assumptions in `registry/research-log.md` or a per-plugin research note.

## Documentation Refresh Rule

Review official Codex plugin, build, skills, security, Agent Skills, and relevant ecosystem documentation every four weeks by default, or bi-weekly during active release work. Record findings in `registry/research-log.md` and update the factory process if guidance changes.

## Agent Team Rule

When sub-agents or cloud agents are used, the main thread must:

- define the goal and success criteria
- assign narrow roles
- avoid overlapping file ownership
- keep final architecture and integration decisions local
- review agent outputs before release

Use `templates/agent-team-plan.md` for coordination.

Cloud agents are best for background research, bounded implementation, test passes, release review, and security/privacy review. Do not delegate final architecture or release approval to a cloud agent.

## Harness Differentiation Rule

For `PreMortemX`, the use of:

- agent teams
- orchestrated adjudication
- governed workflow/runtime harness behavior
- auditable execution control

is a core product differentiator, not an incidental implementation detail.

Therefore, future `PreMortemX` design and roadmap decisions should:

- preserve the visibility of the agent-team and harness model wherever it materially improves the product
- prefer features that make the governed harness more understandable, usable, and defensible
- avoid generic feature design that could dilute `PreMortemX` into a simple prompt or report generator
- treat the harness as part of the product surface and moat, not only as hidden internal plumbing

When evaluating new `PreMortemX` features, explicitly ask:

- does this strengthen or clarify the agent-team model?
- does this strengthen or clarify the governed harness?
- does this make those differentiators more visible to users?

If the answer is no, challenge the feature direction before proceeding.

## Model Selection Rule

Use smaller or faster models for bounded, low-risk, mechanical tasks. Use stronger models for:

- unclear requirements
- architecture decisions
- security and privacy review
- complex implementation
- multi-agent coordination
- final release readiness review

If a task is delegated to a sub-agent, match the sub-agent model to the task complexity. Avoid overusing frontier models for simple checklist, formatting, or file-organization work.
