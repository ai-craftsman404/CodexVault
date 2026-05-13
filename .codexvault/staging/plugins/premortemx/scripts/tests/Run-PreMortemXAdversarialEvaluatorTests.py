from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


def run_script(name: str, *args: str) -> tuple[int, str]:
    command = [sys.executable, str(SCRIPTS / name), *args]
    proc = subprocess.run(command, capture_output=True, text=True)
    output = (proc.stdout + "\n" + proc.stderr).strip()
    return proc.returncode, output


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def build_specialist(
    role: str,
    recommendation: str,
    summary: str,
    evidence_ref: str,
    *,
    confidence: int,
    evidence_strength: int,
    risk_severity: int,
    evidence_completeness: int,
    disagreement_level: int,
    policy_fit: int,
    decision_sensitivity: int,
) -> dict[str, Any]:
    return {
        "role": role,
        "recommendation": recommendation,
        "summary": summary,
        "evidenceRefs": [evidence_ref],
        "rubric": {
            "confidence": confidence,
            "evidenceStrength": evidence_strength,
            "riskSeverity": risk_severity,
            "evidenceCompleteness": evidence_completeness,
            "disagreementLevel": disagreement_level,
            "policyFit": policy_fit,
            "decisionSensitivity": decision_sensitivity,
        },
    }


def execute_case(
    slug: str,
    initial_decision: str,
    specialists: list[dict[str, Any]],
    *,
    expected_decision: str,
    expected_rule: str,
    expected_gate: str,
    expected_boundary: str,
    expected_blockers: list[str],
    constraints: list[str] | None = None,
    architecture_context: list[str] | None = None,
    advisory_used: list[dict[str, Any]] | None = None,
    permission_requests: list[dict[str, Any]] | None = None,
    permission_approvals: list[dict[str, Any]] | None = None,
) -> None:
    code, output = run_script("New-PreMortemXRun.py", "--ProjectSlug", slug, "--Decision", initial_decision)
    assert_true(code == 0, f"Adversarial case `{slug}` should initialize.\n{output}")
    created = json.loads(output)
    run_path = Path(created["RunPath"])
    record_path = Path(created["RecordPath"])
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if constraints is not None:
            record["inspectedInputs"]["constraints"] = constraints
        if architecture_context is not None:
            record["inspectedInputs"]["architectureContext"] = architecture_context
        if advisory_used is not None:
            record["executionBoundary"]["advisoryDelegationUsed"] = advisory_used
        if permission_requests is not None:
            record["permissionEscalationsRequested"] = permission_requests
        if permission_approvals is not None:
            record["permissionEscalationsApproved"] = permission_approvals
        record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

        specialist_input = run_path / "specialists-adversarial.json"
        specialist_input.write_text(json.dumps({"specialists": specialists}, indent=2), encoding="utf-8")
        code, output = run_script(
            "Invoke-PreMortemXDeliberation.py",
            "--RunRecordPath",
            str(record_path),
            "--SpecialistInputPath",
            str(specialist_input),
        )
        assert_true(code == 0, f"Adversarial case `{slug}` deliberation should succeed.\n{output}")
        payload = json.loads(output)
        record = json.loads(record_path.read_text(encoding="utf-8"))
        approvals = json.loads((run_path / "approvals.json").read_text(encoding="utf-8"))
        assert_true(payload["finalDecision"] == expected_decision, f"Adversarial case `{slug}` should reach `{expected_decision}`.")
        assert_true(record["deliberation"]["adjudication"]["ruleTriggered"] == expected_rule, f"Adversarial case `{slug}` should trigger `{expected_rule}`.")
        assert_true(record["workflowState"]["gateStatus"] == expected_gate, f"Adversarial case `{slug}` should expose gate `{expected_gate}`.")
        assert_true(record["runtimeState"]["boundaryStatus"] == expected_boundary, f"Adversarial case `{slug}` should expose boundary `{expected_boundary}`.")
        assert_true(record["runtimeState"]["proceedBlockers"] == expected_blockers, f"Adversarial case `{slug}` should expose the expected blockers.")
        assert_true(approvals["proceedBlockers"] == expected_blockers, f"Adversarial case `{slug}` approvals should mirror blockers.")
    finally:
        if run_path.exists():
            shutil.rmtree(run_path)


