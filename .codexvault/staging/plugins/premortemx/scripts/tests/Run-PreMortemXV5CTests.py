from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def as_doc_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def require_lines(text: str, required: list[str], label: str) -> None:
    for item in required:
        assert_true(item in text, f"{label} should contain `{item}`.")


def main() -> None:
    tests_run = 0

    folders = [
        RUNTIME / "policies",
        RUNTIME / "context",
        RUNTIME / "traces",
        RUNTIME / "dashboards",
        RUNTIME / "factsheets",
    ]
    for folder in folders:
        assert_true(folder.exists(), f"{folder} should exist.")
        assert_true((folder / "README.md").exists(), f"{folder / 'README.md'} should exist.")
    tests_run += 1

    control_tower = RUNTIME / "dashboards" / "control-tower-view-default-release-risk.md"
    factsheet = RUNTIME / "factsheets" / "governed-run-factsheet-release-risk-synthetic.md"
    boundary = RUNTIME / "policies" / "boundary-enforcement-panel-release-risk-synthetic.md"
    resolver = RUNTIME / "policies" / "policy-resolver-record-release-risk-synthetic.md"
    context = RUNTIME / "context" / "context-contract-release-risk-synthetic.md"
    trace = RUNTIME / "traces" / "runtime-trace-summary-release-risk-synthetic.md"

    for path in [control_tower, factsheet, boundary, resolver, context, trace]:
        assert_true(path.exists(), f"{path.name} should exist.")
    tests_run += 1

    common_required = [
        "Status: `active`",
        "Version: `v5c-1`",
        "Owner: `PreMortemX Maintainers`",
        "Last Updated: `2026-05-09`",
        "## Skim Summary",
        "## Linked Assets",
        "## Change And Review Notes",
        "## Critical Summary",
    ]
    for path in [control_tower, factsheet, boundary, resolver, context, trace]:
        require_lines(read(path), common_required, path.name)
    tests_run += 1

    require_lines(
        read(control_tower),
        [
            "Asset Type: `Control Tower View`",
            "## Active Policy Profile",
            "## Runtime Mode",
            "## Approval Posture",
            "## Open Breaches And Exceptions",
            "## Recent Adjudications",
            "## Attention Queue",
        ],
        control_tower.name,
    )
    tests_run += 1

    require_lines(
        read(factsheet),
        [
            "Asset Type: `Governed Run Factsheet`",
            "## Run Identity",
            "## Scope",
            "## Active Policy And Config",
            "## Approval Events",
            "## Triggered Thresholds",
            "## Final Adjudication",
            "## Linked Artifacts",
            "Run ID: `pmx-synthetic-release-v5c-001`",
        ],
        factsheet.name,
    )
    tests_run += 1

    require_lines(
        read(boundary),
        [
            "Asset Type: `Boundary And Enforcement Panel`",
            "## Trusted Instructions",
            "## Allowed Evidence Classes",
            "## Blocked Or Excluded Context",
            "## Runtime Restrictions",
            "## Approval Tier",
            "## Escalation Path",
        ],
        boundary.name,
    )
    tests_run += 1

    require_lines(
        read(resolver),
        [
            "Asset Type: `Policy Resolver Record`",
            "## Task",
            "## Selected Policy Pack",
            "## Selected Model And Runtime",
            "## Enabled Controls",
            "## Disabled Controls",
            "## Feature Flags Used",
            "## Selection Rationale",
        ],
        resolver.name,
    )
    tests_run += 1

    require_lines(
        read(context),
        [
            "Asset Type: `Context Contract`",
            "## Source Context Class",
            "## Allowed Downstream Target",
            "## Required Transformation",
            "## Prohibited Carry-forward",
            "## Retention Expectation",
        ],
        context.name,
    )
    tests_run += 1

    require_lines(
        read(trace),
        [
            "Asset Type: `Runtime Trace Summary`",
            "## Key Runtime Events",
            "## Approvals Triggered",
            "## Controls Triggered",
            "## Override Checks",
            "## Final Adjudication Path",
        ],
        trace.name,
    )
    tests_run += 1

    assert_true("Selected Policy Pack" not in read(control_tower), "Control tower view should not absorb resolver sections.")
    assert_true("## Triggered Thresholds" not in read(boundary), "Boundary panel should stay distinct from run factsheets.")
    tests_run += 1

    assert_true(as_doc_path(factsheet) in read(control_tower), "Control tower should link to the governed run factsheet.")
    assert_true(as_doc_path(resolver) in read(factsheet), "Factsheet should link to the policy resolver record.")
    assert_true(as_doc_path(boundary) in read(factsheet), "Factsheet should link to the boundary panel.")
    assert_true(as_doc_path(context) in read(boundary), "Boundary panel should link to the context contract.")
    assert_true(as_doc_path(trace) in read(context), "Context contract should link to the runtime trace summary.")
    tests_run += 1

    assert_true(as_doc_path(control_tower) in read(resolver), "Resolver should link back to the control tower.")
    assert_true(as_doc_path(factsheet) in read(trace), "Trace summary should link to the governed run factsheet.")
    tests_run += 1

    print(f"PreMortemX v5c tests passed: {tests_run}")


if __name__ == "__main__":
    main()
