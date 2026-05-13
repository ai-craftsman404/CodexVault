from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / "workflow"


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
        WORKFLOW / "lifecycle",
        WORKFLOW / "stages",
        WORKFLOW / "approvals",
        WORKFLOW / "handoffs",
        WORKFLOW / "exceptions",
    ]
    for folder in folders:
        assert_true(folder.exists(), f"{folder} should exist.")
        assert_true((folder / "README.md").exists(), f"{folder / 'README.md'} should exist.")
    tests_run += 1

    lifecycle = WORKFLOW / "lifecycle" / "lifecycle-map-core-release-risk.md"
    intake = WORKFLOW / "stages" / "stage-definition-intake.md"
    assess = WORKFLOW / "stages" / "stage-definition-assess.md"
    approval = WORKFLOW / "approvals" / "approval-playbook-high-sensitivity-release-decision.md"
    handoff = WORKFLOW / "handoffs" / "handoff-summary-assess-to-deliberate.md"
    exception = WORKFLOW / "exceptions" / "exception-rule-missing-evidence-reentry.md"

    for path in [lifecycle, intake, assess, approval, handoff, exception]:
        assert_true(path.exists(), f"{path.name} should exist.")
    tests_run += 1

    common_required = [
        "Status: `active`",
        "Version: `v5b-1`",
        "Owner: `PreMortemX Maintainers`",
        "Last Updated: `2026-05-09`",
        "## Skim Summary",
        "## Linked Assets",
        "## Change And Review Notes",
        "## Critical Summary",
    ]
    for path in [lifecycle, intake, assess, approval, handoff, exception]:
        require_lines(read(path), common_required, path.name)
    tests_run += 1

    require_lines(
        read(lifecycle),
        [
            "Asset Type: `Lifecycle Map`",
            "## Lifecycle Rail",
            "## Entry Point",
            "## Terminal States",
            "## Re-entry Paths",
            "## Linked Stage Definitions",
            "`Intake`",
            "`Assess`",
            "`Deliberate`",
            "`Approve/Block`",
            "`Monitor`",
            "`Revisit`",
        ],
        lifecycle.name,
    )
    tests_run += 1

    for stage in [intake, assess]:
        require_lines(
            read(stage),
            [
                "Asset Type: `Stage Definition`",
                "## Entry Criteria",
                "## Required Inputs",
                "## Actions",
                "## Required Outputs",
                "## Approval Requirement",
                "## Failure Path",
                "## Next Stage",
            ],
            stage.name,
        )
    tests_run += 1

    require_lines(
        read(approval),
        [
            "Asset Type: `Approval Playbook`",
            "## Applies To",
            "## Approval Tier",
            "## Decision Owner",
            "## Required Evidence",
            "## Allowed Outcomes",
            "## Escalation Path",
            "## Audit Trail",
        ],
        approval.name,
    )
    tests_run += 1

    require_lines(
        read(handoff),
        [
            "Asset Type: `Handoff Summary`",
            "## From And To",
            "## Decision Made",
            "## Decision Rationale",
            "## Evidence Used",
            "## Open Issues",
            "## Next Owner",
            "## Next Required Action",
        ],
        handoff.name,
    )
    tests_run += 1

    require_lines(
        read(exception),
        [
            "Asset Type: `Exception/Re-entry Rule`",
            "## Trigger",
            "## Severity",
            "## Re-entry Stage",
            "## Required Owner",
            "## Expected Follow-up",
            "## Temporary Mitigation",
        ],
        exception.name,
    )
    tests_run += 1

    assert_true("Approval Tier" not in read(intake), "Stage definitions should not absorb approval-playbook sections.")
    assert_true("Next Stage" not in read(approval), "Approval playbook should stay distinct from stage definitions.")
    tests_run += 1

    lifecycle_text = read(lifecycle)
    assert_true(as_doc_path(intake) in lifecycle_text, "Lifecycle should link to intake stage.")
    assert_true(as_doc_path(assess) in lifecycle_text, "Lifecycle should link to assess stage.")
    assert_true(as_doc_path(approval) in lifecycle_text, "Lifecycle should link to approval playbook.")
    assert_true(as_doc_path(exception) in lifecycle_text, "Lifecycle should link to exception rule.")
    tests_run += 1

    assert_true(as_doc_path(handoff) in read(assess), "Assess stage should link to the handoff summary.")
    assert_true(as_doc_path(approval) in read(handoff), "Handoff summary should link to the approval playbook.")
    assert_true(as_doc_path(assess) in read(exception), "Exception rule should link back to the assess stage.")
    tests_run += 1

    print(f"PreMortemX v5b tests passed: {tests_run}")


if __name__ == "__main__":
    main()