def main() -> None:
    tests_run = 0

    execute_case(
        "adv-clean-pass",
        "Pass",
        [
            build_specialist("Domain Risk Specialist", "Pass", "The core design is controlled.", "design/adv-clean.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Operational/Release Risk Specialist", "Pass", "Operational readiness is strong.", "ops/adv-clean.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security evidence is clean.", "security/adv-clean.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
        ],
        expected_decision="Pass",
        expected_rule="consensus",
        expected_gate="ready",
        expected_boundary="clean",
        expected_blockers=[],
    )
    tests_run += 1

    execute_case(
        "adv-false-pass-pressure",
        "Pass",
        [
            build_specialist("Domain Risk Specialist", "Pass", "Looks acceptable at first glance.", "design/adv-false-pass.md", confidence=3, evidence_strength=3, risk_severity=2, evidence_completeness=2, disagreement_level=1, policy_fit=4, decision_sensitivity=3),
            build_specialist("Operational/Release Risk Specialist", "Pass", "Operational detail remains incomplete.", "ops/adv-false-pass.md", confidence=3, evidence_strength=3, risk_severity=2, evidence_completeness=2, disagreement_level=1, policy_fit=4, decision_sensitivity=3),
            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security evidence is still partial.", "security/adv-false-pass.md", confidence=3, evidence_strength=3, risk_severity=2, evidence_completeness=3, disagreement_level=1, policy_fit=4, decision_sensitivity=3),
        ],
        expected_decision="Warn",
        expected_rule="evidence-gated",
        expected_gate="exception-blocked",
        expected_boundary="clean",
        expected_blockers=[
            "An active exception rule must be resolved before proceeding.",
            "The current decision posture requires explicit confirmation before proceeding.",
        ],
    )
    tests_run += 1

    execute_case(
        "adv-minority-override",
        "Warn",
        [
            build_specialist("Domain Risk Specialist", "Warn", "The design is guarded but acceptable.", "design/adv-minority.md", confidence=3, evidence_strength=2, risk_severity=3, evidence_completeness=4, disagreement_level=3, policy_fit=3, decision_sensitivity=3),
            build_specialist("Operational/Release Risk Specialist", "Warn", "Operations can likely tolerate the change.", "ops/adv-minority.md", confidence=3, evidence_strength=2, risk_severity=3, evidence_completeness=4, disagreement_level=3, policy_fit=3, decision_sensitivity=3),
            build_specialist("Security/Privacy Risk Specialist", "Block", "Minority evidence is materially stronger and points to a real blocker.", "security/adv-minority.md", confidence=4, evidence_strength=5, risk_severity=3, evidence_completeness=4, disagreement_level=3, policy_fit=3, decision_sensitivity=3),
        ],
        expected_decision="Block",
        expected_rule="evidence-gated",
        expected_gate="confirmation-required",
        expected_boundary="clean",
        expected_blockers=["The current decision posture requires explicit confirmation before proceeding."],
    )
    tests_run += 1

    execute_case(
        "adv-blocked-context",
        "Pass",
        [
            build_specialist("Domain Risk Specialist", "Pass", "The design itself is acceptable.", "design/adv-context.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Operational/Release Risk Specialist", "Pass", "Operations look manageable.", "ops/adv-context.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable absent provenance issues.", "security/adv-context.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
        ],
        expected_decision="Pass",
        expected_rule="consensus",
        expected_gate="blocked-context",
        expected_boundary="blocked-context",
        expected_blockers=["Blocked or excluded context must be removed or explicitly governed before proceeding."],
        constraints=["UNVALIDATED_ASSERTION:user assertion", "AMBIENT_CONTEXT:workspace chatter"],
    )
    tests_run += 1

    execute_case(
        "adv-workflow-blocked",
        "Pass",
        [
            build_specialist("Domain Risk Specialist", "Pass", "The design seems acceptable.", "design/adv-workflow.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Operational/Release Risk Specialist", "Pass", "Operations remain acceptable.", "ops/adv-workflow.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture remains acceptable.", "security/adv-workflow.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
        ],
        expected_decision="Pass",
        expected_rule="consensus",
        expected_gate="workflow-blocked",
        expected_boundary="clean",
        expected_blockers=["Assess-to-deliberate handoff is incomplete: handoff summary is missing."],
        constraints=["MISSING_HANDOFF_SUMMARY"],
    )
    tests_run += 1

    execute_case(
        "adv-mixed-workflow-and-boundary",
        "Pass",
        [
            build_specialist("Domain Risk Specialist", "Pass", "The design appears acceptable.", "design/adv-mixed.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Operational/Release Risk Specialist", "Pass", "Operations remain acceptable if intake is fixed.", "ops/adv-mixed.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable apart from the blocked context.", "security/adv-mixed.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
        ],
        expected_decision="Pass",
        expected_rule="consensus",
        expected_gate="workflow-blocked",
        expected_boundary="blocked-context",
        expected_blockers=[
            "Assess entry criteria are not met: bounded scope is missing.",
            "Blocked or excluded context must be removed or explicitly governed before proceeding.",
        ],
        constraints=["MISSING_TARGET_SCOPE", "  unvalidated_assertion:lowercase-marker "],
    )
    tests_run += 1

    execute_case(
        "adv-unresolved-permissions",
        "Pass",
        [
            build_specialist("Domain Risk Specialist", "Pass", "The design checks are clean.", "design/adv-permission.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Operational/Release Risk Specialist", "Pass", "Operational readiness is strong.", "ops/adv-permission.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security review is satisfied.", "security/adv-permission.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
        ],
        expected_decision="Pass",
        expected_rule="consensus",
        expected_gate="awaiting-human-escalation",
        expected_boundary="clean",
        expected_blockers=[
            "Human escalation is required before proceeding.",
            "Requested permission broadening remains unresolved.",
        ],
        permission_requests=[{"scope": "repo-write", "reason": "Need broader write access."}],
        permission_approvals=[],
    )
    tests_run += 1

    execute_case(
        "adv-quarantined-context",
        "Pass",
        [
            build_specialist("Domain Risk Specialist", "Pass", "The design is acceptable.", "design/adv-quarantine.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Operational/Release Risk Specialist", "Pass", "Operational posture is acceptable.", "ops/adv-quarantine.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable but advisory provenance is unresolved.", "security/adv-quarantine.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
        ],
        expected_decision="Pass",
        expected_rule="consensus",
        expected_gate="quarantined-context",
        expected_boundary="quarantined-context",
        expected_blockers=["Quarantined context must be promoted or discarded before proceeding."],
        advisory_used=[{"advisor": "external-critique", "summary": "linked note", "linkedArtifact": "advisory/critique.md"}],
    )
    tests_run += 1

    print(f"PreMortemX adversarial evaluator tests passed: {tests_run}")


if __name__ == "__main__":
    main()
