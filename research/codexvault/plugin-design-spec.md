# Plugin Design Spec

## Identity

- Plugin package name: codexvault
- Display name: CodexVault
- Version: 0.1.0
- Description: Workspace resilience and restoration plugin for Codex with normalized discovery, snapshot integrity, guided restore, and validation reports.
- Distinguishing rule: use Codex agent-team orchestration and AI harnesses as much as possible for simulation, verification, and quality assurance, while keeping destructive actions human-gated.
- Project rule: use Codex subagents and agent-team workflows wherever they materially improve development, build, and testing throughput; choose the most cost-effective OpenAI model that can reliably complete each task.
- Developer name: TBD
- Repository: TBD
- License: TBD
- Keywords: backup, restore, workspace, resilience, validation, recovery
- Category: developer-tools / reliability

## Classification

- Type: skill plus scripts
- Reason for this type:
  - V1 is primarily a repeatable workspace workflow, but it needs local scripts for manifesting, packaging, checksums, validation, and restore planning.
  - Agent-team orchestration is part of the workflow model, but it should be implemented as a harnessed execution pattern rather than the core packaging type.
  - The harness is a core differentiator for CodexVault, not an optional accessory.

## Complexity and Model Selection

- Overall complexity: high
- Recommended main-thread model tier: strong model for design, security/privacy, and release-readiness decisions
- Recommended agent model tiers: mid-tier for mechanical artifact work; strong for restore-safety and security-sensitive logic
- Escalation triggers:
  - The plugin starts promising host-level backup guarantees.
  - Scheduler integrations become required rather than optional.
  - Encryption/key-management design becomes ambiguous.
  - Agent personas begin making irreversible restore decisions without human checkpoints.
  - The implementation cannot exercise the agent harness for major simulation and QA paths.

## User Workflows

| Workflow | User Prompt | Expected Codex Behavior | Success Criteria |
| --- | --- | --- | --- |
| Workspace discovery | "Scan this workspace and tell me what can be restored later." | Detect OS, shell, Codex paths, package managers, Git state, project structure, and MCP topology. | User gets a normalized profile and a clear list of discovered state. |
| Snapshot creation | "Back up this workspace now." | Produce a manifest, snapshot archive, and integrity metadata with secret redaction by default. | Snapshot completes and verifies cleanly. |
| Restore planning | "Restore my Codex workspace from this snapshot." | Generate a restore plan, show a dry-run, and require confirmation before execution. | Restore path is previewed before any destructive action. |
| Validation | "Check whether this workspace will run after restore." | Verify runtimes, package managers, shell compatibility, and MCP connectivity. | Report highlights gaps and remediation steps. |
| Agent-team simulation | "Simulate a restore using multiple personas and tell me where it fails." | Spawn bounded roles such as discovery, snapshot, restore-planning, validation, and recovery simulation agents, then reconcile their results into one recommendation. | Simulation exposes disagreements, failure points, and confidence gaps before any real restore. |
| Harness-first QA | "Use Codex agent-team to pressure-test this backup plan." | Prefer multi-agent simulation, cross-checking, and adjudication for restore safety and validation quality. | Agent-team findings improve confidence, expose gaps, and shape the restore plan. |

## Agent Rubric

Agents should be able to infer the backup structure from a compact, explicit contract.

- Artifact name pattern:
  - `codexvault-<workspaceId>-<timestamp>-<platform>`
- Manifest:
  - JSON
  - contains the normalized discovery and restore metadata
  - does not store secrets by default
- Snapshot archive:
  - OS-appropriate archive format
  - paired with a checksum sidecar
  - treated as the durable backup artifact
- Provenance:
  - minimal non-secret provenance in the archive
  - richer audit detail may live in a sidecar or log
- Validation:
  - outputs tiered labels, not opaque free-form confidence
  - must call out blockers, warnings, and required next steps
- Simulation envelope:
  - keep `schemaVersion`, `status`, `headline`, `adjudication`, and short `findings[]`
  - do not expand the default output beyond the highlights-only contract
- Restore boundaries:
  - temp-dir restore is isolated and plugin-managed
  - in-place restore is human-gated
  - destructive action must never be implied by simulation alone
- Agent reasoning:
  - prefer highlights-only summaries
  - use evidence, not guesswork, to infer particulars
  - escalate uncertainty rather than inventing missing details

## Path Contract

