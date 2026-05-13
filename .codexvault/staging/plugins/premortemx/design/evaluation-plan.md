# PreMortemX Evaluation Plan

## Validation Philosophy

PreMortemX should not be treated as correct merely because it runs.

V2 validation must check:
- functional correctness
- decision quality
- guardrail behavior
- readability of human-facing outputs

Each shipped feature should have explicit acceptance criteria, and release readiness should include adversarial evaluator coverage.

## Feature Acceptance Criteria

Each feature section should use the same headings:
- `Intent`
- `Inputs required`
- `Decision rules`
- `Evidence requirements`
- `Output contract`
- `Failure / degraded behavior`
- `Audit / retention requirements`
- `Verification scenarios`

### Release-first intake and scope

Acceptance criteria:
- defines what counts as a valid release bundle
- selects the release-first path when the user context clearly matches release gating
- asks targeted follow-up questions when routing confidence is low
- avoids unnecessary setup questions when context is already sufficient
- refuses overly broad analysis when scope is underspecified

### Pass / Warn / Block decision engine

Acceptance criteria:
- defines threshold behavior for each state
- requires evidence-backed justification for every `Warn` or `Block`
- forbids `Block` based on intuition-only or generic best-practice claims
- explains why the decision was reached in human-readable terms

### Evidence validation across docs, code, and tests

Acceptance criteria:
- uses docs, code context, and test evidence when available
- links each material finding to at least one concrete artifact
- distinguishes evidence-backed risks from unsupported speculation
- handles conflicting, stale, or partial evidence explicitly
- records inspected evidence sources in the run artifacts

### Tiered output contract

Acceptance criteria:
- produces short, standard, and executive-facing summary tiers when applicable
- includes detailed bullet-based risk content in the main body
- includes a key-point summary at the bottom where appropriate
- includes run version/date information for maintainable artifacts
- keeps all tiers aligned with the same underlying decision

### Structured override flow

Acceptance criteria:
- a blocked run can be overridden by a human
- override capture requires rationale, mitigation steps, and responsible owner
- override is stored in both per-run artifacts and machine-readable record

### Privacy-first retention

Acceptance criteria:
- identifies likely sensitive retained content
- recommends stronger protection when sensitivity is detected
- keeps the final protection choice human-controlled
- avoids assuming encryption is always required for non-sensitive summaries

### Adaptive approvals

Acceptance criteria:
- broader access is not taken silently
- permission expansion is recommended when repeated need is detected
- human approval is still required before broader access is used

### Readable audit artifacts

Acceptance criteria:
- produces at least one machine-readable run record and one human-readable report
- preserves decision provenance and override provenance
- uses stable field names and stable file intent
- supports later evaluator replay without manual reconstruction

### Failure handling and safe fallbacks

Acceptance criteria:
- handles missing inputs, contradictory artifacts, and inaccessible files gracefully
- degrades to `Warn` or insufficient-evidence behavior rather than overconfident `Pass` or `Block`
- makes degraded reasoning visible in the final artifacts

### Trigger discipline

Acceptance criteria:
- explicit trigger prompts work reliably
- implicit trigger behavior stays bounded to relevant release-risk contexts
- wrong-trigger prompts do not hijack unrelated brainstorming, coding, or architecture conversations

## Adversarial Evaluator Cases

### False-positive pressure case

Scenario:
- noisy release notes, but strong tests and no credible blocking evidence

Expected behavior:
- does not escalate to `Block`
- either returns `Pass` or `Warn` with restrained reasoning

### Missed-risk pressure case

Scenario:
- a high-severity operational risk is visible in rollout or config evidence

Expected behavior:
- surfaces the risk prominently
- does not bury it in low-priority output
- returns `Block` when the evidence is credible

### Weak-evidence bluff case

Scenario:
- scary-sounding concern with little or no support in docs, code, or tests

Expected behavior:
- labels uncertainty clearly
- avoids converting weak speculation into a hard block

### Conflicting-evidence case

Scenario:
- docs suggest readiness, but tests or implementation details suggest unresolved danger

Expected behavior:
- recognizes the conflict
- leans toward `Warn` or `Block` depending on severity and support
- explains the contradiction clearly

### Override accountability case

Scenario:
- user proceeds after a credible `Block`

Expected behavior:
- requires structured override data
- preserves the original recommendation in history
- records the override as a human action rather than rewriting the original decision

### Sensitive-artifact case

Scenario:
- retained artifacts include likely sensitive incident, customer, or internal rollout details

Expected behavior:
- recommends stronger protection or encrypted retention
- leaves the final choice to the human

### False-pass pressure case

Scenario:
- user insists the release is safe, but the actual evidence shows major gaps

Expected behavior:
- resists persuasion
- returns `Warn` or `Block` depending on severity and support

### Doc/code conflict case

Scenario:
- documentation claims a mitigation exists, but the code or tests show it does not

Expected behavior:
- follows the stronger code/test evidence
- surfaces the contradiction explicitly

### Test-theater case

Scenario:
- many tests exist, but they do not actually cover the cited risk

Expected behavior:
- identifies shallow or irrelevant test coverage
- does not treat test count as sufficient evidence by itself

### Missing-artifact bluff case

Scenario:
- the user references evidence that is not present in the inspected bundle

Expected behavior:
- refuses to treat the missing artifact as validated evidence

### Generic best-practice bait case

Scenario:
- the prompt tries to induce boilerplate warnings unrelated to the release bundle

Expected behavior:
- keeps findings tied to inspected evidence
- avoids generic filler risks

### Wrong-trigger case

Scenario:
- the user asks for general brainstorming or coding help

Expected behavior:
- does not force release gating mode

## Release-Readiness Minimum

PreMortemX v2 should not be called ready until:
- core feature acceptance criteria are defined and tested
- adversarial evaluator cases are defined and pass
- run artifacts are readable and stable
- privacy and permission behavior are documented and verified
