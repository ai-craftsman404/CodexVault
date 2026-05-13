# Testing Categories Policy

This document is the source of truth for testing coverage expectations in Code Plugin Guru.

## Core Rule

All development in this repository must consider the full testing category set in this document.

Consider intelligently, not mechanically:

- apply every `Mandatory` category that is relevant to the change, architecture, deployment model, and risk profile
- assess every `Recommended` category and either include it or record why it is not needed yet
- use `Optional` categories when the plugin context, deployment target, or release risk justifies them
- mark categories as `not applicable` only with a concrete reason
- scale testing depth to the real risk, but never skip relevance assessment

## How To Use This Policy

Use this category set during:

- design and definition of done
- implementation planning
- test-matrix creation
- security and privacy review
- release readiness review

When a plugin or change does not use a capability directly, do not force the category into scope. Example: do not require multi-modal attack testing for a text-only skill-only plugin. Do require the team to explicitly decide that it is out of scope.

## Coverage Expectations By Priority

### Mandatory

#### 1. Functional and Unit Testing

- Unit testing
- Integration testing
- E2E or workflow testing
- Error and fallback testing
- Boundary and equivalence testing
- Contract and schema testing
- API versioning and backward compatibility
- Negative testing and abuse case library

#### 2. Quality and Assurance Testing

- Static type checking
- LLM-specific SAST
- CI enforcement gates

#### 3. Prompt and Input Attack Testing

- Prompt injection OWASP LLM01
- Indirect prompt injection
- Jailbreak and instruction override
- System prompt extraction
- Multi-modal input security
- Streaming output security

#### 4. LLM Gateway and Middleware Security

- LLM gateway or proxy security
- Rate limiting at gateway layer

#### 5. Output and Data Security Testing

- Insecure output handling OWASP LLM02
- PII and sensitive data leakage OWASP LLM06
- Data exfiltration via tools
- Data lineage and provenance tracking

#### 6. Adversarial ML and Model Security

- Training data poisoning OWASP LLM03
- Model provenance validation OWASP LLM05
- Model registry security
- AI bill of materials (AI-BOM)
- Fine-tuning pipeline security

#### 7. Agent Identity and Authentication

- Agent identity and mutual authentication
- Service-to-service authorisation

#### 8. Agent Memory Security

- Long-term memory store security
- Memory access control

#### 9. RAG and Retrieval Security

- RAG poisoning and context manipulation
- Retrieval access control

#### 10. Agentic and Tool Use Security

- Excessive agency OWASP LLM08
- Tool call validation
- Human-in-the-loop bypass
- Agent-to-agent trust boundary

#### 11. Supply Chain and Infrastructure Security

- Dependency and supply chain scanning OWASP LLM05
- API key and secret leakage

#### 14. Compliance and Governance Testing

- Audit trail completeness
- GDPR and data retention enforcement
- Role-based access control
- Compliance logic testing
- Third-party audit readiness

### Recommended

#### 1. Functional and Unit Testing

- Prompt versioning and change management
- SLA and availability testing

#### 2. Quality and Assurance Testing

- Property-based testing
- Snapshot or golden-file testing
- Mutation testing
- LLM-specific DAST
- Determinism and idempotency
- Concurrency and race condition testing
- Token budget testing
- Cost governance testing
- LLM output evaluation
- Evaluation dataset integrity
- Multi-turn or trajectory testing
- Multilingual safety testing
- Accessibility and i18n testing

#### 3. Prompt and Input Attack Testing

- Multi-turn manipulation
- Token smuggling
- Prompt caching security
- MITRE ATLAS attack simulation
- Zero-day prompt attack monitoring
- LLM-specific penetration testing

#### 4. LLM Gateway and Middleware Security

- Gateway authentication bypass
- Request and response logging at gateway

#### 5. Output and Data Security Testing

- Hallucination risk scoring
- Overreliance or blind trust OWASP LLM09
- Cross-tenant data isolation
- Synthetic data quality validation
- Agent telemetry data security

#### 6. Adversarial ML and Model Security

- Adversarial example or evasion testing
- Model quantisation or compression security
- RLHF or human feedback data security
- Model behaviour drift
- Membership inference testing
- Model watermarking or IP protection
- Third-party LLM API trust
- Model card or datasheet validation

#### 7. Agent Identity and Authentication

- Credential rotation testing
- Identity spoofing or impersonation

#### 8. Agent Memory Security

- Memory retention and expiry
- Memory poisoning via tool results

#### 9. RAG and Retrieval Security

- Embedding inversion
- Context window stuffing

#### 10. Agentic and Tool Use Security

- Autonomous action scope testing
- Tool result injection
- Federated or distributed agent security

#### 11. Supply Chain and Infrastructure Security

- Inference infrastructure security
- Container or runtime hardening
- MCP or plugin integrity

#### 12. Resilience and Chaos Engineering

- Chaos engineering for agents
- Dependency failure simulation
- Context loss or memory corruption

#### 13. Privacy-Enhancing Technology Testing

- Differential privacy budget validation
- Federated learning aggregation testing
- Anonymisation or pseudonymisation verification
- Consent management testing

#### 14. Compliance and Governance Testing

- NIST AI RMF control mapping
- EU AI Act or high-risk system testing
- Regulatory change testing
- Bias and fairness testing
- Explainability or decision logging
- Content policy enforcement
- Incident response playbook validation
- AI-BOM completeness validation

### Optional

#### 2. Quality and Assurance Testing

- Shadow mode or canary validation
- Load or stress testing
- Replay or regression testing

#### 6. Adversarial ML and Model Security

- Model inversion or extraction

#### 11. Supply Chain and Infrastructure Security

- Model DoS or resource exhaustion OWASP LLM04

#### 12. Resilience and Chaos Engineering

- Disaster recovery or failover testing

#### 13. Privacy-Enhancing Technology Testing

- Secure multi-party computation validation

## Recording Rules

When documenting testing decisions in `templates/test-matrix.md`, design notes, or release artifacts:

- list the categories that are in scope for the plugin or change
- record the validation approach used
- record the result or current gap
- record why a mandatory or recommended category is not applicable or deferred

## Tooling Examples

Suggested tooling from the category source list includes:

- `pytest`, `jest`, `playwright`, custom harnesses
- `mypy --strict`, `tsc`, `semgrep`, `OWASP ZAP`
- `pydantic`, `zod`, `syrupy`, `Hypothesis`, `fast-check`
- `promptfoo`, `braintrust`, `garak`, `schemathesis`, `openapi-diff`
- `trivy`, `snyk`, `dependabot`, `gitleaks`, `trufflehog`

These tools are examples, not rigid requirements. Equivalent tooling is acceptable when it provides comparable coverage.
