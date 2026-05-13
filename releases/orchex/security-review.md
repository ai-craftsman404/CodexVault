# Security and Privacy Review

## Plugin

- Plugin name: orchex
- Version: 0.1.0
- Review date: 2026-04-30
- Reviewer: Codex main thread

## Data Access

- Local files read:
  - repository root for stack detection
  - run artifact files under the selected Orchex run directory
- Local files written:
  - `run-summary.md` in the run directory
  - plugin-local docs and scripts during development
- External services accessed:
  - none in V1 plugin runtime
- User data categories:
  - source code
  - local run artifacts
  - test and review notes
- Sensitive data categories:
  - potentially whatever is already present in the repo or artifact files

## Secrets and Credentials

- Requires secrets: no
- Secret names: none
- Storage guidance: no plugin-owned secret storage
- `.env.example` required: no
- Public repo secret scan complete: no

## Network and External Services

| Service | Purpose | Auth Required | Data Sent | Risk |
| --- | --- | --- | --- | --- |
| none | N/A | no | none | low |

## App and MCP Permissions

- App connectors: none
- MCP servers: none
- Read permissions:
  - local repository files
  - run artifact files
- Write permissions:
  - run summary generation
  - normal plugin development files
- Destructive actions:
  - none designed into V1 scripts
- Approval expectations:
  - optional policy gate before completion; current implementation uses `approval-note.md` when configured

## Prompt Injection and Untrusted Content

- Untrusted sources:
  - repository files
  - user instructions
  - generated artifacts
- Prompt-injection risk:
  - medium; repo content may attempt to persuade the agent to skip tests or approvals
- Mitigations:
  - keep workflow contract explicit in skills
  - use script-backed validation rather than prompt-only assertions
  - fail closed on unsupported stack detection
  - require run metadata and matching run IDs across artifacts
- User warnings required:
  - yes; V1 does not yet provide strong machine-checkable defenses against all artifact tampering or prompt-injection patterns

## Scripts

| Script | Side Effects | Risk | Mitigation |
| --- | --- | --- | --- |
| `resolve-stack-profile.ps1` | Reads repo files to infer commands | low | Read-only behavior; fail closed on unsupported stacks |
| `validate-artifacts.ps1` | Reads artifact files and exits non-zero on failures | low | No writes; checks for non-empty and non-placeholder content |
| `validate-stage.ps1` | Reads artifacts and blocks invalid progression | low to medium | No writes; explicit transition map and evidence checks |
| `summarize-run.ps1` | Writes `run-summary.md` | low | Writes only to caller-selected run directory |

## Public Release Decision

- Safe to publish: not yet
- Required changes:
  - verify live plugin loading and trigger behavior in Codex
  - complete a public secret scan and release packaging review
- Residual risks:
  - file-based approval and artifact integrity are still lightweight
  - stale-artifact reuse is reduced by run ID checks, but stronger cross-run isolation checks are still absent
  - prompt-injection resistance relies mainly on the workflow contract and local validation gates rather than deep semantic inspection
  - E2E coverage now includes realistic mini-repos, but live Codex runtime verification is still needed before public release
