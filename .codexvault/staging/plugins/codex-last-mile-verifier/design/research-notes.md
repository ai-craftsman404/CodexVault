# Research Notes

## Official documentation reviewed

- 2026-05-04: OpenAI Academy, "Plugins and skills"
- 2026-05-04: OpenAI Help, "Skills in ChatGPT"
- 2026-05-04: OpenAI Help, "Using Codex with your ChatGPT plan"

## Key takeaways

- Current official guidance distinguishes plugins from skills clearly: use plugins to package connected capabilities and skills to encode reusable process.
- Codex exposes plugin and skill discovery surfaces in the runtime UI, which makes live discovery and install checks a legitimate final-mile workflow.
- Workspace controls and RBAC can block plugin access, so the verifier must support `blocked` outcomes rather than assuming every failure is a product defect.
- Skills are reusable and installable, but they do not sync across products automatically, so real runtime confirmation still matters.

## Ecosystem positioning

- Different from static manifest validators because it focuses on observed runtime behavior.
- Different from general QA checklists because it is Codex-extension specific and artifact-driven.
- Best v1 shape remains `skill plus scripts`, not a connector-heavy plugin.

## Dated assumptions

- Assumption date: 2026-05-04
- Assumption: A reusable guided workflow is the safest v1 because Codex runtime behavior and workspace controls may vary across environments.
- Assumption: Optional browser or UI assistance can be layered later without making v1 depend on automation.
