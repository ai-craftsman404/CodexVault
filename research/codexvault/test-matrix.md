# Test Matrix

## Plugin

- Plugin: CodexVault
- Version: 0.1.0
- Date: 2026-05-18

## Coverage Summary

This matrix reflects the agreed MVP defaults:

- harness-first validation is a core differentiator
- agent-team simulation is required for high-risk QA paths
- TDD is required for new implementation work: tests first, then code, then rerun
- adversarial evaluator review is required for risky changes before merge/release
- the user-facing workflow is a single cross-platform Python CLI
- discovery intelligence has moved to a safer v1b shape with adapter-based OS metadata, Linux heuristics, and workspace-scoped installer seeding
- verified path mapping now covers Windows Desktop, Windows CLI, WSL Ubuntu, Debian container, Ubuntu 24.04 container, Debian 12 container, Fedora 42 container, and Alpine 3.21 container
- destructive restore actions remain human-gated
- scheduling is out of MVP
- secrets are redacted by default
- temp-dir partial restore is limited to a plugin-managed isolated directory
- validation uses tiered labels rather than a single precision score
- macOS coverage is postponed to post-MVP
- restore verification uses one smoke test plus required checks
- checksum algorithm is SHA-256
- snapshot format uses OS-native archive plus checksum sidecar
- no subpath preview mode in v1a
- archive inclusion uses explicit allowlist with secret redaction
- checksum sidecar is plain JSON
- restore verification uses one smoke check plus required checks
- temp-dir restore remains plugin-managed and isolated
- temp-dir restore root is plugin-managed or OS temp only
- temp-dir restore cleanup occurs on success or failure
- temp-dir failure reports include cleanup status
- checksum mismatch maps to integrity failure
- path traversal maps to security/gate failure
- archive allowlist uses root-relative file and folder patterns
- archive exclusions include `.git`, `node_modules`, `__pycache__`, `.codexvault`, `.DS_Store`
- malformed manifest coverage starts with invalid JSON, missing required top-level fields, and path traversal / out-of-scope paths
- v1b config schema and examples are treated as first-class fixtures for path customization
- self-improvement loop uses tiered fidelity labels, structured deltas, and bounded adversarial mutation

## Functional and Unit Testing

| Category | Scope | Validation Approach | Current Status |
| --- | --- | --- | --- |
| Unit testing | Discovery, manifest, snapshot, restore planning, validation helpers | Focused tests per script and schema helper | Covered |
| Integration testing | End-to-end discovery to report generation | Run the workflow across a sample workspace | Covered |
| E2E or workflow testing | Snapshot and restore rehearsal flow | Simulate the full MVP path with fixtures | Covered |
| E2E review-flow testing | Review-band candidate surfacing and JSON-only guidance | Dry-run scenarios with zero, one, and many candidates; confirm/reject persistence via embedded instructions | Covered |
| Platform coverage | Windows, WSL, and Linux normalization | Use Windows/WSL locally plus disposable Linux containers | Covered |
| Error and fallback testing | Missing runtimes, invalid manifests, corrupted archives | Negative-path fixtures and expected failures | Partially covered |
| Temp-dir restore fixtures | Isolated partial restore behavior | Plugin-managed isolated temp-dir only | Planned |
| Boundary and equivalence testing | Workspace boundaries, file sets, partial state | Equivalence classes for stable, volatile, and excluded data | Covered |
| Contract and schema testing | Manifest and simulation JSON contracts | Schema validation and golden files | Covered |
| Config schema and example testing | v1b path customization schema and OS examples | Validate required keys and expected example values | Covered |
| Python CLI coverage | User-facing entrypoint and workflow commands | Run discover/manifest/snapshot/plan/verify/simulate/backup end-to-end | Covered |
| Fidelity scoring testing | Temp-dir restore mirror quality | Validate tiered labels `pass`, `pass-with-warnings`, `partial`, `fail` | Planned |
| Delta envelope testing | Safe simulation feedback to agent-team | Confirm only allowed delta fields are accepted | Planned |
| Adversarial rehearsal testing | Non-destructive mutation pass | Validate bounded mutation scope and review boundary | Planned |
| Provenance testing | Minimal provenance fields and redaction rules | Confirm archive metadata stays non-secret | Partially covered |
| Checksum testing | Snapshot integrity sidecar | Validate SHA-256 digests against archives | Covered |
| Archive inclusion testing | Snapshot content allowlist | Confirm only allowed files are archived | Covered |
| API versioning and backward compatibility | Manifest schema evolution | Additive-only minor changes and migration checks | Partially covered |
| Negative testing and abuse case library | Corrupt, incomplete, or malicious inputs | Fixture library for bad manifests and hostile files | Partially covered |
| Temp-dir rollback testing | Cleanup after restore simulation | Verify temp dirs are removed on success/failure | Covered |
| TDD change loop testing | New code paths and bug fixes | Confirm failing test is written or updated before implementation | Covered for this change set; still required for future changes |
| Adversarial evaluator testing | Risky logic, security-sensitive flows, agent prompts | Dedicated red-team style review before release | Covered for this change set; still required for future changes |

## Quality and Assurance Testing

| Category | Scope | Validation Approach | Current Status |
| --- | --- | --- | --- |
| Static type checking | Script and schema helpers | Type/lint checks where applicable | Planned |
| LLM-specific SAST | Prompt/tool misuse and hidden-automation risks | Review of agent prompts and tool boundaries | Partially covered |
| CI enforcement gates | Path, schema, and safety gates | Build blocked if core checks fail | Planned |
| Determinism and idempotency | Snapshot and validation repeatability | Repeat runs on same fixture set | Covered |
| Snapshot or golden-file testing | Manifests, plans, and reports | Compare outputs to known-good fixtures | Planned |
| Concurrency and race condition testing | Snapshot drift and capture timing | Mutate fixture during capture and verify detection | Planned |

