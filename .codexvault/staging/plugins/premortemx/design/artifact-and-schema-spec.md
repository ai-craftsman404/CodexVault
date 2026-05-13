# PreMortemX Artifact And Schema Spec

## Design Goal

Artifact naming should be intuitive, sortable, and stable across repeated runs.

V2 should prefer:
- readable names
- ISO-like timestamps
- explicit run identifiers
- clear separation between human-facing and machine-facing artifacts

## Per-Run Directory Convention

Recommended directory root:

```text
plugins/premortemx/runs/
```

Recommended run directory name:

```text
pmx-<project-slug>-<utc-yyyymmddThhmmssZ>-<shortid>/
```

Example:

```text
pmx-acme-api-20260504T123500Z-a17c/
```

Rationale:
- sorts naturally
- easy for humans to scan
- avoids collisions
- stable enough for registry linking

Recommended dated path layout:

```text
plugins/premortemx/runs/YYYY/MM/<run-id>/
```

Example:

```text
plugins/premortemx/runs/2026/05/pmx-acme-api-20260504T123500Z-a17c/
```

## Per-Run Artifact Layout

```text
plugins/premortemx/runs/YYYY/MM/<run-id>/
  summary-short.md
  summary-standard.md
  summary-exec.md
  risk-register.md
  run-record.json
  analysis.json
  approvals.json
  retention.json
  override.md
  evidence-index.md
  attachments/
```

File intent:
- `summary-short.md`: shortest decision snapshot
- `summary-standard.md`: default readable summary
- `summary-exec.md`: compact executive-facing version when needed
- `risk-register.md`: detailed evidence/risk/mitigation report
- `run-record.json`: machine-readable record
- `analysis.json`: structured internal analysis output suitable for replay or evaluator review
- `approvals.json`: permission requests, approvals, and escalation trace
- `retention.json`: retention and sensitivity handling decisions
- `override.md`: only present when a human overrides a block
- `evidence-index.md`: compact reference list of inspected evidence sources
- `attachments/`: optional referenced artifacts or generated exports

## Registry Convention

Recommended registry root:

```text
plugins/premortemx/registry/
```

Recommended files:

```text
plugins/premortemx/registry/runs/index.jsonl
plugins/premortemx/registry/quality-review-log.json
```

Intent:
- `index.jsonl`: append-only summary index of all runs
- `quality-review-log.json`: later outcome review and quality-signal updates

## Human-Facing Report Titles

Recommended title pattern:

```text
PreMortemX Release Assessment
```

Recommended subtitle block:
- run id
- created timestamp
- last updated timestamp
- active mode
- current recommendation
- confidence band

## Report Template Conventions

### `summary-short.md`

Suggested sections:
- title
- recommendation snapshot
- top blockers or concerns
- key-point summary

### `summary-standard.md`

Suggested sections:
- title
- recommendation snapshot
- top blockers or concerns
- mitigation path
- confidence and evidence note
- key-point summary

### `summary-exec.md`

Suggested sections:
- title
- recommendation
- top blockers
- mitigation path
- key-point summary

### `risk-register.md`

Suggested sections:
- title
- scope reviewed
- detailed risk bullets
- evidence references
- mitigation bullets
- unresolved assumptions
- key-point summary

### `override.md`

Suggested sections:
- title
- overridden recommendation
- rationale
- mitigation steps
- responsible owner
- date/time
- key-point summary

## Run Record Schema

Required fields:

```json
{
  "schemaVersion": "1.0",
  "runId": "pmx-acme-api-20260504T123500Z-a17c",
  "pluginVersion": "0.2.0",
  "createdAt": "2026-05-04T12:35:00Z",
  "updatedAt": "2026-05-04T12:35:00Z",
  "status": "completed",
  "projectSlug": "acme-api",
  "taskType": "architecture-review",
  "executionMode": "skill+scripts",
  "approvalMode": "adaptive",
  "privacyMode": "privacy-first-hybrid",
  "retentionClass": "standard",
  "artifactPath": "runs/2026/05/pmx-acme-api-20260504T123500Z-a17c",
  "registryRefs": {
    "indexKey": "2026-05/pmx-acme-api-20260504T123500Z-a17c"
  },
  "inputFingerprint": {
    "promptHash": "sha256:...",
    "contextHash": "sha256:..."
  },
  "mode": "architecture-validation",
  "routingType": "hybrid",
  "decision": "Warn",
  "confidenceBand": "Medium",
  "inspectedInputs": {
    "designDocs": [],
    "implementationContext": [],
    "releasePlan": [],
    "testEvidence": [],
    "architectureContext": [],
    "dependencies": [],
    "constraints": []
  },
  "riskSummary": {
    "high": 0,
    "medium": 2,
    "low": 3
  },
  "topRisks": [],
  "evidenceCoverage": "adequate",
  "warnReasons": [],
  "blockReasons": [],
  "outputTiers": [
    "short",
    "standard",
    "exec"
  ],
  "override": {
    "applied": false,
    "rationale": null,
    "mitigationSteps": [],
    "responsibleOwner": null
  },
  "sensitivityReview": {
    "likelySensitive": false,
    "recommendedProtection": "none",
    "encryptionUsed": false
  },
  "artifacts": {
    "summaryShort": "summary-short.md",
    "summaryStandard": "summary-standard.md",
    "summaryExec": "summary-exec.md",
    "riskRegister": "risk-register.md",
    "runRecord": "run-record.json",
    "analysis": "analysis.json",
    "approvals": "approvals.json",
    "retention": "retention.json",
    "override": null,
    "evidenceIndex": "evidence-index.md"
  },
  "qualityFollowup": {
    "status": "pending",
    "reviewDue": null,
    "falsePositiveNotes": [],
    "missedRiskNotes": [],
    "outcomeNotes": []
  }
}
```

## Optional Fields

- `completedAt`
- `parentRunId`
- `branch`
- `workspaceHash`
- `labels`
- `aggregateScore`
- `confidenceScoreInternal`
- `routingConfidenceInternal`
- `permissionEscalationsRequested`
- `permissionEscalationsApproved`
- `guardrailRecommendations`
- `approvers`
- `approvalEvents`
- `redactions`
- `dataClasses`
- `expiresAt`
- `purgedAt`
- `failure`
- `metrics`
- `scriptVersions`
- `attachments`
- `tags`
- `linkedPreviousRunId`

## Schema Principles

- Required fields should support auditability and future review.
- Optional fields should support harness growth without making v2 brittle.
- The schema should stay readable enough that humans can inspect it without tooling.
- The example schema should match the generated script output exactly in field casing and structure.