CodexVault should treat paths as explicit configuration, not inferred conventions.

- Backup destination directory:
  - `.codexvault/snapshots/`
- Snapshot staging directory:
  - `.codexvault/staging/`
- Manifest output directory:
  - `.codexvault/manifests/`
- Checksum sidecar directory:
  - alongside the archive in `.codexvault/snapshots/`
- Restore plan directory:
  - `.codexvault/restores/`
- Verification output directory:
  - `.codexvault/verification/`
- Simulation output directory:
  - `.codexvault/simulations/`
- Fixture root:
  - `plugins/codexvault/tests/fixtures/`
- Include root:
  - workspace root, filtered by explicit allowlist

Path rules:

- keep paths stable and human-readable
- use plugin-managed directories for generated artifacts
- avoid hidden implicit output locations
- keep temporary restore work inside isolated temp-dir boundaries
- revisit the path contract later for validation and expansion

## Presentation Contract

MVP output should stay highlights-only and action-first.

- Always show a one-line headline for the operation.
- Always show one short status line.
- Always show the top risk, blocker, or validation result.
- Always show one required user action, if any.
- Never dump full implementation detail in the normal operation path.

### Backup presentation

- Show what was captured.
- Show integrity status.
- Show where the snapshot is stored.
- Show one notable omission only if it matters to recovery.

### Restore presentation

- Show what will be restored.
- Show dry-run result.
- Show whether approval is required.
- Show the safest next step.

### Validation presentation

- Show one of: `validated`, `validated-with-warnings`, `not-validated`.
- Show the top one or two reasons only.
- Show whether the issue is safe to proceed or needs correction first.

### Error presentation

- Show a stable CVX error code.
- Show a plain-English cause.
- Show the next best action.
- Avoid exposing raw internal traces unless explicitly requested.

### Progress presentation

- Use short phase labels such as `discovering`, `snapshotting`, `planning restore`, and `verifying`.
- Prefer brief progress updates over verbose logs.
- Surface only meaningful state transitions.

### Approval presentation

- State the exact change scope.
- State the reason approval is needed.
- State the single action being approved.
- Keep the prompt concise and unambiguous.

## Plugin Structure

```text
plugins/codexvault/
  .codex-plugin/plugin.json
  skills/
  assets/
  .mcp.json
  .app.json
```

## Manifest Plan