## Prompt and Input Attack Testing

| Category | Scope | Validation Approach | Current Status |
| --- | --- | --- | --- |
| Prompt injection OWASP LLM01 | Hostile instructions in captured content | Ensure tools ignore injected text in files | Planned |
| Indirect prompt injection | Malicious README/config content | Simulated poisoned workspace inputs | Partially covered |
| Jailbreak and instruction override | Override attempts against safety policy | Persona prompts and adversarial cases | Planned |
| System prompt extraction | Leakage from agent outputs | Review outputs for hidden prompt exposure | Planned |
| Streaming output security | Partial results and intermediate state | Ensure no sensitive state leaks in incremental output | Planned |

## Output and Data Security Testing

| Category | Scope | Validation Approach | Current Status |
| --- | --- | --- | --- |
| Insecure output handling OWASP LLM02 | Logs and reports | Verify sensitive data never appears in outputs | Partially covered |
| PII and sensitive data leakage OWASP LLM06 | Env vars, tokens, config values | Redaction tests and allowlist review | Partially covered |
| Data exfiltration via tools | Archive, manifest, and simulation tool calls | Confirm tools only access intended paths | Partially covered |
| Data lineage and provenance tracking | Snapshot provenance and audit trail | Record source and capture context | Planned |

## Agentic and Tool Use Security

| Category | Scope | Validation Approach | Current Status |
| --- | --- | --- | --- |
| Excessive agency OWASP LLM08 | Agent actions beyond scope | Enforce human-gated destructive actions | Covered |
| Tool call validation | Discovery, snapshot, restore, verify calls | Check arguments and path scope | Partially covered |
| Human-in-the-loop bypass | Restore execution without approval | Explicit block tests | Covered |
| Agent-to-agent trust boundary | Persona handoff and adjudication | Validate contracts and evidence flow | Planned |
| Autonomous action scope testing | Harness usage boundaries | Ensure simulation stays non-destructive | Covered |
| Tool result injection | Poisoned tool output | Verify agent does not trust hostile results blindly | Planned |

## Supply Chain and Infrastructure Security

| Category | Scope | Validation Approach | Current Status |
| --- | --- | --- | --- |
| Dependency and supply chain scanning OWASP LLM05 | Scripts and local dependencies | Scan for vulnerable or unexpected packages | Planned |
| API key and secret leakage | Archives, manifests, logs | Secret scanning and fixture review | Partially covered |
| MCP or plugin integrity | Plugin manifest and local structure | Validate bundle integrity and path correctness | Planned |
| Container or runtime hardening | Local runtime assumptions | Confirm no unnecessary elevated privileges | Not applicable for MVP unless runtime changes |

## Compliance and Governance Testing

| Category | Scope | Validation Approach | Current Status |
| --- | --- | --- | --- |
| Audit trail completeness | Snapshot, restore, and simulation actions | Confirm logs include approvals and decisions | Planned |
| GDPR and data retention enforcement | Retention and deletion behavior | Retention policy checks and pruning tests | Planned |
| Role-based access control | Human approval checkpoints | Confirm restore gate behavior | Planned |
| Compliance logic testing | Privacy and retention rules | Policy tests against sample scenarios | Planned |
| Incident response playbook validation | Failure and corruption paths | Verify documented recovery steps exist | Planned |

## Recommended Categories

| Category | Decision | Reason |
| --- | --- | --- |
| Property-based testing | Include | Good fit for manifest and path normalization rules |
| Determinism and idempotency | Include | Central to the product promise |
| Concurrency and race condition testing | Include | Snapshot drift is a core risk |
| Replay or regression testing | Include | Useful for restore simulations and fixture evolution |
| Cross-tenant data isolation | Not applicable | Single-user local-first MVP |
| LLM output evaluation | Include | Needed for harness and agent-team recommendation quality |
| Hallucination risk scoring | Include | Important for restore recommendations |
| Adversarial evaluator pass | Include | Needed to challenge restore claims and safety boundaries |
| Disaster recovery or failover testing | Defer | V1 is not full host failover |
| Encrypted sensitive retention | Defer | Not required for MVP and increases key-management complexity |
| macOS CI smoke testing | Include | Minimal GitHub Actions smoke workflow for release validation |

## MVP Exit Criteria

- Manifest schema validates on sample workspaces.
- Snapshot packaging produces checksum-verified archives.
- Restore planning and dry-run validation complete successfully on fixtures.
- Temp-dir partial restore tests pass for isolated non-destructive paths.
- Agent-team simulation surfaces disagreements and failure modes.
- TDD change loop is followed for new code paths and bug fixes.
- Adversarial evaluator review is completed for security-sensitive or restore-critical changes.
- Secret redaction tests pass.
- Dry-run review-band candidates are surfaced with embedded JSON instructions and a single canonical review artifact.
- Human approval gates block in-place destructive restore actions.
- Scheduling remains out of scope in the shipped MVP.
- Provenance metadata remains minimal and non-secret.
- Validation labels resolve to `validated`, `validated-with-warnings`, or `not-validated`.
- Error codes map consistently to the agreed CVX namespace.
- Agent-team adjudication records claims, evidence, disputes, and decisions in a shared JSON envelope.
- Discovery fields use a shared core plus small OS-specific extensions.
- Verified Linux container coverage includes Ubuntu, Debian, Fedora, and Alpine install-tree captures.
- v1b config schema validates and example configs match the documented OS-specific paths.
- Self-improvement loop outputs tiered fidelity labels, safe deltas only, and bounded adversarial mutations.
- Python CLI is the only supported user-facing entrypoint.
