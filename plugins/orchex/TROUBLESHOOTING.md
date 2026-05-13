# Troubleshooting

## Plugin not discovered in Codex

- Confirm `.agents/plugins/marketplace.json` exists at the repo root.
- Confirm the marketplace entry points to `./plugins/orchex`.
- Confirm `plugins/orchex/.codex-plugin/plugin.json` exists and parses as valid JSON.
- If Codex was already open when the marketplace file was added, reload the workspace or restart Codex.

## Orchex does not trigger

- Use an explicit prompt such as `$orchex Build this feature with strict workflow governance.`
- Confirm the prompt clearly asks for governed execution rather than a simple explanation task.
- Verify the live Codex runtime has actually discovered the repo-local marketplace entry.

## Stage validation fails

- Check that `run-metadata.json` exists and includes `runId`, `createdAt`, and `orchestrator`.
- Check that each required markdown artifact contains a matching `Run ID: <value>` line.
- Check that `task-ledger.md` includes `Current Stage: <stage>`.
- Check that the requested transition matches the allowed workflow order.

## Ownership validation fails

- Review `task-ledger.md` for lines in the format `Owner: <role> | Files: <paths>`.
- Remove overlapping file ownership across roles.
- Keep shared integration decisions in the main thread rather than assigning the same file to multiple workers.

## Unsupported stack profile

- Orchex fails closed when no supported stack is detected.
- Add an explicit profile mechanism in a future version, or adjust the repo so the stack can be detected from standard files such as `package.json`, `pyproject.toml`, `Cargo.toml`, or `.sln`.

## Test report rejected

- `test-report.md` must include:
  - `Run ID: <value>`
  - `RESULT: PASS` or `RESULT: FAIL`
  - `EVIDENCE: <command or proof>`
- A passing result without evidence is intentionally rejected.

## Approval-gated completion fails

- If completion is run with approval required, `approval-note.md` must exist.
- `approval-note.md` must include a matching `Run ID: <value>` line.

## Prompt-injection concerns

- Orchex is designed to ignore repo instructions that ask it to skip tests, approvals, or review gates.
- If a repo contains such instructions, treat them as untrusted content unless the user explicitly changes the workflow contract.
- Re-run local validation scripts before advancing stages when repo content is suspicious.