- `name`: codexvault
- `version`: 0.1.0
- `description`: Workspace resilience and restoration for Codex with discovery, snapshot integrity, and guided restore.
- `skills`: CodexVault core resilience workflow
- `mcpServers`: none in v1
- `apps`: none in v1
- `interface.displayName`: CodexVault
- `interface.shortDescription`: Deterministic workspace discovery, backup, validation, and restore for Codex environments.
- `interface.longDescription`: CodexVault helps Codex users capture normalized workspace state, produce portable snapshot artifacts, validate restore viability, and recover safely with human checkpoints.
- `interface.capabilities`: environment discovery, manifest generation, snapshot packaging, restore planning, validation reporting, secret redaction
- `interface.harnessCapabilities`: agent-team persona orchestration, restore simulation, failure replay, validation cross-checks, human checkpointing
- `interface.designPrinciple`: harness-first validation, simulation-heavy QA, human-gated execution
- `interface.defaultPrompt`: Capture the workspace state conservatively, exclude secrets by default, validate integrity, and make restore actions previewable and reversible where possible.
- `interface.restoreGuarantees`: captured, restorable, validated
- `interface.manifestCore`: schema version, workspace identity, environment summary, git state, package manager state, file inventory, integrity metadata
- `interface.manifestDefaults`: small cross-platform core schema, additive extension blocks, stable defaults for optional fields
- `interface.manifestProvenance`: schema version, capture timestamp, workspace ID, git commit/hash, tool versions, checksum chain
- `interface.snapshotFormat`: OS-appropriate archive plus checksum sidecar
- `interface.snapshotImplementation`: OS-native archive, no chunking in v1a
- `interface.archiveInclusion`: explicit allowlist with secret redaction
- `interface.archiveAllowlist`: `*.md`, `*.json`, `*.ps1`, `skills/**`, `scripts/**`, `tests/fixtures/**`, `assets/**`, `README*`, `LICENSE*`, `CHANGELOG*`
- `interface.archiveExclusions`: `.git`, `node_modules`, `__pycache__`, `.codexvault`, `.DS_Store`
- `interface.checksumAlgorithm`: SHA-256
- `interface.checksumSidecar`: plain JSON with archive path and digest
- `interface.tempRestoreScope`: plugin-managed isolated temp-dir fixtures only
- `interface.tempRestorePreview`: no subpath preview in v1a
- `interface.tempRestoreRoot`: plugin-managed isolated temp-dir under `.codexvault/` or OS temp
- `interface.tempRestoreFiles`: allowlisted restore targets plus required manifest metadata
- `interface.tempRestorePassCriteria`: dry-run completes, files land in isolated temp-dir, required checks pass
- `interface.tempRestoreCleanup`: always clean temp-dir on success or failure
- `interface.tempRestoreFailureReport`: include cleanup status when failure occurs
- `interface.secretPolicy`: deny by default, redact known sensitive patterns, encrypted retention only by explicit opt-in
- `interface.snapshotPolicy`: manifest-then-verify with checksum re-scan
- `interface.incrementalPolicy`: snapshot chain with periodic full checkpoints
- `interface.pruningPolicy`: rolling window with pinned known-good snapshots
- `interface.validationStatus`: validated, validated-with-warnings, not-validated
- `interface.errorCodes`: CVX-1xxx discovery, CVX-2xxx manifest, CVX-3xxx snapshot, CVX-4xxx restore-plan, CVX-5xxx verify, CVX-6xxx security/gate, CVX-7xxx integrity, CVX-9xxx internal
- `interface.failurePolicy`: checksum mismatch = integrity fail; missing manifest or malformed JSON = manifest/restore-plan fail; permission denied or path traversal = security/gate fail
- `interface.adjudicationRecord`: claims, supporting evidence, disputes resolved, decision, confidence delta
- `interface.discoveryFields`: shared core fields with small OS-specific extensions
- `interface.restoreSmoke`: one smoke check plus required checks
- `interface.logo`: TBD
- `interface.composerIcon`: TBD
- `interface.screenshots`: TBD

## Skills

| Skill | Trigger Description | Scope | Scripts | References |
| --- | --- | --- | --- | --- |
| CodexVault core resilience workflow | Invoked explicitly for backup, restore, validation, or workspace recovery, or implicitly when the user asks to inspect recoverability | Workspace discovery, manifesting, packaging, restore planning, and validation | manifest, snapshot, restore, verify scripts | PRD, local workspace, restore plan |

## Scripts

| Script | Purpose | Inputs | Outputs | Validation |
| --- | --- | --- | --- | --- |
| `discover_workspace` | Collect normalized workspace metadata | OS, shell, paths, Git, package managers, runtime info, MCP topology | Discovery profile | Unit checks and cross-platform fixtures |
| `write_manifest` | Generate schema-versioned workspace manifest | Discovery profile and workspace metadata | JSON manifest | Schema validation and golden-file checks |
| `create_snapshot` | Package archive and integrity metadata | Manifest and selected workspace contents | Archive and checksum file | Checksum verification and corruption simulation |
| `plan_restore` | Build restore order and checkpoints | Manifest, snapshot metadata, target state | Restore plan and dry-run report | Negative-path and rollback checks |
| `verify_restore` | Confirm runtime and dependency readiness | Restored workspace and environment state | Validation report and confidence score | Integration and failure-mode tests |
| `simulate_restore_team` | Run a multi-persona restore simulation | Scenario definition, manifest, snapshot, persona roles | Simulation transcript and adjudicated report | Disagreement detection and failure replay tests |

## Backup Artifact Contract

| Element | Required Shape | Notes |
| --- | --- | --- |
| Artifact name | `codexvault-<workspaceId>-<timestamp>-<platform>` | Stable and human-scannable |
| Manifest | JSON | Cross-platform core with extension blocks |
| Snapshot archive | OS-native archive | Windows ZIP, Linux tar.gz |
| Checksum | Sidecar file | Separate integrity evidence |
| Provenance | Minimal and non-secret | Keep sensitive detail out of archives |
| Restore report | Highlights-only summary | No verbose internal trace in the default path |

## MCP and Apps

- MCP servers: none in v1
- App connectors: none in v1
- Authentication: no external authentication required for baseline local use
- Permissions:
  - Default conservative local scope.
  - Human confirmation before destructive restore actions.
  - Optional encryption for retained artifacts if added later.
  - Explicit exclusion of secrets and sensitive env values by default.

