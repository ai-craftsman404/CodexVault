from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
PLUGIN_ROOT = ROOT
CALIBRATION_DB = PLUGIN_ROOT / "calibration" / "premortemx-calibration-python.sqlite"


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


def execute_workflow_case(
    project_slug: str,
    initial_decision: str,
    specialists: list[dict[str, Any]],
    *,
    expected_decision: str,
    expected_rule_triggered: str,
    expected_gate_status: str,
    expected_approval_status: str,
    expected_current_action: str,
    expected_next_stage: str,
    expected_allowed_next_stage: str | None,
    expected_proceed_allowed: bool,
    expected_human_escalation: bool,
    expected_active_exception_rule: str | None,
    expected_blockers: list[str],
    expected_boundary_status: str,
    expected_blocked_context_classes: list[str],
    expected_carry_forward_allowed: bool,
    expected_transformation_status: str,
    expected_assess_entry_status: str,
    expected_assess_entry_blockers: list[str],
    expected_deliberate_handoff_status: str,
    expected_handoff_blockers: list[str],
    permission_requests: list[dict[str, Any]] | None = None,
    permission_approvals: list[dict[str, Any]] | None = None,
    constraints: list[str] | None = None,
    architecture_context: list[str] | None = None,
    implementation_context: list[str] | None = None,
    advisory_used: list[dict[str, Any]] | None = None,
) -> None:
    code, output = run_script("New-PreMortemXRun.py", "--ProjectSlug", project_slug, "--Decision", initial_decision)
    assert_true(code == 0, f"Workflow case `{project_slug}` should initialize successfully.\n{output}")
    created = json.loads(output)
    run_path = Path(created["RunPath"])
    record_path = Path(created["RecordPath"])
    try:
        if permission_requests is not None or permission_approvals is not None:
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["permissionEscalationsRequested"] = permission_requests or []
            record["permissionEscalationsApproved"] = permission_approvals or []
            if constraints is not None:
                record["inspectedInputs"]["constraints"] = constraints
            if architecture_context is not None:
                record["inspectedInputs"]["architectureContext"] = architecture_context
            if implementation_context is not None:
                record["inspectedInputs"]["implementationContext"] = implementation_context
            if advisory_used is not None:
                record["executionBoundary"]["advisoryDelegationUsed"] = advisory_used
            record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        elif any(value is not None for value in (constraints, architecture_context, implementation_context, advisory_used)):
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if constraints is not None:
                record["inspectedInputs"]["constraints"] = constraints
            if architecture_context is not None:
                record["inspectedInputs"]["architectureContext"] = architecture_context
            if implementation_context is not None:
                record["inspectedInputs"]["implementationContext"] = implementation_context
            if advisory_used is not None:
                record["executionBoundary"]["advisoryDelegationUsed"] = advisory_used
            record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

        specialist_input = run_path / "specialists-matrix.json"
        specialist_input.write_text(json.dumps({"specialists": specialists}, indent=2), encoding="utf-8")
        code, output = run_script(
            "Invoke-PreMortemXDeliberation.py",
            "--RunRecordPath",
            str(record_path),
            "--SpecialistInputPath",
            str(specialist_input),
        )
        assert_true(code == 0, f"Workflow case `{project_slug}` deliberation should succeed.\n{output}")
        payload = json.loads(output)
        record = json.loads(record_path.read_text(encoding="utf-8"))
        approvals = json.loads((run_path / "approvals.json").read_text(encoding="utf-8"))
        start_here = (run_path / "start-here.md").read_text(encoding="utf-8")
        summary_short = (run_path / "summary-short.md").read_text(encoding="utf-8")

        assert_true(payload["finalDecision"] == expected_decision, f"Workflow case `{project_slug}` should reach `{expected_decision}`.")
        assert_true(record["status"] == "adjudicated", f"Workflow case `{project_slug}` should move the top-level run status to adjudicated.")
        assert_true(record["deliberation"]["adjudication"]["ruleTriggered"] == expected_rule_triggered, f"Workflow case `{project_slug}` should record `{expected_rule_triggered}`.")
        assert_true(record["workflowState"]["gateStatus"] == expected_gate_status, f"Workflow case `{project_slug}` should expose gate status `{expected_gate_status}`.")
        assert_true(record["workflowState"]["nextStage"] == expected_next_stage, f"Workflow case `{project_slug}` should expose next stage `{expected_next_stage}`.")
        assert_true(record["workflowState"]["allowedNextStage"] == expected_allowed_next_stage, f"Workflow case `{project_slug}` should expose allowed next stage `{expected_allowed_next_stage}`.")
        assert_true(record["workflowState"]["activeExceptionRule"] == expected_active_exception_rule, f"Workflow case `{project_slug}` should expose the expected exception rule.")
        assert_true(record["workflowState"]["assessEntryStatus"] == expected_assess_entry_status, f"Workflow case `{project_slug}` should expose assess entry status `{expected_assess_entry_status}`.")
        assert_true(record["workflowState"]["assessEntryBlockers"] == expected_assess_entry_blockers, f"Workflow case `{project_slug}` should expose assess entry blockers `{expected_assess_entry_blockers}`.")
        assert_true(record["workflowState"]["deliberateHandoffStatus"] == expected_deliberate_handoff_status, f"Workflow case `{project_slug}` should expose deliberate handoff status `{expected_deliberate_handoff_status}`.")
        assert_true(record["workflowState"]["handoffBlockers"] == expected_handoff_blockers, f"Workflow case `{project_slug}` should expose handoff blockers `{expected_handoff_blockers}`.")
        assert_true(record["workflowState"]["blockedBy"] == expected_blockers, f"Workflow case `{project_slug}` should mirror blockers in workflow state.")
        assert_true(record["runtimeState"]["proceedAllowed"] is expected_proceed_allowed, f"Workflow case `{project_slug}` should expose proceedAllowed=`{expected_proceed_allowed}`.")
        assert_true(record["runtimeState"]["proceedBlockers"] == expected_blockers, f"Workflow case `{project_slug}` should expose the expected proceed blockers.")
        assert_true(record["runtimeState"]["boundaryStatus"] == expected_boundary_status, f"Workflow case `{project_slug}` should expose boundary status `{expected_boundary_status}`.")
        assert_true(record["runtimeState"]["blockedContextClasses"] == expected_blocked_context_classes, f"Workflow case `{project_slug}` should expose blocked context classes `{expected_blocked_context_classes}`.")
        assert_true(record["runtimeState"]["carryForwardAllowed"] is expected_carry_forward_allowed, f"Workflow case `{project_slug}` should expose carryForwardAllowed=`{expected_carry_forward_allowed}`.")
        assert_true(record["runtimeState"]["transformationStatus"] == expected_transformation_status, f"Workflow case `{project_slug}` should expose transformation status `{expected_transformation_status}`.")
        assert_true(record["deliberation"]["overrideModel"]["humanEscalationRequired"] is expected_human_escalation, f"Workflow case `{project_slug}` should expose the expected human escalation posture.")
        assert_true(approvals["approvalStatus"] == expected_approval_status, f"Workflow case `{project_slug}` should expose approval status `{expected_approval_status}`.")
        assert_true(approvals["recommendation"] == expected_decision, f"Workflow case `{project_slug}` approvals should mirror the final decision recommendation.")
        assert_true(approvals["currentAction"] == expected_current_action, f"Workflow case `{project_slug}` should expose current action `{expected_current_action}`.")
        assert_true(approvals["playbookGateStatus"] == expected_gate_status, f"Workflow case `{project_slug}` should mirror gate status into approvals.")
        assert_true(approvals["allowedNextStage"] == expected_allowed_next_stage, f"Workflow case `{project_slug}` should mirror allowed next stage into approvals.")
        assert_true(approvals["proceedAllowed"] is expected_proceed_allowed, f"Workflow case `{project_slug}` approvals should expose proceedAllowed=`{expected_proceed_allowed}`.")
        assert_true(approvals["proceedBlockers"] == expected_blockers, f"Workflow case `{project_slug}` approvals should mirror the expected blockers.")
        assert_true(approvals["boundaryStatus"] == expected_boundary_status, f"Workflow case `{project_slug}` approvals should mirror boundary status `{expected_boundary_status}`.")
        assert_true(approvals["blockedContextClasses"] == expected_blocked_context_classes, f"Workflow case `{project_slug}` approvals should mirror blocked context classes `{expected_blocked_context_classes}`.")
        assert_true(approvals["carryForwardAllowed"] is expected_carry_forward_allowed, f"Workflow case `{project_slug}` approvals should mirror carryForwardAllowed=`{expected_carry_forward_allowed}`.")
        assert_true(approvals["transformationStatus"] == expected_transformation_status, f"Workflow case `{project_slug}` approvals should mirror transformation status `{expected_transformation_status}`.")
        assert_true(f"Gate status: `{expected_gate_status}`" in start_here, f"Workflow case `{project_slug}` start-here should show gate status.")
        assert_true(f"Assess entry status: `{expected_assess_entry_status}`" in start_here, f"Workflow case `{project_slug}` start-here should show assess entry status.")
        assert_true(f"Deliberate handoff status: `{expected_deliberate_handoff_status}`" in start_here, f"Workflow case `{project_slug}` start-here should show deliberate handoff status.")
        assert_true(f"Boundary status: `{expected_boundary_status}`" in start_here, f"Workflow case `{project_slug}` start-here should show boundary status.")
        assert_true(f"Gate status: `{expected_gate_status}`" in summary_short, f"Workflow case `{project_slug}` short summary should show gate status.")
        assert_true(f"Assess entry status: `{expected_assess_entry_status}`" in summary_short, f"Workflow case `{project_slug}` short summary should show assess entry status.")
        assert_true(f"Deliberate handoff status: `{expected_deliberate_handoff_status}`" in summary_short, f"Workflow case `{project_slug}` short summary should show deliberate handoff status.")
        assert_true(f"Boundary status: `{expected_boundary_status}`" in summary_short, f"Workflow case `{project_slug}` short summary should show boundary status.")
        assert_true(f"Proceed allowed: `{'Yes' if expected_proceed_allowed else 'No'}`" in start_here, f"Workflow case `{project_slug}` start-here should show proceedAllowed.")
    finally:
        if run_path.exists():
            shutil.rmtree(run_path)


