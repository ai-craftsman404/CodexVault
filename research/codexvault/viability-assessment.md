# Viability Assessment

## Plugin

- Working name: CodexVault
- Date: 2026-05-13
- Assessor: Codex

## Scoring

Score each area from 1 to 5.

| Area | Score | Notes |
| --- | ---: | --- |
| Usefulness | 5 | Workspace recovery is a real pain point, especially for AI-assisted environments that accumulate local state quickly. |
| Uniqueness | 4 | Backup utilities are common, but a Codex-native resilience workflow with manifests and restore validation is more specific. |
| Technical feasibility | 3 | Discovery, manifesting, packaging, and guided restore are feasible; full deterministic reconstruction across machines is not. |
| Low maintenance burden | 3 | Ongoing burden will come from schema evolution, OS differences, and validation coverage. |
| Low security/privacy risk | 2 | Environment capture can easily over-collect secrets or sensitive machine details without strong redaction defaults. |
| GitHub visibility value | 4 | The positioning is strong if framed as workspace resilience for AI-assisted development rather than a generic backup tool. |

## Decision

- Total score: 21 / 30
- Decision: proceed with scope controls
- Reason:
  - The concept is useful and distinctive, but v1 must stay bounded to workspace-level resilience with explicit exclusions around host imaging, unmanaged secrets, and over-automation.

## Complexity and Model Recommendation

- Estimated complexity: high
- Recommended model tier for design: strong
- Recommended model tier for build: strong for discovery/restore logic and security-sensitive boundaries, mid-tier for mechanical packaging work
- Recommended model tier for final review: strong

## Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Scope expands into full backup/recovery of the host machine | High | High | Limit v1 to workspace-local and explicitly enumerated environment state. |
| Sensitive variables or tokens are captured in manifests or archives | High | High | Exclude secrets by default, redact aggressively, and require explicit opt-in for sensitive retention. |
| Restore success depends on host-specific runtime drift | High | High | Provide dry-run restore, validation reports, and remediation guidance rather than unconditional restore promises. |
| Cross-platform support becomes inconsistent | Medium | Medium | Keep a normalized schema and platform-specific adapters separate. |
| Automation becomes destructive without enough checkpoints | Medium | High | Require restore previews, human approval, and rollback checkpoints. |

## MVP Recommendation

- Smallest useful version:
  - Workspace discovery, normalized manifest generation, integrity-checked snapshot packaging, and guided restore dry-runs with validation reporting.
- Required capabilities:
  - Discovery engine
  - Manifest system
  - Snapshot packaging and checksum validation
  - Restore planning and dry-run preview
  - Dependency/runtime verification
  - Secret-redaction defaults
- Deferred capabilities:
  - Scheduled automation across OS schedulers
  - Cloud sync
  - Team workspace templates
  - Full disaster-recovery bootstrap mode

## Versioned Outlook

- V1 outlook:
  - Strong if positioned as a recovery assistant for Codex workspaces, not as a generic enterprise backup suite.
- V2 outlook:
  - Better once scheduling, provenance metadata, and conflict resolution are added.
- V3 outlook:
  - Stronger still if the system becomes a full resilience platform with optional sync and recovery coaching.

## Validation Notes

- The test matrix should include destructive-path simulation, failure handling, and redaction checks.
- Windows, macOS, and Linux paths need explicit coverage because shell and archive behavior differs materially.

