# Plugin Idea Intake

## Summary

- Working name: PreMortemX
- One-line description: Evidence-backed pre-mortem decision plugin for release risk gating, with a lightweight harness for auditability, adaptive guardrails, and continuous improvement.
- Target user: Primary target user remains flexible, but v1 is optimized for release decision-makers working around code changes, release plans, and implementation artifacts.
- User problem: Teams and individual builders miss important pre-release risks or overreact to weak, anxiety-driven concerns. They need a disciplined way to surface credible blockers, explain them clearly, and preserve human override.
- Desired outcome: Improve release decision quality with clear Pass/Warn/Block recommendations, evidence-backed rationale, and a feedback loop that reduces missed risks and false positives over time.

## Expected Codex Behavior

- What should Codex do differently when this plugin is installed?
  - Run a hybrid intake flow: auto-detect likely mode first, then ask targeted setup questions when confidence is low.
  - Focus v1 on release risk gating using a design-to-release bundle: design or PRD context, implementation summary, and release plan.
  - Separate analysis internals from human-facing outputs, keeping artifacts intuitive, easy to read, and semi-technical/non-technical where appropriate.
  - Return a three-state decision model: Pass, Warn, or Block, with structured human override support for Block.
  - Keep a local audit trail and per-run artifacts that support later quality review and harness optimization.
- What should Codex avoid doing?
  - Avoid unsupported blocking decisions based on weak evidence.
  - Avoid broad filesystem or runtime access without explicit escalation.
  - Avoid storing more sensitive detail than necessary by default.
  - Avoid shipping architecture validation as a full v1 mode; define it, but defer it.
- Example user prompts:
  - "Run a pre-mortem on this release plan and tell me whether we should ship."
  - "Assess this change set, test evidence, and rollout plan for release blockers."
  - "Give me a plain-language summary of the top risks and what we should do next."

## Scope

- MVP capabilities:
  - Release-first analysis mode with hybrid intake routing.
  - Evidence policy limited to docs, code context, and test evidence.
  - Tiered outputs with a decision-focused top summary and deeper evidence/risk sections.
  - Structured override flow requiring rationale, mitigation steps, and responsible owner.
  - Local registry plus per-run artifacts for audit and optimization history.
  - Adaptive approvals and conservative guardrail recommendations that can broaden only with human approval.
- Out of scope for v1:
  - Full architecture-validation mode shipped as a production-ready workflow.
  - Mandatory external services or cloud storage.
  - Automatic self-loosening guardrails without human approval.
  - Dependence on AgentFS as a required runtime component.
- Future possibilities:
  - V2: architecture validation mode, stronger artifact schemas, and richer guardrail memory/recommendation behavior.
  - V2: optional AgentFS-like or AgentFS-backed isolation pattern if runtime maturity is acceptable.
  - V3: broader multi-mode decision support across release, architecture, and change-risk workflows.
  - V3: stronger harness calibration, quality-trend analysis, and more mature permission/review patterns.
  - Ultimate direction: a trusted Codex-native decision harness that improves over time while staying evidence-backed, inspectable, and human-governed.

## Inputs and Outputs

- Inputs Codex needs:
  - Design or PRD document.
  - Implementation summary or code change context.
  - Release plan and rollout notes.
  - Test, lint, or build evidence where available.
- Outputs Codex should produce:
  - Tiered, decision-focused summary with verdict, recommendation, blockers, mitigation path, and confidence band.
  - Structured risk register with evidence and mitigation detail.
  - Machine-readable per-run record linked into a local registry.
- Files, services, or systems involved:
  - Local workspace artifacts and generated plugin records.
  - No external service is required for v1.

## Dependencies

- Skills:
  - Core PreMortemX analysis skill.
- Scripts:
  - Scoring, record generation, registry update, and report generation scripts.
- MCP servers:
  - None required for v1.
- App connectors:
  - None required for v1.
- External APIs:
  - None required for v1.
- Secrets or credentials:
  - None required for baseline local use.
  - Optional local-user-controlled secret or key source if sensitive retained artifacts are encrypted.

## Public Positioning

- GitHub repository name: premortemx
- Display name: PreMortemX
- Short description: Evidence-backed pre-mortem release gating for Codex, with auditable decisions and adaptive guardrails.
- Target audience: Developers, leads, and release decision-makers who want structured, explainable release-risk analysis inside Codex workflows.
- Why this should exist: Existing pre-mortem concepts help teams think better, but they often stop at facilitation. PreMortemX aims to turn that reasoning into a repeatable, evidence-backed, inspectable decision system with a practical harness and improvement loop.

## Open Questions

- Question: What exact file/folder naming convention should the registry-linked bundle use?
- Owner: Spec phase
- Resolution: To be finalized during design-spec detailing.
- Question: What exact fields should the machine-readable run record contain?
- Owner: Spec phase
- Resolution: To be finalized during design-spec detailing.
- Question: What exact test scenarios should be required for the release bar?
- Owner: Spec phase
- Resolution: To be finalized during test-matrix drafting.

## Roadmap

- V1:
  - Release-first pre-mortem plugin with hybrid intake routing.
  - Design-to-release evidence bundle using docs, code context, and test evidence.
  - Tiered human-facing outputs plus machine-readable registry-linked records.
  - Structured Block override with rationale, mitigation, and owner.
  - Privacy-first retention, adaptive approvals, and conservative default scope.
- V2:
  - Add architecture-validation mode as a supported workflow.
  - Strengthen run-record schemas, registry trend views, and quality-signal review flows.
  - Improve harness memory around boundaries, exceptions, and recommended permission expansions.
  - Explore optional isolation backend improvements such as AgentFS-like runtime support.
- V3:
  - Expand to a broader multi-mode decision platform across release, architecture, and change-risk analysis.
  - Improve calibration and optimization workflows using accumulated quality signals and outcome reviews.
  - Introduce more mature governance patterns for organization/team use while preserving local-first usability.
- Ultimate goals and deliverables:
  - A Codex-native evidence-backed decision harness, not just a prompt skill.
  - Reusable decision artifacts that are understandable by semi-technical and non-technical stakeholders.
  - A human-governed system that reduces missed risks, controls false positives, and improves confidence over repeated use.
