# Plugin Design Spec

## Identity

- Plugin package name: premortemx
- Display name: PreMortemX
- Version: 0.1.0
- Description: Evidence-backed pre-mortem release gating plugin for Codex with auditable decisions, structured overrides, and an adaptive harness model.
- Developer name: TBD
- Repository: TBD
- License: TBD
- Keywords: pre-mortem, release-risk, evidence, harness, guardrails, auditability
- Category: project-management / release-governance

## Classification

- Type: skill plus scripts
- Reason for this type:
  - V1 should keep the user experience skill-first while still making the harness concept concrete through local scripts for scoring, records, and report generation.

## Complexity and Model Selection

- Overall complexity: high
- Recommended main-thread model tier: strong model for final design, security/privacy review, and release readiness decisions
- Recommended agent model tiers: mid-tier for bounded documentation, formatting, and mechanical script tasks; strong model for security/privacy or architecture review
- Escalation triggers:
  - Security/privacy storage design becomes ambiguous.
  - Harness/runtime design expands beyond local script orchestration.
  - Architecture-validation mode is pulled into v1.

## User Workflows

| Workflow | User Prompt | Expected Codex Behavior | Success Criteria |
| --- | --- | --- | --- |
| Release risk gating | "Run a pre-mortem on this release plan and tell me whether we should ship." | Gather the design-to-release bundle, classify likely release risks, validate claims against docs/code/test evidence, and return Pass/Warn/Block plus mitigation path. | User receives a clear, evidence-backed recommendation with readable summary and supporting details. |
| Change-risk review | "Assess this change set and test evidence for release blockers." | Review implementation summary, code context, and test evidence under the release-first model and surface credible blockers or warnings. | Risks are prioritized and supported by concrete evidence rather than generic concern. |
| Block override | "Override this block and record why." | Require structured override fields: rationale, mitigation steps, and responsible owner; store the event in per-run artifacts and registry history. | Override is auditable and usable for later quality review. |

## Plugin Structure

```text
plugins/<plugin-name>/
  .codex-plugin/plugin.json
  skills/
  assets/
  .mcp.json
  .app.json
```

## Manifest Plan

- `name`: premortemx
- `version`: 0.1.0
- `description`: Evidence-backed pre-mortem release gating for Codex with auditable decisions and adaptive guardrails.
- `skills`: PreMortemX core analysis skill
- `mcpServers`: none in v1
- `apps`: none in v1
- `interface.displayName`: PreMortemX
- `interface.shortDescription`: Release-first pre-mortem risk analysis with evidence and audit trails.
- `interface.longDescription`: PreMortemX helps Codex users stress-test releases before execution by combining pre-mortem reasoning, evidence validation, readable decision artifacts, and a lightweight harness for auditability and improvement.
- `interface.capabilities`: hybrid intake routing, release-first analysis, tiered outputs, structured overrides, local registry-linked artifacts
- `interface.defaultPrompt`: Assess upcoming work using evidence-backed pre-mortem reasoning. Start conservative, explain clearly, and escalate only with evidence.
- `interface.logo`: TBD
- `interface.composerIcon`: TBD
- `interface.screenshots`: TBD

## Skills

| Skill | Trigger Description | Scope | Scripts | References |
| --- | --- | --- | --- | --- |
| PreMortemX core analysis | Invoked explicitly for pre-mortem, release-risk, or blocker review, or implicitly when routing confidence supports release analysis | Release-first decision support using docs, code context, and test evidence | scoring/report/registry scripts | PRD, design-to-release bundle, local registry |

## Scripts

| Script | Purpose | Inputs | Outputs | Validation |
| --- | --- | --- | --- | --- |
| `score_run` | Rank risks and support rule-first recommendation explanations | Risk findings, evidence strength, uncertainty signals | Structured score data | Unit checks plus representative scenario fixtures |
| `write_report` | Produce readable tiered human-facing artifacts | Decision data, risk register, mitigation data | Summary and detailed report artifacts | Output template validation |
| `update_registry` | Append per-run record and aggregate history | Run metadata, override data, quality signals | Machine-readable run record and registry update | Schema validation |

## MCP and Apps

- MCP servers: none in v1
- App connectors: none in v1
- Authentication: no external authentication required for baseline local use
- Permissions:
  - Default conservative local scope
  - Adaptive approvals for broader access
  - Human approval required for any higher-permission broadening
  - Sensitive retained artifacts should be encryptable with a local-user-controlled key source

## Definition of Done

- [ ] Plugin installs locally.
- [ ] Manifest paths are valid and relative to plugin root.
- [ ] Skills trigger correctly.
- [ ] Example prompts work.
- [ ] Scripts are tested where applicable.
- [ ] Security and privacy review is complete.
- [ ] Public README is complete.
- [ ] Changelog and license are present.
- [ ] Release-first workflow passes representative scenario tests.
- [ ] Structured Block override flow is implemented and recorded correctly.
- [ ] Registry-linked bundle artifacts are readable and machine-validated.
- [ ] Privacy-first retention and adaptive approval behavior are documented.
- [ ] Each shipped feature/task has explicit acceptance criteria.
- [ ] Adversarial evaluator scenarios are defined and pass for false positives, missed risks, weak-evidence cases, and override handling.

## Roadmap

- V1 (`0.1.x`):
  - Ship release-first workflow only.
  - Deliver skill plus scripts packaging with tiered outputs and registry-linked bundle records.
  - Support structured Block override, adaptive approvals, optional sensitive-artifact encryption, and local-first operation.
- V2 (`0.2.x`):
  - Ship architecture-validation mode.
  - Expand harness memory and boundary-recommendation behavior.
  - Improve registry/report schemas and quality review workflows.
  - Evaluate optional AgentFS-like or AgentFS-backed isolation support if stable enough.
- V3 (`0.3.x` or later):
  - Broaden into a multi-mode decision harness across release, architecture, and change-risk use cases.
  - Add stronger trend analysis, calibration workflows, and organization-ready governance/reporting patterns.
  - Refine permission models, review checkpoints, and optimization loops using accumulated run history.

## Long-Term Product Goal

- PreMortemX should evolve from a release-risk plugin into a trusted evidence-backed decision harness for Codex workflows.
- The system should stay readable for humans, conservative by default, and adaptive through structured learning rather than opaque automation.
- The long-term deliverable is a repeatable, inspectable, and human-governed decision layer that improves risk judgment over time.

## Evaluation Approach

- Development and release validation should follow task/feature-level acceptance criteria.
- PreMortemX should use adversarial evaluator patterns as part of TDD/TDLC validation, especially for:
  - false-positive pressure tests
  - missed-risk detection tests
  - weak or conflicting evidence cases
  - structured Block override handling
  - sensitive-data retention and protection recommendations
- Release readiness requires both functional correctness and judgment-quality evaluation, not just happy-path execution.

## Agent Team Plan

- Agent team needed: no
- Reason:
  - Current work is still in intake/spec stage and does not yet require parallel implementation.
- Planned roles:
  - None for current stage.
- Non-overlapping file ownership:
  - Not applicable yet.