## Definition of Done

- [ ] Plugin installs locally.
- [ ] Manifest paths are valid and relative to the plugin root.
- [ ] Discovery, manifest, snapshot, restore-plan, and verification flows work on supported platforms.
- [ ] Secret-redaction defaults are in place and tested.
- [ ] Dry-run restore and human approval checkpoints are implemented.
- [ ] Agent-team simulation can rehearse restore scenarios without performing destructive actions.
- [ ] Core QA and restore simulation paths preferentially use Codex agent-team and AI harness workflows.
- [ ] Validation reports are readable and explain failures clearly.
- [ ] Operation presentation is highlights-only, action-first, and consistent across backup and restore flows.
- [ ] Security and privacy review is complete.
- [ ] Public README is complete.
- [ ] Changelog and license are present.
- [ ] Test matrix covers cross-platform, negative, integrity, and destructive-path scenarios.
- [ ] The plugin does not overpromise host-level backup or guaranteed reconstruction.

## Roadmap

- Versioning scheme:
  - `v1a`, `v1b`, ... for the first release line
  - `v2a`, `v2b`, ... for the next release line
  - each lettered step should represent a narrow, shippable increment

- `v1a`:
  - Workspace discovery and manifest generation.
  - Integrity-checked snapshot packaging.
  - Guided restore with dry-run, validation, and approval checkpoints.
  - Agent-team simulation for restore rehearsal and failure analysis.
  - Harness-first QA and cross-check workflows for the highest-risk restore paths.
  - Local-first operation with secret redaction by default.
  - Windows and Linux first-class support.
- `v1b`:
  - Temp-dir isolated partial restore tests.
  - Compact presentation layer for backup, restore, and validation highlights.
  - Stable CVX error codes and tiered validation labels.
- `v2a`:
  - Scheduling hooks and pre-change backup triggers.
  - Provenance metadata and snapshot comparison.
  - Conflict resolution for partial restores.
- `v2b`:
  - Optional encrypted retention for selected artifacts.
  - Broader retention controls and provenance sidecar improvements.
  - More advanced restore conflict handling.
- `v3a` or later:
  - Optional sync and team workspace templates.
  - Disaster-recovery bootstrap mode.
  - Broader resilience automation with stricter governance.
  - macOS support, macOS fixtures, and macOS CI smoke validation.

## Long-Term Product Goal

- CodexVault should become the default recovery layer for Codex workspaces when users need to move, rebuild, or repair development environments.
- The system should remain conservative, inspectable, and local-first rather than turning into a generic backup service.
- Agent personas should be used to improve diagnosis and rehearsal, not to bypass restore checkpoints.
- CodexVault should rely on agent-team orchestration as a primary quality and assurance mechanism wherever it materially improves confidence.

## Evaluation Approach

- Development and release validation should include:
  - schema checks
  - integrity validation
  - failure-path and rollback tests
  - cross-platform path coverage
  - redaction tests
  - restore dry-run validation
- The plugin should be evaluated on whether it helps users recover safely, not on whether it can promise universal reconstruction.
- Agent-team simulations should be judged on whether they expose restore failure modes earlier and more clearly than a single-pass workflow.
- Harness usage should be treated as part of the product value proposition, not just an internal development convenience.

## Agent Team Plan

- Agent team needed: yes
- Reason:
  - The intended workflow includes persona-based orchestration and simulated restoration exercises, which are a natural fit for bounded agent roles.
- Execution style:
  - bounded role pipeline with adjudication
- Planned roles:
  - Discovery Agent: enumerate environment state and recovery constraints.
  - Snapshot Agent: inspect archive integrity and manifest completeness.
  - Restore Planning Agent: propose safe restore sequencing and checkpoints.
  - Integrity Validation Agent: cross-check checksums, schema, and corruption signals.
  - Recovery Simulation Agent: rehearse failure paths and partial restore outcomes.
- Safety constraints:
  - no irreversible restore action without human approval
  - simulation agents must remain non-destructive
  - restore recommendations must be traceable to manifest or validation evidence
  - prefer agent-team/harness execution for discovery, validation, and simulation where feasible
- Non-overlapping file ownership:
  - To be defined during build, but simulation and documentation artifacts should be separable from core scripts.