def main() -> None:
    tests_run = 0
    index_path = PLUGIN_ROOT / "registry" / "runs" / "index.jsonl"
    quality_log_path = PLUGIN_ROOT / "registry" / "quality-review-log.json"
    views_root = PLUGIN_ROOT / "registry" / "views"
    index_backup = index_path.read_text(encoding="utf-8") if index_path.exists() else None
    quality_backup = quality_log_path.read_text(encoding="utf-8") if quality_log_path.exists() else None
    views_backup = views_root.exists()

    code, output = run_script("New-PreMortemXRun.py", "--ProjectSlug", "py-sample-api", "--Decision", "Warn")
    assert_true(code == 0, f"Python run initialization should succeed.\n{output}")
    created = json.loads(output)
    run_path = Path(created["RunPath"])
    record_path = Path(created["RecordPath"])
    arch_run_path: Path | None = None
    arch_record_path: Path | None = None

    try:
        assert_true(run_path.exists(), "Python-created run directory should exist.")
        summary_short = (run_path / "summary-short.md").read_text(encoding="utf-8")
        summary_standard = (run_path / "summary-standard.md").read_text(encoding="utf-8")
        summary_exec = (run_path / "summary-exec.md").read_text(encoding="utf-8")
        start_here = (run_path / "start-here.md").read_text(encoding="utf-8")
        risk_register = (run_path / "risk-register.md").read_text(encoding="utf-8")
        evidence_index = (run_path / "evidence-index.md").read_text(encoding="utf-8")
        analysis = json.loads((run_path / "analysis.json").read_text(encoding="utf-8"))
        deliberation = json.loads((run_path / "deliberation.json").read_text(encoding="utf-8"))
        retention_payload = json.loads((run_path / "retention.json").read_text(encoding="utf-8"))
        approvals_payload = json.loads((run_path / "approvals.json").read_text(encoding="utf-8"))
        record_payload = json.loads(record_path.read_text(encoding="utf-8"))
        governance_assets = record_payload["governanceAssets"]
        workflow_assets = record_payload["workflowAssets"]
        workflow_state = record_payload["workflowState"]
        runtime_assets = record_payload["runtimeAssets"]
        runtime_state = record_payload["runtimeState"]
        assert_true("## Assessment Scope" in summary_short, "Python short summary should include assessment scope.")
        assert_true("Runtime boundary:" in summary_short, "Python short summary should show runtime boundary linkage.")
        assert_true("## What To Read First" in start_here, "Python start-here should include the reading order.")
        assert_true("[Standard summary](summary-standard.md)" in start_here, "Python start-here should link to the standard summary.")
        assert_true("## Next Action" in start_here, "Python start-here should include next action guidance.")
        assert_true("## Continue Or Resume" in start_here, "Python start-here should include continue or resume guidance.")
        assert_true("Proceed allowed: `No`" in start_here, "Python start-here should block progression while confirmation is pending.")
        assert_true("Confirmation reason: A Warn decision should be explicitly accepted or mitigated before proceeding." in start_here, "Python start-here should show the initial confirmation reason.")
        assert_true("Resume guidance: Resume from `Assess` when the next action items are complete." in start_here, "Python start-here should show the initial resume guidance.")
        assert_true("## Run Status" in summary_short, "Python short summary should include run status.")
        assert_true("## Approval Posture" in summary_short, "Python short summary should include approval posture.")
        assert_true("## Next Action" in summary_short, "Python short summary should include next action.")
        assert_true("## Continue Or Resume" in summary_short, "Python short summary should include continue or resume guidance.")
        assert_true("## Assessment Scope And Decision Window" in summary_standard, "Python standard summary should include scope and decision window.")
        assert_true("## Run Status" in summary_standard, "Python standard summary should include run status.")
        assert_true("## Approval Posture" in summary_standard, "Python standard summary should include approval posture.")
        assert_true("## Next Action" in summary_standard, "Python standard summary should include next action.")
        assert_true("## Continue Or Resume" in summary_standard, "Python standard summary should include continue or resume guidance.")
        assert_true("## Decision Owner And Required Action" in summary_standard, "Python standard summary should include decision owner.")
        assert_true("## Decision Required" in summary_exec, "Python exec summary should include decision required.")
        assert_true("## Proceed Conditions" in summary_exec, "Python exec summary should include proceed conditions.")
        assert_true("Active runtime factsheet:" in summary_exec, "Python exec summary should show runtime factsheet linkage.")
        assert_true("## Next Action" in summary_exec, "Python exec summary should include next action.")
        assert_true("## Continue Or Resume" in summary_exec, "Python exec summary should include continue or resume guidance.")
        assert_true("Governed by:" in summary_standard, "Python standard summary should show governed asset linkage.")
        assert_true("Governed template:" in summary_standard, "Python standard summary should show governed template linkage.")
        assert_true("Workflow lifecycle:" in summary_standard, "Python standard summary should show workflow linkage.")
        assert_true("Likelihood:" in risk_register, "Python risk register should scaffold likelihood.")
        assert_true("Risk owner:" in risk_register, "Python risk register should scaffold risk ownership.")
        assert_true("Workflow handoff contract:" in risk_register, "Python risk register should show workflow handoff linkage.")
        assert_true("supports finding IDs" in evidence_index, "Python evidence index should scaffold traceability fields.")
        assert_true("decisionContext" in analysis, "Python analysis scaffold should include decision context.")
        assert_true(len(analysis["findings"]) >= 1, "Python analysis scaffold should include finding placeholders.")
        assert_true(deliberation["overrideModel"]["overrideTestSummary"] == "Pending override evaluation.", "Python deliberation scaffold should include override test summary.")
        assert_true(record_payload["pluginVersion"] == "0.4.0", "Python run record should use the current plugin version.")
        assert_true(governance_assets["version"] == "v5a-1", "Python run record should resolve the governed asset version.")
        assert_true(governance_assets["prompt"]["path"].endswith("governance-prompt-core-risk-governance.md"), "Python run record should resolve the governance prompt path.")
        assert_true(any(card["name"] == "Orchestrator" for card in governance_assets["roleCards"]), "Python run record should include the orchestrator role card.")
        assert_true(workflow_assets["version"] == "v5b-1", "Python run record should resolve the governed workflow asset version.")
        assert_true(workflow_assets["lifecycleMap"]["path"].endswith("lifecycle-map-core-release-risk.md"), "Python run record should resolve the lifecycle map path.")
        assert_true(any(item["path"].endswith("stage-definition-intake.md") for item in workflow_assets["stageDefinitions"]), "Python run record should resolve the intake stage definition.")
        assert_true(any(item["path"].endswith("stage-definition-assess.md") for item in workflow_assets["stageDefinitions"]), "Python run record should resolve the assess stage definition.")
        assert_true(workflow_assets["approvalPlaybooks"][0]["path"].endswith("approval-playbook-high-sensitivity-release-decision.md"), "Python run record should resolve the approval playbook.")
        assert_true(workflow_assets["handoffs"][0]["path"].endswith("handoff-summary-assess-to-deliberate.md"), "Python run record should resolve the handoff asset.")
        assert_true(workflow_assets["exceptionRules"][0]["path"].endswith("exception-rule-missing-evidence-reentry.md"), "Python run record should resolve the exception rule asset.")
        assert_true(workflow_state["currentStage"] == "Intake", "Python workflow state should begin at Intake.")
        assert_true(workflow_state["nextStage"] == "Assess", "Python workflow state should point to Assess initially.")
        assert_true(workflow_state["pendingApprovalPlaybook"] == "High-Sensitivity Release Decision Approval Playbook", "Python workflow state should bind the approval playbook name.")
        assert_true(workflow_state["assessEntryStatus"] == "ready", "Python workflow state should begin with assess entry ready.")
        assert_true(workflow_state["assessEntryBlockers"] == [], "Python workflow state should begin with no assess entry blockers.")
        assert_true(workflow_state["deliberateHandoffStatus"] == "pending-assess", "Python workflow state should begin with handoff pending assess.")
        assert_true(workflow_state["handoffBlockers"] == [], "Python workflow state should begin with no handoff blockers.")
        assert_true(workflow_state["gateStatus"] == "confirmation-required", "Python workflow state should begin in confirmation-required gate status.")
        assert_true(workflow_state["allowedNextStage"] is None, "Python workflow state should not allow next-stage progression before confirmation.")
        assert_true(workflow_state["blockedBy"] == ["The current decision posture requires explicit confirmation before proceeding."], "Python workflow state should surface the initial blocker.")
        assert_true(runtime_assets["version"] == "v5c-1", "Python run record should resolve the governed runtime asset version.")
        assert_true(runtime_assets["controlTowerView"]["path"].endswith("control-tower-view-default-release-risk.md"), "Python run record should resolve the control tower view.")
        assert_true(runtime_assets["governedRunFactsheet"]["path"].endswith("governed-run-factsheet-release-risk-synthetic.md"), "Python run record should resolve the governed run factsheet.")
        assert_true(runtime_assets["boundaryPanel"]["path"].endswith("boundary-enforcement-panel-release-risk-synthetic.md"), "Python run record should resolve the boundary panel.")
        assert_true(runtime_state["activePolicyProfile"] == "release-risk-core", "Python runtime state should expose the active policy profile.")
        assert_true(runtime_state["runtimeMode"] == "python-first local runtime", "Python runtime state should expose the runtime mode.")
        assert_true(runtime_state["allowedEvidenceClasses"] == ["designDocs", "releasePlan", "testEvidence", "dependencies", "architectureContext", "implementationContext", "advisoryDelegationUsed"], "Python runtime state should expose the allowed evidence classes.")
        assert_true(runtime_state["boundaryStatus"] == "clean", "Python runtime state should begin with a clean boundary status.")
        assert_true(runtime_state["blockedContextClasses"] == [], "Python runtime state should begin with no blocked context classes.")
        assert_true(runtime_state["carryForwardAllowed"] is True, "Python runtime state should allow carry-forward when no blocked context is present.")
        assert_true(runtime_state["transformationStatus"] == "transformed", "Python runtime state should begin with transformed status when no context transformation is needed.")
        assert_true(runtime_state["carryForwardLedger"] == [], "Python runtime state should begin with an empty carry-forward ledger.")
        assert_true(len(runtime_state["trustedInstructionSources"]) == 3, "Python runtime state should surface the trusted instruction sources.")
        assert_true(runtime_state["traceStatus"] == "initialized", "Python runtime state should begin as initialized.")
        assert_true(runtime_state["confirmationRequired"] is True, "Python runtime state should require confirmation for a Warn run.")
        assert_true(runtime_state["confirmationReason"] == "A Warn decision should be explicitly accepted or mitigated before proceeding.", "Python runtime state should expose the initial confirmation reason.")
        assert_true(runtime_state["resumeGuidance"] == "Resume from `Assess` when the next action items are complete.", "Python runtime state should expose the initial resume guidance.")
        assert_true(runtime_state["proceedAllowed"] is False, "Python runtime state should block progression while confirmation is pending.")
        assert_true(runtime_state["proceedBlockers"] == ["The current decision posture requires explicit confirmation before proceeding."], "Python runtime state should expose the initial proceed blocker.")
        assert_true(record_payload["status"] == "initialized", "Python run record should begin in initialized status.")
        assert_true(approvals_payload["playbook"]["path"].endswith("approval-playbook-high-sensitivity-release-decision.md"), "Python approvals scaffold should carry the governed playbook.")
        assert_true(approvals_payload["runtimeBoundary"]["path"].endswith("boundary-enforcement-panel-release-risk-synthetic.md"), "Python approvals scaffold should carry the runtime boundary panel.")
        assert_true(approvals_payload["recommendation"] == "Warn", "Python approvals scaffold should mirror the decision recommendation.")
        assert_true(approvals_payload["approvalRecommendation"] == "stay-conservative", "Python approvals scaffold should expose the approval recommendation separately.")
        assert_true(approvals_payload["approvalStatus"] == "pending-review", "Python approvals scaffold should begin in pending review.")
        assert_true(approvals_payload["currentAction"] == "confirm-or-mitigate", "Python approvals scaffold should surface the initial current action.")
        assert_true(approvals_payload["resumeGuidance"] == "Resume from `Assess` when the next action items are complete.", "Python approvals scaffold should surface the initial resume guidance.")
        assert_true(approvals_payload["proceedAllowed"] is False, "Python approvals scaffold should mirror blocked progression.")
        assert_true(approvals_payload["proceedBlockers"] == ["The current decision posture requires explicit confirmation before proceeding."], "Python approvals scaffold should mirror the initial proceed blocker.")
        assert_true(approvals_payload["boundaryStatus"] == "clean", "Python approvals scaffold should mirror the initial clean boundary status.")
        assert_true(approvals_payload["blockedContextClasses"] == [], "Python approvals scaffold should mirror the initial blocked context classes.")
        assert_true(approvals_payload["carryForwardAllowed"] is True, "Python approvals scaffold should mirror that carry-forward is initially allowed.")
        assert_true(approvals_payload["transformationStatus"] == "transformed", "Python approvals scaffold should mirror the initial transformation status.")
        assert_true(approvals_payload["carryForwardLedger"] == [], "Python approvals scaffold should mirror the initial empty carry-forward ledger.")
        assert_true(approvals_payload["playbookGateStatus"] == "confirmation-required", "Python approvals scaffold should mirror the initial gate status.")
        assert_true(approvals_payload["allowedNextStage"] is None, "Python approvals scaffold should block next-stage progression before confirmation.")
        assert_true(retention_payload["contextContract"]["path"].endswith("context-contract-release-risk-synthetic.md"), "Python retention scaffold should carry the context contract.")
        tests_run += 1

        code, output = run_script("New-PreMortemXRun.py", "--ProjectSlug", "py-sample-arch", "--Mode", "architecture-validation", "--Decision", "Warn")
        assert_true(code == 0, f"Python architecture run initialization should succeed.\n{output}")
        arch_created = json.loads(output)
        arch_run_path = Path(arch_created["RunPath"])
        arch_record_path = Path(arch_created["RecordPath"])
        arch_record = json.loads(arch_record_path.read_text(encoding="utf-8"))
        arch_summary = (arch_run_path / "summary-standard.md").read_text(encoding="utf-8")
        assert_true(arch_record["mode"] == "architecture-validation", "Python architecture mode should be recorded.")
        assert_true(arch_record["taskType"] == "architecture-review", "Python architecture task type should be recorded.")
        assert_true(arch_record["taskCategory"] == "risk-analysis", "Python architecture task category should default to risk-analysis.")
        assert_true("PreMortemX Architecture Assessment" in arch_summary, "Python architecture summary title should be used.")
        tests_run += 1

        code, output = run_script("Test-PreMortemXRunRecord.py", "--RunRecordPath", str(record_path))
        assert_true(code == 0, f"Python run-record validation should succeed.\n{output}")
        tests_run += 1

        code, output = run_script("Test-PreMortemXRunRecord.py", "--RunRecordPath", str(arch_record_path))
        assert_true(code == 0, f"Python architecture run-record validation should succeed.\n{output}")
        tests_run += 1

        specialist_input = run_path / "specialists-test.json"
        specialist_input.write_text(
            json.dumps(
                {
                    "specialists": [
                        {
                            "role": "Domain Risk Specialist",
                            "recommendation": "Warn",
                            "summary": "The delivery shape is fragile.",
                            "evidenceRefs": ["design/spec.md"],
                            "rubric": {
                                "confidence": 2,
                                "evidenceStrength": 2,
                                "riskSeverity": 3,
                                "evidenceCompleteness": 2,
                                "disagreementLevel": 4,
                                "policyFit": 3,
                                "decisionSensitivity": 3,
                            },
                        },
                        {
                            "role": "Operational/Release Risk Specialist",
                            "recommendation": "Pass",
                            "summary": "Operational controls look manageable.",
                            "evidenceRefs": ["ops/checklist.md"],
                            "rubric": {
                                "confidence": 2,
                                "evidenceStrength": 2,
                                "riskSeverity": 2,
                                "evidenceCompleteness": 2,
                                "disagreementLevel": 4,
                                "policyFit": 3,
                                "decisionSensitivity": 4,
                            },
                        },
                        {
                            "role": "Security/Privacy Risk Specialist",
                            "recommendation": "Block",
                            "summary": "Sensitive path lacks enough evidence controls.",
                            "evidenceRefs": ["security/review.md"],
                            "rubric": {
                                "confidence": 4,
                                "evidenceStrength": 5,
                                "riskSeverity": 5,
                                "evidenceCompleteness": 4,
                                "disagreementLevel": 4,
                                "policyFit": 2,
                                "decisionSensitivity": 5,
                            },
                        },
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        code, output = run_script(
            "Invoke-PreMortemXDeliberation.py",
            "--RunRecordPath",
            str(record_path),
            "--SpecialistInputPath",
            str(specialist_input),
        )
        assert_true(code == 0, f"Python deliberation should succeed.\n{output}")
        payload = json.loads(output)
        record = json.loads(record_path.read_text(encoding="utf-8"))
        approvals_after_deliberation = json.loads((run_path / "approvals.json").read_text(encoding="utf-8"))
        retention_after_deliberation = json.loads((run_path / "retention.json").read_text(encoding="utf-8"))
        summary_short_after = (run_path / "summary-short.md").read_text(encoding="utf-8")
        summary_standard_after = (run_path / "summary-standard.md").read_text(encoding="utf-8")
        summary_exec_after = (run_path / "summary-exec.md").read_text(encoding="utf-8")
        start_here_after = (run_path / "start-here.md").read_text(encoding="utf-8")
        assert_true(payload["finalDecision"] == "Block", "Python deliberation should escalate to Block.")
        assert_true(record["status"] == "adjudicated", "Python run record should move to adjudicated status after deliberation.")
        assert_true(record["deliberation"]["status"] == "completed", "Python deliberation status should be completed.")
        assert_true(record["deliberation"]["overrideModel"]["overrideApplied"] is True, "Python override model should record an override.")
        assert_true(record["deliberation"]["overrideModel"]["humanEscalationRequired"] is True, "Python override model should require human escalation.")
        assert_true(record["deliberation"]["adjudication"]["ruleTriggered"] == "severity-and-policy", "Python deliberation should record rule trigger.")
        assert_true(len(record["deliberation"]["adjudication"]["decisionPath"]) >= 1, "Python deliberation should record decision path.")
        assert_true(record["deliberation"]["adjudication"]["humanEscalationConsidered"] is not None, "Python deliberation should record whether human escalation was considered.")
        assert_true(record["workflowState"]["currentStage"] == "Approve/Block", "Python workflow state should advance to Approve/Block after deliberation.")
        assert_true(record["workflowState"]["nextStage"] == "Revisit", "Python workflow state should point to Revisit after a Block.")
        assert_true(record["workflowState"]["activeExceptionRule"] == "Missing Evidence Re-entry Rule", "Python workflow state should activate the missing-evidence rule when completeness degrades.")
        assert_true(record["workflowState"]["assessEntryStatus"] == "ready", "Python workflow state should preserve assess entry readiness when intake remains valid.")
        assert_true(record["workflowState"]["assessEntryBlockers"] == [], "Python workflow state should preserve no assess entry blockers when intake remains valid.")
        assert_true(record["workflowState"]["deliberateHandoffStatus"] == "ready", "Python workflow state should mark the deliberate handoff as ready when outputs exist.")
        assert_true(record["workflowState"]["handoffBlockers"] == [], "Python workflow state should keep handoff blockers empty when outputs exist.")
        assert_true(record["workflowState"]["gateStatus"] == "awaiting-human-escalation", "Python workflow state should require human escalation after the Block case.")
        assert_true(record["workflowState"]["allowedNextStage"] is None, "Python workflow state should block progression after the Block case.")
        assert_true(record["workflowState"]["blockedBy"] == ["An active exception rule must be resolved before proceeding.", "Human escalation is required before proceeding."], "Python workflow state should mirror the Block-case blockers.")
        assert_true("Deliberate" in record["workflowState"]["completedStages"], "Python workflow state should record completed stages.")
        assert_true(approvals_after_deliberation["workflowState"]["currentStage"] == "Approve/Block", "Python approvals artifact should mirror the advanced workflow state.")
        assert_true(record["runtimeState"]["traceStatus"] == "completed", "Python runtime state should mark the trace as completed after deliberation.")
        assert_true(record["runtimeState"]["boundaryStatus"] == "clean", "Python runtime state should remain clean when no blocked context is present.")
        assert_true(record["runtimeState"]["blockedContextClasses"] == [], "Python runtime state should keep blocked context classes empty when no boundary issue is present.")
        assert_true(record["runtimeState"]["carryForwardAllowed"] is True, "Python runtime state should keep carry-forward allowed when no boundary issue is present.")
        assert_true(record["runtimeState"]["transformationStatus"] == "transformed", "Python runtime state should mark transformation status as transformed when only promoted context remains.")
        assert_true(isinstance(record["runtimeState"]["carryForwardLedger"], list), "Python runtime state should expose the carry-forward ledger after deliberation.")
        assert_true(record["runtimeState"]["confirmationRequired"] is True, "Python runtime state should still require confirmation after a Block decision.")
        assert_true(record["runtimeState"]["confirmationReason"] == "Human escalation is required before the workflow can proceed.", "Python runtime state should refresh the post-deliberation confirmation reason.")
        assert_true(record["runtimeState"]["resumeGuidance"] == "Resume from `Revisit` after resolving the active exception rule.", "Python runtime state should refresh the post-deliberation resume guidance.")
        assert_true(record["runtimeState"]["proceedAllowed"] is False, "Python runtime state should continue to block progression after a Block decision.")
        assert_true(record["runtimeState"]["proceedBlockers"] == ["An active exception rule must be resolved before proceeding.", "Human escalation is required before proceeding."], "Python runtime state should expose the active blockers after deliberation.")
        assert_true(len(record["runtimeState"]["openBreaches"]) >= 1, "Python runtime state should record a visible breach when completeness degrades.")
        assert_true(any("Escalate the blocked decision" in item for item in record["runtimeState"]["attentionItems"]), "Python runtime state should surface operator attention for a blocked decision.")
        assert_true(approvals_after_deliberation["runtimeBoundary"]["path"].endswith("boundary-enforcement-panel-release-risk-synthetic.md"), "Python approvals artifact should preserve runtime boundary linkage after deliberation.")
        assert_true(approvals_after_deliberation["recommendation"] == "Block", "Python approvals artifact should mirror the final decision recommendation after deliberation.")
        assert_true(approvals_after_deliberation["approvalRecommendation"] == "human-escalation-required", "Python approvals artifact should expose the approval recommendation after deliberation.")
        assert_true(approvals_after_deliberation["approvalStatus"] == "awaiting-human-escalation", "Python approvals artifact should require human escalation after deliberation.")
        assert_true(approvals_after_deliberation["currentAction"] == "escalate-before-revisit", "Python approvals artifact should refresh the current action after deliberation.")
        assert_true(approvals_after_deliberation["resumeGuidance"] == "Resume from `Revisit` after resolving the active exception rule.", "Python approvals artifact should refresh the resume guidance after deliberation.")
        assert_true(approvals_after_deliberation["proceedAllowed"] is False, "Python approvals artifact should keep progression blocked after deliberation.")
        assert_true(approvals_after_deliberation["proceedBlockers"] == ["An active exception rule must be resolved before proceeding.", "Human escalation is required before proceeding."], "Python approvals artifact should mirror the active blockers after deliberation.")
        assert_true(approvals_after_deliberation["boundaryStatus"] == "clean", "Python approvals artifact should preserve the clean boundary status when no blocked context is present.")
        assert_true(approvals_after_deliberation["blockedContextClasses"] == [], "Python approvals artifact should preserve empty blocked context classes when no boundary issue is present.")
        assert_true(approvals_after_deliberation["carryForwardAllowed"] is True, "Python approvals artifact should preserve carry-forward allowed when no boundary issue is present.")
        assert_true(approvals_after_deliberation["transformationStatus"] == "transformed", "Python approvals artifact should preserve the transformed status when no boundary issue is present.")
        assert_true(isinstance(approvals_after_deliberation["carryForwardLedger"], list), "Python approvals artifact should preserve the carry-forward ledger when no boundary issue is present.")
        assert_true(approvals_after_deliberation["playbookGateStatus"] == "awaiting-human-escalation", "Python approvals artifact should mirror the Block-case gate status after deliberation.")
        assert_true(approvals_after_deliberation["allowedNextStage"] is None, "Python approvals artifact should keep next-stage progression blocked after deliberation.")
        assert_true(retention_after_deliberation["contextContract"]["path"].endswith("context-contract-release-risk-synthetic.md"), "Python retention artifact should preserve context contract linkage.")
        assert_true("Current stage: `Approve/Block`" in summary_short_after, "Python short summary should refresh with the advanced workflow stage.")
        assert_true("Trace status: `completed`" in summary_short_after, "Python short summary should refresh with completed trace status.")
        assert_true("Proceed allowed: `No`" in summary_short_after, "Python short summary should keep progression blocked after deliberation.")
        assert_true("Confirmation reason: Human escalation is required before the workflow can proceed." in summary_short_after, "Python short summary should refresh the confirmation reason after deliberation.")
        assert_true("Resume guidance: Resume from `Revisit` after resolving the active exception rule." in summary_short_after, "Python short summary should refresh the resume guidance after deliberation.")
        assert_true("Blocker: An active exception rule must be resolved before proceeding." in summary_short_after, "Python short summary should show the active exception blocker.")
        assert_true("Human escalation required: `Yes`" in summary_standard_after, "Python standard summary should refresh with escalation posture.")
        assert_true("Next action summary: Escalate the current decision before the run can return for revisit." in summary_standard_after, "Python standard summary should refresh the next action guidance.")
        assert_true("Confirmation reason: Human escalation is required before the workflow can proceed." in summary_standard_after, "Python standard summary should refresh the confirmation reason after deliberation.")
        assert_true("Resume guidance: Resume from `Revisit` after resolving the active exception rule." in summary_standard_after, "Python standard summary should refresh the resume guidance after deliberation.")
        assert_true("Next action summary: Escalate the current decision before the run can return for revisit." in summary_exec_after, "Python exec summary should refresh the next action guidance.")
        assert_true("Confirmation reason: Human escalation is required before the workflow can proceed." in summary_exec_after, "Python exec summary should refresh the confirmation reason after deliberation.")
        assert_true("Current stage: `Approve/Block`" in start_here_after, "Python start-here should refresh the current stage after deliberation.")
        assert_true("Human escalation required: `Yes`" in start_here_after, "Python start-here should refresh the escalation posture after deliberation.")
        assert_true("Proceed allowed: `No`" in start_here_after, "Python start-here should keep progression blocked after deliberation.")
        assert_true("Confirmation reason: Human escalation is required before the workflow can proceed." in start_here_after, "Python start-here should refresh the confirmation reason after deliberation.")
        assert_true("Resume guidance: Resume from `Revisit` after resolving the active exception rule." in start_here_after, "Python start-here should refresh the resume guidance after deliberation.")
        tests_run += 1

        execute_workflow_case(
            "matrix-pass-clean",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "Core design risks are well controlled.", "design/pass.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational rollout looks contained.", "ops/pass.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security review did not surface release blockers.", "security/pass.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="ready",
            expected_approval_status="approved-for-monitor",
            expected_current_action="continue-to-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage="Monitor",
            expected_proceed_allowed=True,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=[],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-pass-low-evidence",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "Delivery shape looks acceptable.", "design/low-evidence.md", confidence=3, evidence_strength=3, risk_severity=2, evidence_completeness=2, disagreement_level=1, policy_fit=4, decision_sensitivity=3),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational checks are incomplete but not alarming.", "ops/low-evidence.md", confidence=3, evidence_strength=3, risk_severity=2, evidence_completeness=3, disagreement_level=1, policy_fit=4, decision_sensitivity=3),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security evidence remains partial.", "security/low-evidence.md", confidence=3, evidence_strength=3, risk_severity=2, evidence_completeness=3, disagreement_level=1, policy_fit=4, decision_sensitivity=3),
            ],
            expected_decision="Warn",
            expected_rule_triggered="evidence-gated",
            expected_gate_status="exception-blocked",
            expected_approval_status="revisit-required",
            expected_current_action="resolve-exception-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule="Missing Evidence Re-entry Rule",
            expected_blockers=["An active exception rule must be resolved before proceeding.", "The current decision posture requires explicit confirmation before proceeding."],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-pass-low-policy-fit",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "Primary design appears sound.", "design/low-policy.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=2, decision_sensitivity=3),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational checks mostly pass.", "ops/low-policy.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=3, decision_sensitivity=3),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security fit remains slightly below policy comfort.", "security/low-policy.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=3, decision_sensitivity=3),
            ],
            expected_decision="Warn",
            expected_rule_triggered="severity-and-policy",
            expected_gate_status="confirmation-required",
            expected_approval_status="pending-confirmation",
            expected_current_action="confirm-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["The current decision posture requires explicit confirmation before proceeding."],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-minority-block-override",
            "Warn",
            [
                build_specialist("Domain Risk Specialist", "Warn", "The delivery path has manageable fragility.", "design/minority-override.md", confidence=3, evidence_strength=2, risk_severity=3, evidence_completeness=4, disagreement_level=3, policy_fit=3, decision_sensitivity=3),
                build_specialist("Operational/Release Risk Specialist", "Warn", "Operational posture remains guarded but workable.", "ops/minority-override.md", confidence=3, evidence_strength=2, risk_severity=3, evidence_completeness=4, disagreement_level=3, policy_fit=3, decision_sensitivity=3),
                build_specialist("Security/Privacy Risk Specialist", "Block", "Minority evidence shows a materially stronger blocker.", "security/minority-override.md", confidence=4, evidence_strength=5, risk_severity=3, evidence_completeness=4, disagreement_level=3, policy_fit=3, decision_sensitivity=3),
            ],
            expected_decision="Block",
            expected_rule_triggered="evidence-gated",
            expected_gate_status="confirmation-required",
            expected_approval_status="pending-confirmation",
            expected_current_action="reverse-or-escalate",
            expected_next_stage="Revisit",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["The current decision posture requires explicit confirmation before proceeding."],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-pass-unresolved-permissions",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "Design checks are clean.", "design/permissions.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational readiness is strong.", "ops/permissions.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security review is satisfied.", "security/permissions.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="awaiting-human-escalation",
            expected_approval_status="awaiting-human-escalation",
            expected_current_action="escalate-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=True,
            expected_active_exception_rule=None,
            expected_blockers=["Human escalation is required before proceeding.", "Requested permission broadening remains unresolved."],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            permission_requests=[{"scope": "repo-write", "reason": "Need broader write access for release automation."}],
            permission_approvals=[],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-blocked-unvalidated-context",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "The core design appears acceptable.", "design/context-block.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational signals remain manageable.", "ops/context-block.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture would be acceptable absent the context problem.", "security/context-block.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="blocked-context",
            expected_approval_status="boundary-remediation-required",
            expected_current_action="resolve-boundary-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["Blocked or excluded context must be removed or explicitly governed before proceeding."],
            expected_boundary_status="blocked-context",
            expected_blocked_context_classes=["unvalidated-assertion", "ambient-context"],
            expected_carry_forward_allowed=False,
            expected_transformation_status="blocked",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            constraints=["UNVALIDATED_ASSERTION:user-supplied risk claim", "AMBIENT_CONTEXT:general workspace chatter"],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-blocked-advisory-carry-forward",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "The design itself looks clean.", "design/advisory-block.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational readiness remains sound.", "ops/advisory-block.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security signals are acceptable apart from provenance.", "security/advisory-block.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="blocked-context",
            expected_approval_status="boundary-remediation-required",
            expected_current_action="resolve-boundary-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["Blocked or excluded context must be removed or explicitly governed before proceeding."],
            expected_boundary_status="blocked-context",
            expected_blocked_context_classes=["prior-case-carry-forward", "unlinked-advisory-context"],
            expected_carry_forward_allowed=False,
            expected_transformation_status="blocked",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            architecture_context=["PRIOR_CASE:legacy release postmortem excerpt"],
            advisory_used=[{"advisor": "external-critique", "summary": "Advisory note without linked artifact"}],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-blocked-untransformed-context",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "The design itself is acceptable.", "design/untransformed.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational readiness is otherwise acceptable.", "ops/untransformed.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable absent transformation issues.", "security/untransformed.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="blocked-context",
            expected_approval_status="boundary-remediation-required",
            expected_current_action="resolve-boundary-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["Untransformed context must be converted into governed evidence references before proceeding."],
            expected_boundary_status="blocked-context",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=False,
            expected_transformation_status="blocked",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            implementation_context=["raw implementation note without governed prefix"],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-quarantined-advisory-context",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "The design checks are acceptable.", "design/quarantined.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational readiness remains acceptable.", "ops/quarantined.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable but advisory provenance is still unresolved.", "security/quarantined.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="quarantined-context",
            expected_approval_status="boundary-remediation-required",
            expected_current_action="resolve-boundary-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["Quarantined context must be promoted or discarded before proceeding."],
            expected_boundary_status="quarantined-context",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=False,
            expected_transformation_status="quarantined",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            advisory_used=[{"advisor": "external-critique", "summary": "Linked advisory note", "linkedArtifact": "advisory/report.md"}],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-combined-workflow-and-boundary-blockers",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "The design itself is acceptable.", "design/combined-blockers.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational posture is acceptable if prerequisites are met.", "ops/combined-blockers.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable absent the blocked context.", "security/combined-blockers.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="workflow-blocked",
            expected_approval_status="workflow-remediation-required",
            expected_current_action="fix-intake-before-assess",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=[
                "Assess entry criteria are not met: bounded scope is missing.",
                "Blocked or excluded context must be removed or explicitly governed before proceeding.",
            ],
            expected_boundary_status="blocked-context",
            expected_blocked_context_classes=["unvalidated-assertion"],
            expected_carry_forward_allowed=False,
            expected_transformation_status="blocked",
            expected_assess_entry_status="blocked",
            expected_assess_entry_blockers=["Assess entry criteria are not met: bounded scope is missing."],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            constraints=["MISSING_TARGET_SCOPE", "UNVALIDATED_ASSERTION:ungoverned claim"],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-workflow-missing-evidence-bundle",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "Design itself looks acceptable.", "design/missing-evidence.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational posture is otherwise clean.", "ops/missing-evidence.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security signals would be acceptable if intake were complete.", "security/missing-evidence.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="workflow-blocked",
            expected_approval_status="workflow-remediation-required",
            expected_current_action="fix-intake-before-assess",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["Assess entry criteria are not met: evidence bundle is not named."],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="blocked",
            expected_assess_entry_blockers=["Assess entry criteria are not met: evidence bundle is not named."],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            constraints=["MISSING_EVIDENCE_BUNDLE"],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-workflow-missing-intake-pair",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "Design itself looks acceptable.", "design/missing-intake-pair.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational posture is otherwise clean.", "ops/missing-intake-pair.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture remains acceptable if intake is fixed.", "security/missing-intake-pair.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="workflow-blocked",
            expected_approval_status="workflow-remediation-required",
            expected_current_action="fix-intake-before-assess",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=[
                "Assess entry criteria are not met: bounded scope is missing.",
                "Assess entry criteria are not met: evidence bundle is not named.",
            ],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="blocked",
            expected_assess_entry_blockers=[
                "Assess entry criteria are not met: bounded scope is missing.",
                "Assess entry criteria are not met: evidence bundle is not named.",
            ],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            constraints=["MISSING_TARGET_SCOPE", "MISSING_EVIDENCE_BUNDLE"],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-workflow-missing-handoff",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "The assessed risk picture would normally be acceptable.", "design/missing-handoff.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational checks remain acceptable.", "ops/missing-handoff.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture remains acceptable.", "security/missing-handoff.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="workflow-blocked",
            expected_approval_status="workflow-remediation-required",
            expected_current_action="complete-handoff-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=["Assess-to-deliberate handoff is incomplete: handoff summary is missing."],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="blocked",
            expected_handoff_blockers=["Assess-to-deliberate handoff is incomplete: handoff summary is missing."],
            constraints=["MISSING_HANDOFF_SUMMARY"],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-workflow-missing-handoff-pair",
            "Pass",
            [
                build_specialist("Domain Risk Specialist", "Pass", "The assessed risk picture would normally be acceptable.", "design/missing-handoff-pair.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Operational/Release Risk Specialist", "Pass", "Operational checks remain acceptable.", "ops/missing-handoff-pair.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture remains acceptable.", "security/missing-handoff-pair.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
            ],
            expected_decision="Pass",
            expected_rule_triggered="consensus",
            expected_gate_status="workflow-blocked",
            expected_approval_status="workflow-remediation-required",
            expected_current_action="complete-handoff-before-monitor",
            expected_next_stage="Monitor",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=[
                "Assess-to-deliberate handoff is incomplete: handoff summary is missing.",
                "Assess-to-deliberate handoff is incomplete: structured risk picture is missing.",
            ],
            expected_boundary_status="clean",
            expected_blocked_context_classes=[],
            expected_carry_forward_allowed=True,
            expected_transformation_status="transformed",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="blocked",
            expected_handoff_blockers=[
                "Assess-to-deliberate handoff is incomplete: handoff summary is missing.",
                "Assess-to-deliberate handoff is incomplete: structured risk picture is missing.",
            ],
            constraints=["MISSING_HANDOFF_SUMMARY", "MISSING_RISK_PICTURE"],
        )
        tests_run += 1

        execute_workflow_case(
            "matrix-boundary-block-on-block-path",
            "Block",
            [
                build_specialist("Domain Risk Specialist", "Block", "The design remains blocked.", "design/boundary-revisit.md", confidence=4, evidence_strength=4, risk_severity=4, evidence_completeness=4, disagreement_level=1, policy_fit=3, decision_sensitivity=4),
                build_specialist("Operational/Release Risk Specialist", "Block", "Operational posture does not support release.", "ops/boundary-revisit.md", confidence=4, evidence_strength=4, risk_severity=4, evidence_completeness=4, disagreement_level=1, policy_fit=3, decision_sensitivity=4),
                build_specialist("Security/Privacy Risk Specialist", "Block", "Security posture remains blocked and context is also invalid.", "security/boundary-revisit.md", confidence=4, evidence_strength=4, risk_severity=4, evidence_completeness=4, disagreement_level=1, policy_fit=3, decision_sensitivity=4),
            ],
            expected_decision="Block",
            expected_rule_triggered="severity-and-policy",
            expected_gate_status="blocked-context",
            expected_approval_status="boundary-remediation-required",
            expected_current_action="resolve-boundary-before-revisit",
            expected_next_stage="Revisit",
            expected_allowed_next_stage=None,
            expected_proceed_allowed=False,
            expected_human_escalation=False,
            expected_active_exception_rule=None,
            expected_blockers=[
                "Blocked or excluded context must be removed or explicitly governed before proceeding.",
                "The current decision posture requires explicit confirmation before proceeding.",
            ],
            expected_boundary_status="blocked-context",
            expected_blocked_context_classes=["ambient-context"],
            expected_carry_forward_allowed=False,
            expected_transformation_status="blocked",
            expected_assess_entry_status="ready",
            expected_assess_entry_blockers=[],
            expected_deliberate_handoff_status="ready",
            expected_handoff_blockers=[],
            constraints=["AMBIENT_CONTEXT:operator note without governance link"],
        )
        tests_run += 1

        code, output = run_script("New-PreMortemXRun.py", "--ProjectSlug", "matrix-remediation-transition", "--Decision", "Pass")
        assert_true(code == 0, f"Remediation transition case should initialize successfully.\n{output}")
        remediation_created = json.loads(output)
        remediation_run_path = Path(remediation_created["RunPath"])
        remediation_record_path = Path(remediation_created["RecordPath"])
        try:
            remediation_record = json.loads(remediation_record_path.read_text(encoding="utf-8"))
            remediation_record["inspectedInputs"]["constraints"] = ["UNVALIDATED_ASSERTION:transient blocked context"]
            remediation_record_path.write_text(json.dumps(remediation_record, indent=2), encoding="utf-8")
            remediation_specialist_input = remediation_run_path / "specialists-remediation.json"
            remediation_specialist_input.write_text(
                json.dumps(
                    {
                        "specialists": [
                            build_specialist("Domain Risk Specialist", "Pass", "The design remains acceptable.", "design/remediation.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                            build_specialist("Operational/Release Risk Specialist", "Pass", "Operational posture remains acceptable.", "ops/remediation.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable once the context issue is removed.", "security/remediation.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                        ]
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            code, output = run_script("Invoke-PreMortemXDeliberation.py", "--RunRecordPath", str(remediation_record_path), "--SpecialistInputPath", str(remediation_specialist_input))
            assert_true(code == 0, f"Remediation transition first deliberation should succeed.\n{output}")
            remediation_blocked = json.loads(remediation_record_path.read_text(encoding="utf-8"))
            assert_true(remediation_blocked["workflowState"]["gateStatus"] == "blocked-context", "Remediation transition should begin in blocked-context state.")
            remediation_blocked["inspectedInputs"]["constraints"] = []
            remediation_record_path.write_text(json.dumps(remediation_blocked, indent=2), encoding="utf-8")
            code, output = run_script("Invoke-PreMortemXDeliberation.py", "--RunRecordPath", str(remediation_record_path), "--SpecialistInputPath", str(remediation_specialist_input))
            assert_true(code == 0, f"Remediation transition second deliberation should succeed.\n{output}")
            remediation_clean = json.loads(remediation_record_path.read_text(encoding="utf-8"))
            remediation_approvals = json.loads((remediation_run_path / "approvals.json").read_text(encoding="utf-8"))
            assert_true(remediation_clean["workflowState"]["gateStatus"] == "ready", "Remediation transition should become ready after the blocked context is removed.")
            assert_true(remediation_clean["runtimeState"]["boundaryStatus"] == "clean", "Remediation transition should clear boundary status after remediation.")
            assert_true(remediation_clean["runtimeState"]["proceedBlockers"] == [], "Remediation transition should clear proceed blockers after remediation.")
            assert_true(remediation_approvals["approvalStatus"] == "approved-for-monitor", "Remediation transition approvals should move to approved-for-monitor after remediation.")
        finally:
            if remediation_run_path.exists():
                shutil.rmtree(remediation_run_path)
        tests_run += 1

        code, output = run_script("New-PreMortemXRun.py", "--ProjectSlug", "matrix-leakage-redaction", "--Decision", "Pass")
        assert_true(code == 0, f"Leakage redaction case should initialize successfully.\n{output}")
        leakage_created = json.loads(output)
        leakage_run_path = Path(leakage_created["RunPath"])
        leakage_record_path = Path(leakage_created["RecordPath"])
        try:
            leakage_record = json.loads(leakage_record_path.read_text(encoding="utf-8"))
            leakage_record["inspectedInputs"]["constraints"] = ["UNVALIDATED_ASSERTION:do-not-leak-this-text"]
            leakage_record["inspectedInputs"]["architectureContext"] = ["PRIOR_CASE:do-not-leak-prior-case"]
            leakage_record["executionBoundary"]["advisoryDelegationUsed"] = [{"advisor": "external", "summary": "raw-advisory-secret"}]
            leakage_record_path.write_text(json.dumps(leakage_record, indent=2), encoding="utf-8")
            leakage_specialist_input = leakage_run_path / "specialists-leakage.json"
            leakage_specialist_input.write_text(
                json.dumps(
                    {
                        "specialists": [
                            build_specialist("Domain Risk Specialist", "Pass", "Design is acceptable apart from the blocked context.", "design/leakage.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                            build_specialist("Operational/Release Risk Specialist", "Pass", "Operational posture is acceptable apart from provenance.", "ops/leakage.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                            build_specialist("Security/Privacy Risk Specialist", "Pass", "Security posture is acceptable absent the blocked context.", "security/leakage.md", confidence=4, evidence_strength=4, risk_severity=2, evidence_completeness=4, disagreement_level=1, policy_fit=4, decision_sensitivity=2),
                        ]
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            code, output = run_script("Invoke-PreMortemXDeliberation.py", "--RunRecordPath", str(leakage_record_path), "--SpecialistInputPath", str(leakage_specialist_input))
            assert_true(code == 0, f"Leakage redaction deliberation should succeed.\n{output}")
            leakage_approvals = json.loads((leakage_run_path / "approvals.json").read_text(encoding="utf-8"))
            leakage_start_here = (leakage_run_path / "start-here.md").read_text(encoding="utf-8")
            leakage_summary = (leakage_run_path / "summary-standard.md").read_text(encoding="utf-8")
            approvals_text = json.dumps(leakage_approvals)
            for forbidden in ["do-not-leak-this-text", "do-not-leak-prior-case", "raw-advisory-secret"]:
                assert_true(forbidden not in approvals_text, f"Leakage redaction approvals should not expose `{forbidden}`.")
                assert_true(forbidden not in leakage_start_here, f"Leakage redaction start-here should not expose `{forbidden}`.")
                assert_true(forbidden not in leakage_summary, f"Leakage redaction summary should not expose `{forbidden}`.")
        finally:
            if leakage_run_path.exists():
                shutil.rmtree(leakage_run_path)
        tests_run += 1

        code, output = run_script("Update-PreMortemXRegistry.py", "--RunRecordPath", str(record_path))
        assert_true(code == 0, f"Python registry update should succeed.\n{output}")
        assert_true(index_path.exists(), "Python registry index should exist.")
        index_content = index_path.read_text(encoding="utf-8")
        assert_true(created["RunId"] in index_content, "Python registry index should contain the run ID.")
        tests_run += 1

        code, output = run_script("Update-PreMortemXRegistry.py", "--RunRecordPath", str(arch_record_path))
        assert_true(code == 0, f"Python architecture registry update should succeed.\n{output}")
        index_content = index_path.read_text(encoding="utf-8")
        assert_true("risk-analysis" in index_content, "Python registry index should contain task category.")
        tests_run += 1

        code, output = run_script("Get-PreMortemXRegistrySummary.py")
        assert_true(code == 0, f"Python registry summary should succeed.\n{output}")
        summary = json.loads(output)
        assert_true(summary["totalRuns"] >= 1, "Python registry summary should report runs.")
        assert_true(summary["byDecision"]["Block"] >= 1, "Python registry summary should count Block decisions.")
        assert_true(summary["pendingQualityFollowup"] >= 1, "Python registry summary should report pending quality follow-up before reviews.")
        tests_run += 1

        code, output = run_script("Build-PreMortemXRegistryViews.py")
        assert_true(code == 0, f"Python registry view build should succeed.\n{output}")
        assert_true((views_root / "dashboard.md").exists(), "Python dashboard should exist.")
        assert_true((views_root / "latest-by-project.json").exists(), "Python latest-by-project view should exist.")
        assert_true((views_root / "attention-queue.json").exists(), "Python attention-queue view should exist.")
        tests_run += 1

        code, output = run_script(
            "Update-PreMortemXQualityReview.py",
            "--RunRecordPath",
            str(record_path),
            "--ReviewOutcome",
            "accurate",
            "--Reviewer",
            "python-evaluator",
            "--OutcomeNotes",
            "Validated-after-python-review.",
        )
        assert_true(code == 0, f"Python quality review update should succeed.\n{output}")
        review = json.loads(output)
        assert_true(review["reviewer"] == "python-evaluator", "Python review should record reviewer.")
        tests_run += 1

        code, output = run_script("Get-PreMortemXGuardrailRecommendations.py", "--ProjectSlug", "py-sample-api")
        assert_true(code == 0, f"Python guardrail recommendations should succeed.\n{output}")
        guardrails = json.loads(output)
        assert_true(guardrails["reviewedRuns"] >= 1, "Python guardrail recommendations should include reviewed runs.")
        tests_run += 1

        code, output = run_script("Get-PreMortemXTrendSummary.py")
        assert_true(code == 0, f"Python trend summary should succeed.\n{output}")
        trend = json.loads(output)
        assert_true(trend["totalReviewed"] >= 1, "Python trend summary should report reviewed items.")
        assert_true(trend["byOutcome"]["accurate"] >= 1, "Python trend summary should count accurate reviews.")
        tests_run += 1

        code, output = run_script("Initialize-PreMortemXCalibrationStore.py", "--DatabasePath", str(CALIBRATION_DB))
        assert_true(code == 0, f"Python calibration init should succeed.\n{output}")
        assert_true(CALIBRATION_DB.exists(), "Python calibration DB should exist.")
        tests_run += 1

        code, output = run_script(
            "Import-PreMortemXReviewedRunToCalibration.py",
            "--RunRecordPath",
            str(record_path),
            "--PromotionState",
            "trusted",
            "--DatasetVersion",
            "v4-seed",
            "--DatabasePath",
            str(CALIBRATION_DB),
        )
        assert_true(code == 0, f"Python reviewed-run import should succeed.\n{output}")
        imported = json.loads(output)
        assert_true(imported["promotionState"] == "trusted", "Python import should set trusted promotion.")
        tests_run += 1

        code, output = run_script("Get-PreMortemXCalibrationSummary.py", "--DatabasePath", str(CALIBRATION_DB))
        assert_true(code == 0, f"Python calibration summary should succeed.\n{output}")
        calibration_summary = json.loads(output)
        assert_true(calibration_summary["totalCases"] >= 1, "Python calibration summary should report cases.")
        assert_true(calibration_summary["byPromotionState"]["trusted"] >= 1, "Python calibration summary should count trusted cases.")
        tests_run += 1

        code, output = run_script(
            "Set-PreMortemXCalibrationPromotionState.py",
            "--CaseId",
            created["RunId"],
            "--PromotionState",
            "provisional",
            "--ChangedBy",
            "python-codex",
            "--Reason",
            "python-state-change",
            "--DatabasePath",
            str(CALIBRATION_DB),
        )
        assert_true(code == 0, f"Python promotion state change should succeed.\n{output}")
        promotion = json.loads(output)
        assert_true(promotion["toState"] == "provisional", "Python promotion should set provisional state.")
        tests_run += 1

        code, output = run_script(
            "Request-PreMortemXCalibrationChange.py",
            "--ChangeTier",
            "TierB",
            "--ChangeType",
            "confidence-band-tuning",
            "--ProposedValue",
            '{"confidence":4}',
            "--Reason",
            "python-regression-tuning",
            "--RequestedBy",
            "python-codex",
            "--DatabasePath",
            str(CALIBRATION_DB),
        )
        assert_true(code == 0, f"Python calibration change request should succeed.\n{output}")
        change_request = json.loads(output)
        tests_run += 1

        code, output = run_script(
            "Approve-PreMortemXCalibrationChange.py",
            "--ChangeRequestId",
            change_request["changeRequestId"],
            "--ApprovalScope",
            "session",
            "--ApprovalDecision",
            "approved",
            "--ApprovedBy",
            "python-codex",
            "--ApprovalNote",
            "python-bounded-approval",
            "--DatabasePath",
            str(CALIBRATION_DB),
        )
        assert_true(code == 0, f"Python calibration approval should succeed.\n{output}")
        approval = json.loads(output)
        assert_true(approval["status"] == "approved", "Python approval should succeed.")
        tests_run += 1

        code, output = run_script("Get-PreMortemXAdvisoryDelegationPlan.py")
        assert_true(code == 0, f"Python advisory plan should succeed.\n{output}")
        advisory = json.loads(output)
        assert_true(advisory["authorityMode"] == "local-only", "Python advisory plan should keep local-only authority.")
        assert_true(len(advisory["optionallyDelegated"]) >= 1, "Python advisory plan should populate optional delegation.")
        tests_run += 1

        code, output = run_script("Get-PreMortemXRegistrySummary.py")
        assert_true(code == 0, f"Python quality-aware registry summary should succeed.\n{output}")
        quality_summary = json.loads(output)
        assert_true(quality_summary["totalReviewed"] >= 1, "Python registry summary should include reviewed counts.")
        assert_true(quality_summary["byReviewOutcome"]["accurate"] >= 1, "Python registry summary should include review outcomes.")
        assert_true(quality_summary["pendingQualityFollowup"] >= 0, "Python registry summary should include pending quality follow-up count.")
        tests_run += 1

        code, output = run_script("Build-PreMortemXRegistryViews.py")
        assert_true(code == 0, f"Python quality-aware registry view build should succeed.\n{output}")
        dashboard = (views_root / "dashboard.md").read_text(encoding="utf-8")
        assert_true("Reviewed runs:" in dashboard, "Python dashboard should include reviewed run counts.")
        assert_true("Pending quality follow-up:" in dashboard, "Python dashboard should include pending quality follow-up.")
        tests_run += 1

        invalid_record = json.loads(record_path.read_text(encoding="utf-8"))
        invalid_record["decision"] = "Maybe"
        record_path.write_text(json.dumps(invalid_record, indent=2), encoding="utf-8")
        code, output = run_script("Test-PreMortemXRunRecord.py", "--RunRecordPath", str(record_path))
        assert_true(code != 0, "Python invalid decision should fail validation.")
        tests_run += 1
    finally:
        if run_path.exists():
            shutil.rmtree(run_path)
        if arch_run_path and arch_run_path.exists():
            shutil.rmtree(arch_run_path)
        if index_backup is None:
            if index_path.exists():
                index_path.unlink()
        else:
            index_path.write_text(index_backup, encoding="utf-8")
        if quality_backup is None:
            if quality_log_path.exists():
                quality_log_path.unlink()
        else:
            quality_log_path.write_text(quality_backup, encoding="utf-8")
        if not views_backup and views_root.exists():
            shutil.rmtree(views_root)
        if CALIBRATION_DB.exists():
            CALIBRATION_DB.unlink()

    print(f"PreMortemX Python runtime tests passed: {tests_run}")


if __name__ == "__main__":
    main()
