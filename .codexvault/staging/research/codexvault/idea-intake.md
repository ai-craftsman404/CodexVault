# Plugin Idea Intake

## Summary

- Working name: CodexVault
- One-line description: A Codex-native workspace resilience plugin for deterministic discovery, snapshotting, restoration, validation, and recovery of AI-assisted development environments.
- Target user: Developers and technical operators who rely on Codex workspaces and need repeatable recovery across machines or OSes.
- User problem: Workspace rebuilds are brittle because environment state, local configuration, and tool/runtime drift are hard to reconstruct reliably.
- Desired outcome: Help Codex capture normalized workspace state, create portable restoration artifacts, and guide safe recovery with validation and human checkpoints.

## Expected Codex Behavior

- What should Codex do differently when this plugin is installed?
  - Discover workspace and environment state before acting.
  - Build normalized manifests and snapshot records instead of treating the workspace as an opaque file tree.
  - Prefer guided restore workflows with validation, dry-run simulation, and explicit approval before risky changes.
  - Surface runtime, package manager, shell, and MCP mismatch issues with remediation guidance.
- What should Codex avoid doing?
  - Avoid claiming full machine-level backup or recovery coverage if the plugin can only observe and reconstruct workspace-level state.
  - Avoid destructive restore actions without preview, checkpointing, and rollback semantics.
  - Avoid capturing secrets or sensitive environment values by default.
  - Avoid implying it can guarantee deterministic reconstruction for every dependency outside the workspace boundary.
- Example user prompts:
  - "Back up this Codex workspace and make sure I can restore it later."
  - "Restore my workspace on this machine from the last known good snapshot."
  - "Validate whether this workspace can be reconstructed on Windows from the manifest."

## Scope

- MVP capabilities:
  - Environment discovery for OS, shell, Codex paths, package managers, Git repos, project structure, and MCP topology.
  - Workspace manifest generation with normalized metadata and schema versioning.
  - Snapshot creation with checksums, corruption detection, and portable archive packaging.
  - Guided restore orchestration with dry-run, selective restore, rollback checkpoints, and human approval gates.
  - Runtime and dependency verification with remediation guidance.
  - Validation reports and confidence scoring.
- Out of scope for v1:
  - Guaranteed full-machine backup and bare-metal recovery.
  - Cloud sync or team-shared workspace state.
  - Autonomous repair without approval for destructive actions.
  - Heavy enterprise policy management or multi-tenant governance.
- Future possibilities:
  - Scheduled backups and pre-change backup hooks.
  - Snapshot diff visualization and provenance metadata.
  - Conflict resolution modes for partially existing destinations.
  - Minimal disaster recovery bootstrap mode.
  - Optional stronger encryption and signing workflows.

## Inputs and Outputs

- Inputs Codex needs:
  - Current workspace path and user confirmation.
  - Environment variables, shell identity, runtime versions, Git state, and package manager state.
  - Optional restore target and restore policy.
- Outputs Codex should produce:
  - Workspace manifest.
  - Snapshot archive and integrity metadata.
  - Restore plan and dry-run report.
  - Validation report with confidence score and remediation guidance.
  - Audit trail of approvals and actions.
- Files, services, or systems involved:
  - Local workspace files and metadata.
  - Archive artifacts produced locally.
  - Optional scheduler integrations if they are added later.

## Dependencies

- Skills:
  - Workspace discovery and recovery skill.
  - Validation and verification skill.
- Scripts:
  - Manifest generator.
  - Snapshot packager and checksum verifier.
  - Restore planner and dry-run simulator.
  - Validation report generator.
- MCP servers:
  - None required for v1.
- App connectors:
  - None required for v1.
- External APIs:
  - None required for baseline v1.
- Secrets or credentials:
  - None required for baseline local operation.
  - Optional local-user-controlled encryption key if encrypted archives are implemented.

## Public Positioning

- GitHub repository name: codexvault
- Display name: CodexVault
- Short description: Deterministic workspace backup, validation, and recovery for Codex environments.
- Target audience: Developers and Codex users who need repeatable workspace restoration across machines and operating systems.
- Why this should exist: Codex workspaces are operational environments, not just file trees. A purpose-built resilience plugin can preserve enough structured state to make recovery safer and more predictable than a generic archive tool.

## Open Questions

- Question: How much of the environment discovery should be limited to workspace-local state versus system-wide state?
- Owner: Spec phase
- Resolution: To be finalized during design spec.
- Question: What minimum manifest schema is sufficient to support meaningful restore guidance without overfitting to one OS?
- Owner: Spec phase
- Resolution: To be finalized during design spec.
- Question: Which restore actions are safe enough for automation versus requiring explicit confirmation every time?
- Owner: Spec phase
- Resolution: To be finalized during test matrix and security review.

## Roadmap

- V1:
  - Workspace discovery and manifest generation.
  - Snapshot packaging with integrity checks.
  - Guided restore orchestration with dry-run and validation.
  - Local-first audit trail and recovery reports.
- V2:
  - Scheduled and pre-change snapshots.
  - Provenance metadata and snapshot comparison.
  - Conflict resolution and partial restore improvements.
- V3:
  - Broader resilience workflows such as team templates, sync, and disaster recovery bootstrap.
  - More advanced self-healing and repair recommendations.

