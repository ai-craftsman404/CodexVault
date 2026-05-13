from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOV = ROOT / "governance"


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
        GOV / "prompts",
        GOV / "overlays",
        GOV / "roles",
        GOV / "controls",
        GOV / "policy-packs",
        GOV / "templates",
    ]
    for folder in folders:
        assert_true(folder.exists(), f"{folder} should exist.")
        assert_true((folder / "README.md").exists(), f"{folder / 'README.md'} should exist.")
    tests_run += 1

    prompt = GOV / "prompts" / "governance-prompt-core-risk-governance.md"
    overlay = GOV / "overlays" / "task-overlay-release-risk-gating.md"
    orchestrator = GOV / "roles" / "role-card-orchestrator.md"
    evidence_auditor = GOV / "roles" / "role-card-evidence-auditor.md"
    domain_risk = GOV / "roles" / "role-card-domain-risk-specialist.md"
    control = GOV / "controls" / "control-card-high-sensitivity-approval.md"
    policy_pack = GOV / "policy-packs" / "policy-pack-release-risk-core.md"
    template = GOV / "templates" / "template-card-release-risk-standard-summary.md"

    for path in [prompt, overlay, orchestrator, evidence_auditor, domain_risk, control, policy_pack, template]:
        assert_true(path.exists(), f"{path.name} should exist.")
    tests_run += 1

    common_required = [
        "Status: `active`",
        "Version: `v5a-1`",
        "Owner: `PreMortemX Maintainers`",
        "Last Updated: `2026-05-09`",
        "## Skim Summary",
        "## Change And Review Notes",
        "## Critical Summary",
    ]
    for path in [prompt, overlay, orchestrator, evidence_auditor, domain_risk, control, policy_pack, template]:
        require_lines(read(path), common_required, path.name)
    tests_run += 1

    require_lines(
        read(prompt),
        [
            "Asset Type: `Governance Prompt`",
            "## Identity And Role",
            "## Decision Priorities",
            "## Safety Boundaries",
            "## Approval Posture",
            "## Evidence Discipline",
            "## Default Failure Behavior",
        ],
        prompt.name,
    )
    tests_run += 1

    require_lines(
        read(overlay),
        [
            "Asset Type: `Task Overlay`",
            "## Parent Prompt",
            "## Task Mode",
            "## Extra Rules",
            "## Explicit Exclusions",
            "## Evidence Expectations",
            "## Escalation Behavior",
            "## Linked Controls",
        ],
        overlay.name,
    )
    tests_run += 1

    for role_path in [orchestrator, evidence_auditor, domain_risk]:
        role_text = read(role_path)
        require_lines(
            role_text,
            [
                "Asset Type: `Role Card`",
                "## When This Role Is Used",
                "## Inputs",
                "## Outputs",
                "## Must Do",
                "## Must Not Do",
                "## Escalation Behavior",
                "## Linked Controls",
            ],
            role_path.name,
        )
        assert_true("Approval Tier" not in role_text, f"{role_path.name} should not embed control-card approval sections.")
    tests_run += 1

    control_text = read(control)
    require_lines(
        control_text,
        [
            "Asset Type: `Control Card`",
            "## Trigger",
            "## Effect",
            "## Approval Tier",
            "## Evidence Requirement",
            "## Override Rule",
            "## Audit Expectation",
            "## Exceptions",
        ],
        control.name,
    )
    assert_true("## Must Do" not in control_text, "Control card should stay separated from role-card sections.")
    tests_run += 1

    require_lines(
        read(policy_pack),
        [
            "Asset Type: `Policy Pack`",
            "## Applies To",
            "## Included Controls",
            "## Approval Model",
            "## Required Templates",
            "## Exceptions",
        ],
        policy_pack.name,
    )
    tests_run += 1

    require_lines(
        read(template),
        [
            "Asset Type: `Template Card`",
            "## Used By",
            "## Variables",
            "## Output Contract",
            "## Linked Governance Assets",
            "## Validation Notes",
        ],
        template.name,
    )
    tests_run += 1

    prompt_text = read(prompt)
    assert_true(as_doc_path(prompt) in read(overlay), "Overlay should link back to the governance prompt.")
    assert_true(as_doc_path(control) in read(overlay), "Overlay should link to the control card.")
    assert_true(as_doc_path(policy_pack) in read(prompt), "Governance prompt should link to the policy pack.")
    assert_true(as_doc_path(template) in read(policy_pack), "Policy pack should link to the template card.")
    tests_run += 1

    print(f"PreMortemX v5a tests passed: {tests_run}")


if __name__ == "__main__":
    main()
