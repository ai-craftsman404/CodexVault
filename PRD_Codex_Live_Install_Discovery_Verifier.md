# PRD: Codex Live Install and Discovery Verifier

## 1. Overview

### Product name

Codex Live Install Verifier

### Purpose

A reusable workflow or helper system that verifies whether a locally prepared Codex plugin or skill is actually discovered, installable, and invokable in the real Codex UI/runtime.

### Goal

Reduce the manual effort and inconsistency in the final live verification step that cannot be proven by local file validation alone.

## 2. Problem

Static and local checks can confirm:

- manifest structure
- file layout
- marketplace wiring
- local scripts
- release artifacts

But they cannot prove:

- Codex UI discovers the plugin or skill
- install flow works in the real runtime
- invocation works after installation
- the runtime presents the extension correctly

This final step remains repetitive, manual, and easy to perform inconsistently.

## 3. Users

### Primary users

- internal Codex plugin builders
- internal Codex skill builders
- maintainers of many reusable Codex extensions

## 4. Core Use Case

Given a locally prepared plugin or skill, the verifier should guide or assist a real live Codex verification flow and produce a pass/fail report.

## 5. Objectives

- standardize live verification
- reduce missed discovery/install issues
- produce reusable verification evidence
- make final runtime testing faster and more reliable

## 6. Non-Goals

For v1, this verifier should not:

- replace the real Codex runtime
- fake install/discovery success
- publish plugins
- make product decisions for the user

## 7. Functional Requirements

### 7.1 Verification intake

The verifier must accept:

- plugin or skill name
- local path
- expected manifest or skill entrypoint
- expected invocation method
- expected display name and short description

### 7.2 Live verification checklist

The verifier must check or guide checking:

- plugin or skill appears in Codex discovery surface
- display name is correct
- description is correct
- install action is available
- installation completes
- post-install invocation is available
- invocation behaves as expected at a smoke-test level

### 7.3 Output

The verifier must produce:

- pass/fail per step
- screenshots or notes where possible
- final verification summary
- issues found
- recommended fixes

### 7.4 Reusability

The verifier must be reusable across future Codex plugins and skills.

## 8. Suggested V1 Shape

The simplest useful v1 can be:

- a skill or guided workflow
- a standard live-verification checklist
- a report template
- optional browser or UI assistance if runtime tooling allows

## 9. Acceptance Criteria

V1 is successful if it can:

- consistently guide live install/discovery verification
- produce a standard verification report
- catch discovery/install/invocation issues missed by static checks
- be reused across multiple Codex plugins and skills

## 10. Roadmap

### V1

- guided live verification checklist
- standard report output
- reusable workflow across plugins and skills

### V2

- partial UI automation where supported
- screenshot capture and structured evidence
- regression comparison against prior runs

### V3

- portfolio-wide live verification dashboard
- scheduled re-verification after plugin changes
- deeper runtime behavior smoke tests

## 11. Ultimate Deliverable

A reusable last-mile Codex verification workflow that confirms real UI discovery, installability, and basic invocation behavior for any future Codex plugin or skill.
