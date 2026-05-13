from __future__ import annotations

import json
import re
import uuid
from collections import Counter
from datetime import datetime, timezone
from html import escape as html_escape
from pathlib import Path
from typing import Any


ALLOWED_DECISIONS = {"Pass", "Warn", "Block"}
ALLOWED_MODES = {"release-risk-gating", "architecture-validation"}
ALLOWED_TASK_CATEGORIES = {"risk-analysis", "calibration"}
ALLOWED_PROMOTION_STATES = {"trusted", "provisional", "excluded"}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def run_id(project_slug: str, now: datetime) -> str:
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:6]
    return f"pmx-{project_slug}-{stamp}-{suffix}"


def confidence_to_int(band: str) -> int:
    mapping = {
        "Very Low": 1,
        "Low": 2,
        "Medium": 3,
        "Medium-High": 4,
        "High": 4,
        "Very High": 5,
    }
    return mapping.get(band, 3)


def confidence_band(value: int) -> str:
    bands = {
        1: "Very Low",
        2: "Low",
        3: "Medium",
        4: "Medium-High",
        5: "High",
    }
    return bands[max(1, min(5, int(value)))]


def decision_rank(decision: str) -> int:
    return {"Pass": 1, "Warn": 2, "Block": 3}[decision]


def plugin_root_from_script(script_path: str | Path) -> Path:
    return Path(script_path).resolve().parent.parent


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def as_doc_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def report_title(mode: str) -> str:
    return (
        "PreMortemX Architecture Assessment"
        if mode == "architecture-validation"
        else "PreMortemX Release Assessment"
    )


def task_type_for_mode(mode: str) -> str:
    return "architecture-review" if mode == "architecture-validation" else "premortem"


def resolve_governance_assets(plugin_root: str | Path, mode: str) -> dict[str, Any]:
    root = Path(plugin_root)
    governance_root = root / "governance"
    prompt = governance_root / "prompts" / "governance-prompt-core-risk-governance.md"
    overlay_name = (
        "task-overlay-release-risk-gating.md"
        if mode == "release-risk-gating"
        else "task-overlay-release-risk-gating.md"
    )
    overlay = governance_root / "overlays" / overlay_name
    policy_pack = governance_root / "policy-packs" / "policy-pack-release-risk-core.md"
    template = governance_root / "templates" / "template-card-release-risk-standard-summary.md"
    role_cards = {
        "Orchestrator": governance_root / "roles" / "role-card-orchestrator.md",
        "Evidence Auditor": governance_root / "roles" / "role-card-evidence-auditor.md",
        "Domain Risk Specialist": governance_root / "roles" / "role-card-domain-risk-specialist.md",
    }
    control_cards = {
        "High-Sensitivity Approval": governance_root / "controls" / "control-card-high-sensitivity-approval.md",
    }
    required_paths = [prompt, overlay, policy_pack, template, *role_cards.values(), *control_cards.values()]
    missing = [as_doc_path(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing governed asset files: {', '.join(missing)}")
    return {
        "version": "v5a-1",
        "prompt": {"name": "Core Risk Governance Prompt", "path": as_doc_path(prompt)},
        "overlay": {"name": "Release Risk Gating Overlay", "path": as_doc_path(overlay)},
        "policyPack": {"name": "Release Risk Core Policy Pack", "path": as_doc_path(policy_pack)},
        "template": {"name": "Release Risk Standard Summary Template", "path": as_doc_path(template)},
        "roleCards": [{"name": name, "path": as_doc_path(path)} for name, path in role_cards.items()],
        "controlCards": [{"name": name, "path": as_doc_path(path)} for name, path in control_cards.items()],
    }


def resolve_workflow_assets(plugin_root: str | Path, mode: str) -> dict[str, Any]:
    root = Path(plugin_root)
    workflow_root = root / "workflow"
    lifecycle = workflow_root / "lifecycle" / "lifecycle-map-core-release-risk.md"
    intake = workflow_root / "stages" / "stage-definition-intake.md"
    assess = workflow_root / "stages" / "stage-definition-assess.md"
    approval = workflow_root / "approvals" / "approval-playbook-high-sensitivity-release-decision.md"
    handoff = workflow_root / "handoffs" / "handoff-summary-assess-to-deliberate.md"
    exception = workflow_root / "exceptions" / "exception-rule-missing-evidence-reentry.md"
    required_paths = [lifecycle, intake, assess, approval, handoff, exception]
    missing = [as_doc_path(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing workflow asset files: {', '.join(missing)}")
    return {
        "version": "v5b-1",
        "lifecycleMap": {"name": "Core Release Risk Lifecycle Map", "path": as_doc_path(lifecycle)},
        "stageDefinitions": [
            {"name": "Intake Stage Definition", "path": as_doc_path(intake)},
            {"name": "Assess Stage Definition", "path": as_doc_path(assess)},
        ],
        "approvalPlaybooks": [
            {"name": "High-Sensitivity Release Decision Approval Playbook", "path": as_doc_path(approval)},
        ],
        "handoffs": [
            {"name": "Assess To Deliberate Handoff Summary", "path": as_doc_path(handoff)},
        ],
        "exceptionRules": [
            {"name": "Missing Evidence Re-entry Rule", "path": as_doc_path(exception)},
        ],
        "modeBinding": mode,
    }


def resolve_runtime_assets(plugin_root: str | Path, mode: str) -> dict[str, Any]:
    root = Path(plugin_root)
    runtime_root = root / "runtime"
    control_tower = runtime_root / "dashboards" / "control-tower-view-default-release-risk.md"
    factsheet = runtime_root / "factsheets" / "governed-run-factsheet-release-risk-synthetic.md"
    boundary = runtime_root / "policies" / "boundary-enforcement-panel-release-risk-synthetic.md"
    resolver = runtime_root / "policies" / "policy-resolver-record-release-risk-synthetic.md"
    context = runtime_root / "context" / "context-contract-release-risk-synthetic.md"
    trace = runtime_root / "traces" / "runtime-trace-summary-release-risk-synthetic.md"
    required_paths = [control_tower, factsheet, boundary, resolver, context, trace]
    missing = [as_doc_path(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing runtime asset files: {', '.join(missing)}")
    return {
        "version": "v5c-1",
        "controlTowerView": {"name": "Default Release Risk Control Tower View", "path": as_doc_path(control_tower)},
        "governedRunFactsheet": {"name": "Release Risk Governed Run Factsheet", "path": as_doc_path(factsheet)},
        "boundaryPanel": {"name": "Release Risk Boundary And Enforcement Panel", "path": as_doc_path(boundary)},
        "policyResolverRecord": {"name": "Release Risk Policy Resolver Record", "path": as_doc_path(resolver)},
        "contextContract": {"name": "Release Risk Context Contract", "path": as_doc_path(context)},
        "runtimeTraceSummary": {"name": "Release Risk Runtime Trace Summary", "path": as_doc_path(trace)},
        "modeBinding": mode,
    }


def default_record(
    plugin_root: str | Path,
    project_slug: str,
    mode: str,
    decision: str,
    confidence_band_value: str,
    now: datetime,
    run_dir: Path,
) -> dict[str, Any]:
    rid = run_id(project_slug, now)
    artifact_rel = run_dir.as_posix().split("/plugins/premortemx/")[-1] if "/plugins/premortemx/" in run_dir.as_posix() else "/".join(run_dir.parts[-4:])
    governance_assets = resolve_governance_assets(plugin_root, mode)
    workflow_assets = resolve_workflow_assets(plugin_root, mode)
    runtime_assets = resolve_runtime_assets(plugin_root, mode)
    record = {
        "schemaVersion": "1.0",
        "runId": rid,
        "pluginVersion": "0.4.0",
        "createdAt": now.isoformat().replace("+00:00", "Z"),
        "updatedAt": now.isoformat().replace("+00:00", "Z"),
        "status": "initialized",
        "projectSlug": project_slug,
        "taskType": task_type_for_mode(mode),
        "taskCategory": "risk-analysis",
        "initiator": "codex",
        "executionMode": "skill+scripts",
        "approvalMode": "adaptive",
        "privacyMode": "privacy-first-hybrid",
        "retentionClass": "standard",
        "artifactPath": artifact_rel.replace("\\", "/"),
        "registryRefs": {"indexKey": f"{now.strftime('%Y-%m')}/{rid}"},
        "inputFingerprint": {"contextHash": None, "promptHash": None},
        "mode": mode,
        "routingType": "hybrid",
        "governanceAssets": governance_assets,
        "workflowAssets": workflow_assets,
        "runtimeAssets": runtime_assets,
        "workflowState": {
            "lifecycle": "Core Release Risk Lifecycle Map",
            "currentStage": "Intake",
            "completedStages": [],
            "nextStage": "Assess",
            "pendingApprovalPlaybook": "High-Sensitivity Release Decision Approval Playbook",
            "activeExceptionRule": None,
            "assessEntryStatus": "ready",
            "assessEntryBlockers": [],
            "deliberateHandoffStatus": "pending-assess",
            "handoffBlockers": [],
            "gateStatus": "confirmation-required",
            "allowedNextStage": None,
            "blockedBy": ["The current decision posture requires explicit confirmation before proceeding."],
        },
        "runtimeState": {
            "activePolicyProfile": "release-risk-core",
            "runtimeMode": "python-first local runtime",
            "approvalPosture": "Tier B for sensitive Warn/Block outcomes",
            "allowedEvidenceClasses": ["designDocs", "releasePlan", "testEvidence", "dependencies", "architectureContext", "implementationContext", "advisoryDelegationUsed"],
            "boundaryStatus": "clean",
            "blockedContextClasses": [],
            "carryForwardAllowed": True,
            "transformationStatus": "pending",
            "carryForwardLedger": [],
            "trustedInstructionSources": [
                governance_assets["prompt"]["name"],
                governance_assets["overlay"]["name"],
                governance_assets["policyPack"]["name"],
            ],
            "openBreaches": [],
            "attentionItems": ["Verify monitored owner follow-up remains assigned."],
            "traceStatus": "initialized",
            "confirmationRequired": True,
            "confirmationReason": "A Warn decision should be explicitly accepted or mitigated before proceeding.",
            "resumeGuidance": "Resume from `Assess` when the run has enough evidence to continue.",
            "proceedAllowed": False,
            "proceedBlockers": ["The current decision posture requires explicit confirmation before proceeding."],
        },
        "decision": decision,
        "confidenceBand": confidence_band_value,
        "inspectedInputs": {
            "designDocs": [],
            "architectureContext": [],
            "implementationContext": [],
            "releasePlan": [],
            "testEvidence": [],
            "dependencies": [],
            "constraints": [],
        },
        "riskSummary": {"low": 0, "medium": 0, "high": 0},
        "topRisks": [],
        "evidenceCoverage": "incomplete",
        "calibrationState": {
            "promotionState": "excluded",
            "datasetVersion": None,
            "caseId": None,
        },
        "executionBoundary": {
            "authorityMode": "local-only",
            "advisoryMode": "cloud-only-advisory",
            "advisoryDelegationAllowed": True,
            "advisoryDelegationUsed": [],
        },
        "deliberation": {
            "version": "3.0",
            "adjudicatedBy": "orchestrator",
            "status": "initialized",
            "sharedRoles": [
                "Evidence Auditor",
                "Decision Policy Reviewer",
                "Orchestrator",
            ],
            "specialistRoles": [
                "Domain Risk Specialist",
                "Operational/Release Risk Specialist",
                "Security/Privacy Risk Specialist",
            ],
            "specialists": [],
            "agreement": {
                "consensusDecision": decision,
                "disagreementLevel": 1,
                "summary": "Pending deliberation.",
            },
            "rubric": {
                "gradingScale": "1-5",
                "confidence": confidence_to_int(confidence_band_value),
                "evidenceStrength": 3,
                "riskSeverity": 3,
                "evidenceCompleteness": 3,
                "disagreementLevel": 1,
                "policyFit": 3,
                "decisionSensitivity": 3,
                "sourceProvenance": 3,
                "mitigationReadiness": 3,
                "calibratedPatternFit": 3,
                "contradictoryArtifactPressure": 1,
            },
            "overrideModel": {
                "defaultTrigger": "evidence-gated",
                "backstopTrigger": "severity-and-policy",
                "overrideApplied": False,
                "overrideReason": None,
                "humanEscalationRequired": False,
                "humanEscalationReasons": [],
                "overrideTestSummary": "Pending override evaluation.",
            },
            "adjudication": {
                "finalDecision": decision,
                "finalConfidenceBand": confidence_band_value,
                "summary": "Pending orchestrator synthesis.",
                "supportingEvidence": [],
                "decisionOwner": None,
                "ruleTriggered": "pending",
                "humanEscalationConsidered": False,
                "residualRiskAfterMitigation": "pending",
                "decisionPath": [],
                "uncertaintyDrivers": [],
            },
        },
        "warnReasons": [],
        "blockReasons": [],
        "outputTiers": ["short", "standard", "exec"],
        "permissionEscalationsRequested": [],
        "permissionEscalationsApproved": [],
        "guardrailRecommendations": [],
        "override": {
            "applied": False,
            "rationale": None,
            "mitigationSteps": [],
            "responsibleOwner": None,
        },
        "sensitivityReview": {
            "likelySensitive": False,
            "recommendedProtection": "none",
            "encryptionUsed": False,
        },
        "artifacts": {
            "startHere": "start-here.md",
            "journeyView": "journey-view.html",
            "journeyData": "journey-view.json",
            "summaryShort": "summary-short.md",
            "summaryStandard": "summary-standard.md",
            "summaryExec": "summary-exec.md",
            "riskRegister": "risk-register.md",
            "runRecord": "run-record.json",
            "analysis": "analysis.json",
            "approvals": "approvals.json",
            "retention": "retention.json",
            "override": None,
            "evidenceIndex": "evidence-index.md",
            "deliberation": "deliberation.json",
        },
        "qualityFollowup": {
            "status": "pending",
            "reviewDue": None,
            "falsePositiveNotes": [],
            "missedRiskNotes": [],
            "outcomeNotes": [],
        },
    }
    _refresh_derived_state(record)
    return record


def _write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any] | list[Any]) -> None:
    path.write_text(json.dumps(payload, indent=4), encoding="utf-8")


def _display_timestamp(value: str | None) -> str:
    if not value:
        return "unknown"
    return value.replace("T", " ").replace("Z", " UTC")


def _approval_recommendation(record: dict[str, Any]) -> str:
    if record["deliberation"]["overrideModel"]["humanEscalationRequired"]:
        return "human-escalation-required"
    return "stay-conservative"


def _decision_summary_from_action(action: str) -> str:
    mapping = {
        "confirm-or-mitigate": "Confirm the current decision posture or add mitigation before proceeding.",
        "fix-intake-before-assess": "Complete the missing intake prerequisites before the run can move forward.",
        "complete-handoff-before-monitor": "Complete the handoff requirements before the run can move into monitoring.",
        "complete-handoff-before-revisit": "Complete the handoff requirements before the run can return for revisit.",
        "resolve-boundary-before-monitor": "Resolve the blocked context boundary before the run can move into monitoring.",
        "resolve-boundary-before-revisit": "Resolve the blocked context boundary before the run can return for revisit.",
        "escalate-before-monitor": "Escalate the current decision before the run can move into monitoring.",
        "escalate-before-revisit": "Escalate the current decision before the run can return for revisit.",
        "resolve-exception-before-monitor": "Resolve the active exception rule before the run can move into monitoring.",
        "resolve-exception-before-revisit": "Resolve the active exception rule before the run can return for revisit.",
        "reverse-or-escalate": "Escalate the blocked decision and resolve the evidence gap before re-entry.",
        "confirm-before-monitor": "Keep the monitored follow-up active before moving to a cleaner release posture.",
        "continue-to-monitor": "Continue the approved path with normal monitoring.",
    }
    return mapping.get(action, "Continue the governed workflow using the current decision posture.")


def _next_action_summary(record: dict[str, Any]) -> str:
    return _decision_summary_from_action(_current_action(record))


def _next_action_items(record: dict[str, Any]) -> list[str]:
    items = list(record["runtimeState"].get("attentionItems", []))
    if not items:
        items = [f"Advance the run into `{record['workflowState']['nextStage']}` with the current decision posture."]
    return items


def _confirmation_required(record: dict[str, Any]) -> bool:
    return bool(record["deliberation"]["overrideModel"]["humanEscalationRequired"]) or record["decision"] in {"Warn", "Block"}


def _confirmation_reason(record: dict[str, Any]) -> str:
    if record["deliberation"]["overrideModel"]["humanEscalationRequired"]:
        return "Human escalation is required before the workflow can proceed."
    if record["decision"] == "Warn":
        return "A Warn decision should be explicitly accepted or mitigated before proceeding."
    if record["decision"] == "Block":
        return "A Block decision must be explicitly escalated or reversed with new evidence before proceeding."
    return "No additional confirmation is required beyond normal monitoring."


def _resume_guidance(record: dict[str, Any]) -> str:
    if record["workflowState"]["activeExceptionRule"]:
        return f"Resume from `{record['workflowState']['nextStage']}` after resolving the active exception rule."
    return f"Resume from `{record['workflowState']['nextStage']}` when the next action items are complete."


def _proceed_blockers(record: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    workflow_state = _workflow_stage_state(record)
    blockers.extend(workflow_state["assessEntryBlockers"])
    blockers.extend(workflow_state["handoffBlockers"])
    if _boundary_findings(record):
        blockers.append("Blocked or excluded context must be removed or explicitly governed before proceeding.")
    if _transformation_findings(record):
        blockers.append("Untransformed context must be converted into governed evidence references before proceeding.")
    if any(item["carryForwardState"] == "quarantined" for item in _carry_forward_ledger(record)):
        blockers.append("Quarantined context must be promoted or discarded before proceeding.")
    if record["workflowState"]["activeExceptionRule"]:
        blockers.append("An active exception rule must be resolved before proceeding.")
    if record["deliberation"]["overrideModel"]["humanEscalationRequired"]:
        blockers.append("Human escalation is required before proceeding.")
    elif record["decision"] in {"Warn", "Block"}:
        blockers.append("The current decision posture requires explicit confirmation before proceeding.")
    if len(record["permissionEscalationsRequested"]) > len(record["permissionEscalationsApproved"]):
        blockers.append("Requested permission broadening remains unresolved.")
    return blockers


def _proceed_allowed(record: dict[str, Any]) -> bool:
    return len(_proceed_blockers(record)) == 0


def _workflow_gate_status(record: dict[str, Any]) -> str:
    if _proceed_allowed(record):
        return "ready"
    workflow_state = _workflow_stage_state(record)
    if workflow_state["assessEntryStatus"] == "blocked" or workflow_state["deliberateHandoffStatus"] == "blocked":
        return "workflow-blocked"
    if record["runtimeState"].get("boundaryStatus") in {"blocked-context", "quarantined-context"}:
        return str(record["runtimeState"]["boundaryStatus"])
    if record["deliberation"]["overrideModel"]["humanEscalationRequired"]:
        return "awaiting-human-escalation"
    if record["workflowState"]["activeExceptionRule"]:
        return "exception-blocked"
    return "confirmation-required"


def _allowed_next_stage(record: dict[str, Any]) -> str | None:
    return record["workflowState"]["nextStage"] if _proceed_allowed(record) else None


def _approval_status(record: dict[str, Any]) -> str:
    if record["deliberation"]["status"] != "completed":
        return "pending-review"
    mapping = {
        "ready": "approved-for-monitor",
        "workflow-blocked": "workflow-remediation-required",
        "blocked-context": "boundary-remediation-required",
        "quarantined-context": "boundary-remediation-required",
        "awaiting-human-escalation": "awaiting-human-escalation",
        "exception-blocked": "revisit-required",
        "confirmation-required": "pending-confirmation",
    }
    return mapping[_workflow_gate_status(record)]


def _current_action(record: dict[str, Any]) -> str:
    if record["deliberation"]["status"] != "completed":
        return "confirm-or-mitigate"
    workflow_state = _workflow_stage_state(record)
    if workflow_state["assessEntryStatus"] == "blocked":
        return "fix-intake-before-assess"
    if workflow_state["deliberateHandoffStatus"] == "blocked":
        return "complete-handoff-before-revisit" if record["workflowState"]["nextStage"] == "Revisit" else "complete-handoff-before-monitor"
    if record["runtimeState"].get("boundaryStatus") in {"blocked-context", "quarantined-context"}:
        return "resolve-boundary-before-revisit" if record["workflowState"]["nextStage"] == "Revisit" else "resolve-boundary-before-monitor"
    if record["deliberation"]["overrideModel"]["humanEscalationRequired"]:
        return "escalate-before-revisit" if record["workflowState"]["nextStage"] == "Revisit" else "escalate-before-monitor"
    if record["workflowState"]["activeExceptionRule"]:
        return "resolve-exception-before-revisit" if record["workflowState"]["nextStage"] == "Revisit" else "resolve-exception-before-monitor"
    if record["decision"] == "Block":
        return "reverse-or-escalate"
    if record["decision"] == "Warn":
        return "confirm-before-monitor"
    return "continue-to-monitor"


def _normalized_marker_text(value: Any) -> str:
    return str(value).strip()


def _has_marker_prefix(value: Any, prefix: str) -> bool:
    return _normalized_marker_text(value).upper().startswith(prefix.upper())


def _status_value(record: dict[str, Any]) -> str:
    return "adjudicated" if record["deliberation"]["status"] == "completed" else "initialized"


def _public_ledger_value(item: dict[str, Any]) -> str:
    state = str(item.get("carryForwardState") or "unknown")
    source = str(item.get("sourceClass") or "unknown")
    if state == "promoted":
        return str(item.get("value") or "")
    return f"redacted:{source}:{state}"


def _public_carry_forward_ledger(record: dict[str, Any]) -> list[dict[str, Any]]:
    public_items: list[dict[str, Any]] = []
    for item in record["runtimeState"].get("carryForwardLedger", []):
        public_items.append(
            {
                "sourceClass": item.get("sourceClass"),
                "value": _public_ledger_value(item),
                "destination": list(item.get("destination", [])),
                "transformationStatus": item.get("transformationStatus"),
                "carryForwardState": item.get("carryForwardState"),
            }
        )
    return public_items


def _refresh_derived_state(record: dict[str, Any]) -> None:
    ledger = _carry_forward_ledger(record)
    transformation_findings = _transformation_findings(record)
    record["runtimeState"]["allowedEvidenceClasses"] = ["designDocs", "releasePlan", "testEvidence", "dependencies", "architectureContext", "implementationContext", "advisoryDelegationUsed"]
    record["runtimeState"]["boundaryStatus"] = _boundary_status(record)
    record["runtimeState"]["blockedContextClasses"] = _blocked_context_classes(record)
    record["runtimeState"]["carryForwardAllowed"] = (
        record["runtimeState"]["boundaryStatus"] == "clean"
        and not transformation_findings
        and all(item["carryForwardState"] == "promoted" for item in ledger)
    )
    record["runtimeState"]["transformationStatus"] = (
        "blocked"
        if record["runtimeState"]["boundaryStatus"] == "blocked-context" or transformation_findings
        else "quarantined"
        if any(item["carryForwardState"] == "quarantined" for item in ledger)
        else "transformed"
    )
    record["runtimeState"]["carryForwardLedger"] = ledger
    record["runtimeState"]["trustedInstructionSources"] = _trusted_instruction_sources(record)
    workflow_state = _workflow_stage_state(record)
    record["workflowState"]["assessEntryStatus"] = workflow_state["assessEntryStatus"]
    record["workflowState"]["assessEntryBlockers"] = workflow_state["assessEntryBlockers"]
    record["workflowState"]["deliberateHandoffStatus"] = workflow_state["deliberateHandoffStatus"]
    record["workflowState"]["handoffBlockers"] = workflow_state["handoffBlockers"]
    record["runtimeState"]["confirmationRequired"] = _confirmation_required(record)
    record["runtimeState"]["confirmationReason"] = _confirmation_reason(record)
    record["runtimeState"]["resumeGuidance"] = _resume_guidance(record)
    record["runtimeState"]["proceedBlockers"] = _proceed_blockers(record)
    record["runtimeState"]["proceedAllowed"] = len(record["runtimeState"]["proceedBlockers"]) == 0
    record["workflowState"]["gateStatus"] = _workflow_gate_status(record)
    record["workflowState"]["allowedNextStage"] = _allowed_next_stage(record)
    record["workflowState"]["blockedBy"] = list(record["runtimeState"]["proceedBlockers"])
    record["status"] = _status_value(record)


def _approvals_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "approvalsRequested": record["permissionEscalationsRequested"],
        "approvalsGranted": record["permissionEscalationsApproved"],
        "recommendation": record["decision"],
        "approvalRecommendation": _approval_recommendation(record),
        "approvalStatus": _approval_status(record),
        "currentAction": _current_action(record),
        "resumeGuidance": record["runtimeState"]["resumeGuidance"],
        "proceedAllowed": record["runtimeState"]["proceedAllowed"],
        "proceedBlockers": record["runtimeState"]["proceedBlockers"],
        "boundaryStatus": record["runtimeState"]["boundaryStatus"],
        "blockedContextClasses": record["runtimeState"]["blockedContextClasses"],
        "carryForwardAllowed": record["runtimeState"]["carryForwardAllowed"],
        "transformationStatus": record["runtimeState"]["transformationStatus"],
        "carryForwardLedger": _public_carry_forward_ledger(record),
        "playbookGateStatus": record["workflowState"]["gateStatus"],
        "allowedNextStage": record["workflowState"]["allowedNextStage"],
        "playbook": record["workflowAssets"]["approvalPlaybooks"][0],
        "workflowState": record["workflowState"],
        "runtimeBoundary": record["runtimeAssets"]["boundaryPanel"],
        "notes": ["Permission escalation events belong here."],
    }


def _boundary_findings(record: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    for value in record.get("inspectedInputs", {}).get("constraints", []):
        if _has_marker_prefix(value, "UNVALIDATED_ASSERTION:"):
            findings.append("Unvalidated assertions were present in the inspected context.")
        if _has_marker_prefix(value, "AMBIENT_CONTEXT:"):
            findings.append("Ambient context was included without explicit governance linkage.")
    for key in ("architectureContext", "implementationContext"):
        for value in record.get("inspectedInputs", {}).get(key, []):
            if _has_marker_prefix(value, "PRIOR_CASE:"):
                findings.append("Prior-case narrative was carried forward without explicit linkage.")
    for item in record.get("executionBoundary", {}).get("advisoryDelegationUsed", []):
        if isinstance(item, dict):
            linked = item.get("linkedArtifact") or item.get("artifactRef")
            if not linked:
                findings.append("External advisory input lacked an explicit linked artifact.")
    deduped: list[str] = []
    for finding in findings:
        if finding not in deduped:
            deduped.append(finding)
    return deduped


def _blocked_context_classes(record: dict[str, Any]) -> list[str]:
    classes: list[str] = []
    for value in record.get("inspectedInputs", {}).get("constraints", []):
        if _has_marker_prefix(value, "UNVALIDATED_ASSERTION:") and "unvalidated-assertion" not in classes:
            classes.append("unvalidated-assertion")
        if _has_marker_prefix(value, "AMBIENT_CONTEXT:") and "ambient-context" not in classes:
            classes.append("ambient-context")
    for key in ("architectureContext", "implementationContext"):
        for value in record.get("inspectedInputs", {}).get(key, []):
            if _has_marker_prefix(value, "PRIOR_CASE:") and "prior-case-carry-forward" not in classes:
                classes.append("prior-case-carry-forward")
    for item in record.get("executionBoundary", {}).get("advisoryDelegationUsed", []):
        if isinstance(item, dict):
            linked = item.get("linkedArtifact") or item.get("artifactRef")
            if not linked and "unlinked-advisory-context" not in classes:
                classes.append("unlinked-advisory-context")
    return classes


def _transformation_findings(record: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    allowed_prefixes = ("EVIDENCE_REF:", "SUMMARY_REF:", "PRIOR_CASE:")
    for key in ("architectureContext", "implementationContext"):
        for value in record.get("inspectedInputs", {}).get(key, []):
            text = _normalized_marker_text(value)
            if text and not text.upper().startswith(tuple(prefix.upper() for prefix in allowed_prefixes)):
                findings.append("Context items must be transformed into governed evidence references before carry-forward.")
                return findings
    return findings


def _carry_forward_ledger(record: dict[str, Any]) -> list[dict[str, Any]]:
    ledger: list[dict[str, Any]] = []
    for field in ("designDocs", "releasePlan", "testEvidence", "dependencies"):
        for value in record.get("inspectedInputs", {}).get(field, []):
            ledger.append(
                {
                    "sourceClass": field,
                    "value": str(value),
                    "destination": ["orchestrator", "factsheet", "trace"],
                    "transformationStatus": "direct-artifact-ref",
                    "carryForwardState": "promoted",
                }
            )
    for key in ("architectureContext", "implementationContext"):
        for value in record.get("inspectedInputs", {}).get(key, []):
            text = str(value)
            if text.startswith(("EVIDENCE_REF:", "SUMMARY_REF:")):
                ledger.append(
                    {
                        "sourceClass": key,
                        "value": text,
                        "destination": ["orchestrator", "factsheet", "trace"],
                        "transformationStatus": "evidence-indexed",
                        "carryForwardState": "promoted",
                    }
                )
            elif text.startswith("PRIOR_CASE:"):
                ledger.append(
                    {
                        "sourceClass": key,
                        "value": text,
                        "destination": ["trace"],
                        "transformationStatus": "blocked-prior-case",
                        "carryForwardState": "blocked",
                    }
                )
            elif text:
                ledger.append(
                    {
                        "sourceClass": key,
                        "value": text,
                        "destination": [],
                        "transformationStatus": "untransformed",
                        "carryForwardState": "blocked",
                    }
                )
    for item in record.get("executionBoundary", {}).get("advisoryDelegationUsed", []):
        if not isinstance(item, dict):
            ledger.append(
                {
                    "sourceClass": "advisoryDelegationUsed",
                    "value": str(item),
                    "destination": [],
                    "transformationStatus": "malformed-advisory",
                    "carryForwardState": "blocked",
                }
            )
            continue
        linked = item.get("linkedArtifact") or item.get("artifactRef")
        promoted = bool(item.get("promoted"))
        if not linked:
            ledger.append(
                {
                    "sourceClass": "advisoryDelegationUsed",
                    "value": str(item.get("summary") or item.get("advisor") or "advisory-input"),
                    "destination": [],
                    "transformationStatus": "unlinked-advisory",
                    "carryForwardState": "blocked",
                }
            )
        elif promoted:
            ledger.append(
                {
                    "sourceClass": "advisoryDelegationUsed",
                    "value": str(linked),
                    "destination": ["orchestrator", "trace"],
                    "transformationStatus": "linked-advisory",
                    "carryForwardState": "promoted",
                }
            )
        else:
            ledger.append(
                {
                    "sourceClass": "advisoryDelegationUsed",
                    "value": str(linked),
                    "destination": ["trace"],
                    "transformationStatus": "linked-advisory",
                    "carryForwardState": "quarantined",
                }
            )
    return ledger


def _trusted_instruction_sources(record: dict[str, Any]) -> list[str]:
    return [
        record["governanceAssets"]["prompt"]["name"],
        record["governanceAssets"]["overlay"]["name"],
        record["governanceAssets"]["policyPack"]["name"],
    ]


def _boundary_status(record: dict[str, Any]) -> str:
    if _boundary_findings(record) or _transformation_findings(record):
        return "blocked-context"
    if any(item["carryForwardState"] == "quarantined" for item in _carry_forward_ledger(record)):
        return "quarantined-context"
    return "clean"


def _workflow_stage_state(record: dict[str, Any]) -> dict[str, Any]:
    constraints = {str(value) for value in record.get("inspectedInputs", {}).get("constraints", [])}
    assess_entry_blockers: list[str] = []
    handoff_blockers: list[str] = []

    if "MISSING_TARGET_SCOPE" in constraints:
        assess_entry_blockers.append("Assess entry criteria are not met: bounded scope is missing.")
    if "MISSING_EVIDENCE_BUNDLE" in constraints:
        assess_entry_blockers.append("Assess entry criteria are not met: evidence bundle is not named.")

    if record["deliberation"]["status"] == "completed":
        if "MISSING_HANDOFF_SUMMARY" in constraints:
            handoff_blockers.append("Assess-to-deliberate handoff is incomplete: handoff summary is missing.")
        if "MISSING_RISK_PICTURE" in constraints:
            handoff_blockers.append("Assess-to-deliberate handoff is incomplete: structured risk picture is missing.")
        if not record.get("topRisks") and not record["runtimeState"].get("openBreaches"):
            handoff_blockers.append("Assess-to-deliberate handoff is incomplete: no risk picture or evidence-gap output was recorded.")

    return {
        "assessEntryStatus": "blocked" if assess_entry_blockers else "ready",
        "assessEntryBlockers": assess_entry_blockers,
        "deliberateHandoffStatus": (
            "pending-assess"
            if record["deliberation"]["status"] != "completed"
            else "blocked" if handoff_blockers else "ready"
        ),
        "handoffBlockers": handoff_blockers,
    }


def _journey_stage_sequence() -> list[str]:
    return ["Intake", "Assess", "Deliberate", "Approve/Block", "Monitor", "Revisit"]


def _journey_owner(record: dict[str, Any]) -> str:
    return (
        "Architecture decision owner"
        if record["mode"] == "architecture-validation"
        else "Release decision owner"
    )


def _journey_blocker_path_type(blocker: str) -> str:
    text = blocker.lower()
    if any(token in text for token in ("approval", "confirmation", "escalation", "human")):
        return "approval"
    if "boundary" in text or "context" in text:
        return "boundary"
    if "exception" in text:
        return "revisit"
    return "risk"


def _journey_is_compact(record: dict[str, Any]) -> bool:
    return (
        record["decision"] == "Pass"
        and len(record.get("topRisks", [])) <= 1
        and record["runtimeState"]["boundaryStatus"] == "clean"
        and not record["deliberation"]["overrideModel"]["humanEscalationRequired"]
        and not record["workflowState"]["activeExceptionRule"]
        and not record["runtimeState"]["proceedBlockers"]
    )


def _derive_journey_view(record: dict[str, Any]) -> dict[str, Any]:
    warnings: list[str] = []
    if record["mode"] != "release-risk-gating":
        warnings.append("V6A journey view is optimized for release-risk-gating; non-release mode is rendered with reduced specificity.")

    stage_sequence = _journey_stage_sequence()
    completed = set(record["workflowState"].get("completedStages", []))
    current_stage = record["workflowState"]["currentStage"]
    current_index = stage_sequence.index(current_stage) if current_stage in stage_sequence else 0
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    def add_node(
        node_id: str,
        parent_id: str | None,
        kind: str,
        stage: str,
        title: str,
        status: str,
        path_type: str,
        summary: str,
        *,
        decision: str | None = None,
        gate_status: str | None = None,
        boundary_status: str | None = None,
        owner: str | None = None,
        next_action: str | None = None,
        resume_stage: str | None = None,
        source_refs: list[str] | None = None,
        risk_level: str | None = None,
        residual_risk: str | None = None,
        approval_status: str | None = None,
        is_current: bool = False,
        is_winning_path: bool = False,
        is_blocked: bool = False,
        blocked_by: list[str] | None = None,
        display_order: int | None = None,
    ) -> None:
        nodes.append(
            {
                "id": node_id,
                "parentId": parent_id,
                "kind": kind,
                "stage": stage,
                "title": title,
                "status": status,
                "pathType": path_type,
                "decision": decision or record["decision"],
                "gateStatus": gate_status or record["workflowState"]["gateStatus"],
                "boundaryStatus": boundary_status or record["runtimeState"]["boundaryStatus"],
                "summary": summary,
                "owner": owner,
                "nextAction": next_action,
                "resumeStage": resume_stage,
                "sourceRefs": list(source_refs or []),
                "riskLevel": risk_level,
                "residualRisk": residual_risk,
                "approvalStatus": approval_status,
                "isCurrent": is_current,
                "isWinningPath": is_winning_path,
                "isBlocked": is_blocked,
                "blockedBy": list(blocked_by or []),
                "displayOrder": display_order,
            }
        )

    previous_stage_node_id: str | None = None
    current_node_id = f"stage-{current_stage.lower().replace('/', '-').replace(' ', '-')}"
    for index, stage in enumerate(stage_sequence):
        node_id = f"stage-{stage.lower().replace('/', '-').replace(' ', '-')}"
        if stage in completed:
            status = "completed"
        elif stage == current_stage:
            status = "current"
        elif index == current_index + 1:
            status = "next"
        else:
            status = "pending"
        add_node(
            node_id,
            previous_stage_node_id,
            "stage",
            stage,
            stage,
            status,
            "mainline",
            f"{stage} stage in the governed lifecycle.",
            gate_status=record["workflowState"]["gateStatus"],
            boundary_status=record["runtimeState"]["boundaryStatus"],
            owner=_journey_owner(record),
            next_action=_next_action_summary(record),
            resume_stage=record["workflowState"]["nextStage"],
            source_refs=["run-record.json"],
            approval_status=_approval_status(record),
            is_current=stage == current_stage,
            is_winning_path=index <= current_index,
            is_blocked=stage == current_stage and bool(record["runtimeState"]["proceedBlockers"]),
            blocked_by=record["runtimeState"]["proceedBlockers"] if stage == current_stage else [],
            display_order=index,
        )
        if previous_stage_node_id is not None:
            edges.append(
                {
                    "id": f"edge-{previous_stage_node_id}-to-{node_id}",
                    "from": previous_stage_node_id,
                    "to": node_id,
                    "type": "progresses",
                    "label": "progresses",
                    "isWinningPath": index <= current_index,
                    "sourceRefs": ["run-record.json"],
                    "isBlockedEdge": False,
                    "precedenceRank": index,
                }
            )
        previous_stage_node_id = node_id

    top_risks = record.get("topRisks", [])
    for index, risk in enumerate(top_risks or [{"role": "Orchestrator", "summary": "Governed path summary", "recommendation": record["decision"], "evidenceRefs": []}], start=1):
        node_id = f"branch-risk-{index}"
        summary = risk.get("summary") or "Governed branch detail."
        add_node(
            node_id,
            current_node_id,
            "branch",
            current_stage,
            risk.get("role") or f"Branch {index}",
            "blocked" if record["runtimeState"]["proceedBlockers"] else "active",
            "risk",
            summary,
            decision=risk.get("recommendation") or record["decision"],
            owner=_journey_owner(record),
            next_action=_next_action_summary(record),
            resume_stage=record["workflowState"]["nextStage"],
            source_refs=list(risk.get("evidenceRefs", [])) or ["deliberation.json"],
            risk_level=record["decision"],
            residual_risk=record["deliberation"]["adjudication"].get("residualRiskAfterMitigation"),
            approval_status=_approval_status(record),
            is_current=index == 1,
            is_winning_path=index == 1,
            is_blocked=bool(record["runtimeState"]["proceedBlockers"]),
            blocked_by=record["runtimeState"]["proceedBlockers"],
            display_order=100 + index,
        )
        edges.append(
            {
                "id": f"edge-{current_node_id}-to-{node_id}",
                "from": current_node_id,
                "to": node_id,
                "type": "branches",
                "label": "branches",
                "isWinningPath": index == 1,
                "sourceRefs": list(risk.get("evidenceRefs", [])) or ["deliberation.json"],
                "isBlockedEdge": False,
                "precedenceRank": index,
            }
        )

    if not top_risks:
        mainline_node_id = "branch-mainline-1"
        add_node(
            mainline_node_id,
            current_node_id,
            "branch",
            current_stage,
            "Governed mainline path",
            "active",
            "mainline",
            "The governed path remains straightforward with no competing branch pressure recorded yet.",
            owner=_journey_owner(record),
            next_action=_next_action_summary(record),
            resume_stage=record["workflowState"]["nextStage"],
            source_refs=["run-record.json"],
            risk_level=record["decision"],
            approval_status=_approval_status(record),
            is_current=True,
            is_winning_path=True,
            display_order=100,
        )
        edges.append(
            {
                "id": f"edge-{current_node_id}-to-{mainline_node_id}",
                "from": current_node_id,
                "to": mainline_node_id,
                "type": "branches",
                "label": "branches",
                "isWinningPath": True,
                "sourceRefs": ["run-record.json"],
                "isBlockedEdge": False,
                "precedenceRank": 1,
            }
        )

    for index, blocker in enumerate(record["runtimeState"]["proceedBlockers"], start=1):
        blocker_node_id = f"gate-blocker-{index}"
        add_node(
            blocker_node_id,
            current_node_id,
            "gate",
            current_stage,
            f"Blocker {index}",
            "blocked",
            _journey_blocker_path_type(blocker),
            blocker,
            owner=_journey_owner(record),
            next_action=_next_action_summary(record),
            resume_stage=record["workflowState"]["nextStage"],
            source_refs=["approvals.json", "run-record.json"],
            approval_status=_approval_status(record),
            is_blocked=True,
            blocked_by=[blocker],
            display_order=200 + index,
        )
        edges.append(
            {
                "id": f"edge-{current_node_id}-to-{blocker_node_id}",
                "from": current_node_id,
                "to": blocker_node_id,
                "type": "blocked-by",
                "label": "blocked by",
                "isWinningPath": False,
                "sourceRefs": ["approvals.json"],
                "isBlockedEdge": True,
                "precedenceRank": index,
            }
        )
    if record["runtimeState"]["resumeGuidance"] and record["runtimeState"]["proceedBlockers"]:
        reentry_node_id = "reentry-shared"
        add_node(
            reentry_node_id,
            current_node_id,
            "reentry",
            record["workflowState"]["nextStage"],
            "Resume path",
            "resume",
            "revisit" if record["workflowState"]["activeExceptionRule"] else "remediation",
            record["runtimeState"]["resumeGuidance"],
            owner=_journey_owner(record),
            next_action=_next_action_summary(record),
            resume_stage=record["workflowState"]["nextStage"],
            source_refs=["approvals.json"],
            approval_status=_approval_status(record),
            display_order=300,
        )
        for index, _blocker in enumerate(record["runtimeState"]["proceedBlockers"], start=1):
            blocker_node_id = f"gate-blocker-{index}"
            edges.append(
                {
                    "id": f"edge-{blocker_node_id}-to-{reentry_node_id}",
                    "from": blocker_node_id,
                    "to": reentry_node_id,
                    "type": "reenters",
                    "label": "re-enters",
                    "isWinningPath": False,
                    "sourceRefs": ["approvals.json"],
                    "isBlockedEdge": False,
                    "precedenceRank": index,
                }
            )

    winning_node_id = "branch-risk-1" if top_risks else "branch-mainline-1"
    gate_card = {
        "nodeId": current_node_id,
        "finalRecommendation": record["decision"],
        "approvalStatus": _approval_status(record),
        "gateStatus": record["workflowState"]["gateStatus"],
        "blockerPrecedence": record["runtimeState"]["proceedBlockers"][0] if record["runtimeState"]["proceedBlockers"] else "none",
        "allowedNextStage": record["workflowState"]["allowedNextStage"],
        "decisionOwner": _journey_owner(record),
        "nextOwner": _journey_owner(record),
        "resumeGuidance": record["runtimeState"]["resumeGuidance"],
        "boundaryStatus": record["runtimeState"]["boundaryStatus"],
        "confirmationRequired": record["runtimeState"]["confirmationRequired"],
        "confirmationReason": record["runtimeState"]["confirmationReason"],
        "currentAction": _current_action(record),
    }

    return {
        "schemaVersion": "v6a-1",
        "runId": record["runId"],
        "mode": record["mode"],
        "generatedAt": record["updatedAt"],
        "currentNodeId": current_node_id,
        "winningNodeId": winning_node_id,
        "isCompact": _journey_is_compact(record),
        "derivationWarnings": warnings,
        "journey": {"nodes": nodes, "edges": edges},
        "gateCard": gate_card,
    }


def _render_journey_svg(journey_view: dict[str, Any]) -> str:
    nodes = sorted(journey_view["journey"]["nodes"], key=lambda item: (item.get("displayOrder") or 0, item["id"]))
    stage_nodes = [node for node in nodes if node["kind"] == "stage"]
    non_stage_nodes = [node for node in nodes if node["kind"] != "stage"]
    stage_width = 150
    stage_start_x = 30
    stage_y = 30
    svg_parts = [f'<svg viewBox="0 0 1080 {max(260, 170 + (len(non_stage_nodes) * 90))}" role="img" aria-label="PreMortemX risk journey view" xmlns="http://www.w3.org/2000/svg">']
    svg_parts.append('<rect x="0" y="0" width="1080" height="100%" fill="#0b0f14"/>')
    svg_parts.append('<line x1="60" y1="74" x2="980" y2="74" stroke="#37506d" stroke-width="4" />')
    for index, node in enumerate(stage_nodes):
        x = stage_start_x + (index * stage_width)
        fill = "#1a7f5a" if node["status"] == "completed" else "#d39c27" if node["status"] == "current" else "#203040"
        stroke = "#9ac7ff" if node["status"] in {"current", "next"} else "#4d6b8a"
        svg_parts.append(f'<rect x="{x}" y="{stage_y}" width="120" height="52" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        svg_parts.append(f'<text x="{x + 12}" y="{stage_y + 22}" fill="#f4f7fb" font-size="12" font-family="Segoe UI, Arial, sans-serif">{html_escape(node["title"])}</text>')
        svg_parts.append(f'<text x="{x + 12}" y="{stage_y + 39}" fill="#c7d8eb" font-size="10" font-family="Segoe UI, Arial, sans-serif">{html_escape(node["status"])}</text>')
    branch_y = 140
    for index, node in enumerate(non_stage_nodes):
        y = branch_y + (index * 84)
        x = 120 if node["kind"] == "branch" else 420 if node["kind"] == "gate" else 720
        width = 260 if node["kind"] == "branch" else 250
        fill = "#172231" if not node.get("isBlocked") else "#3b1f25"
        stroke = "#4f86c6" if node.get("isWinningPath") else "#607d9b"
        if node["kind"] == "reentry":
            stroke = "#4cae8a"
        svg_parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="60" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        svg_parts.append(f'<text x="{x + 10}" y="{y + 18}" fill="#f4f7fb" font-size="12" font-family="Segoe UI, Arial, sans-serif">{html_escape(node["title"])}</text>')
        svg_parts.append(f'<text x="{x + 10}" y="{y + 35}" fill="#c7d8eb" font-size="10" font-family="Segoe UI, Arial, sans-serif">{html_escape(node["pathType"])}</text>')
        svg_parts.append(f'<text x="{x + 10}" y="{y + 50}" fill="#c7d8eb" font-size="10" font-family="Segoe UI, Arial, sans-serif">{html_escape(node["summary"][:72])}</text>')
    svg_parts.append("</svg>")
    return "".join(svg_parts)


def _render_journey_html(record: dict[str, Any], journey_view: dict[str, Any]) -> str:
    gate_card = journey_view["gateCard"]
    warnings_html = ""
    if journey_view["derivationWarnings"]:
        warnings_html = "\n".join(
            [
                "<details class=\"warnings\">",
                "<summary>Derivation warnings</summary>",
                "<ul>",
                *[f"<li>{html_escape(item)}</li>" for item in journey_view["derivationWarnings"]],
                "</ul>",
                "</details>",
            ]
        )
    node_items = []
    for node in sorted(journey_view["journey"]["nodes"], key=lambda item: (item.get("displayOrder") or 0, item["id"])):
        badges = []
        if node.get("isCurrent"):
            badges.append("current")
        if node.get("isWinningPath"):
            badges.append("winning")
        if node.get("isBlocked"):
            badges.append("blocked")
        badge_text = " | ".join(badges) if badges else node["status"]
        node_items.append(
            "\n".join(
                [
                    "<details class=\"node-card\">",
                    f"<summary>{html_escape(node['title'])} <span>{html_escape(badge_text)}</span></summary>",
                    f"<p>{html_escape(node['summary'])}</p>",
                    "<ul>",
                    f"<li>Stage: <code>{html_escape(node['stage'])}</code></li>",
                    f"<li>Path type: <code>{html_escape(node['pathType'])}</code></li>",
                    f"<li>Decision: <code>{html_escape(str(node['decision']))}</code></li>",
                    f"<li>Next action: {html_escape(node.get('nextAction') or 'None recorded.')}</li>",
                    f"<li>Resume at: <code>{html_escape(node.get('resumeStage') or 'none')}</code></li>",
                    "</ul>",
                    "</details>",
                ]
            )
        )
    return "\n".join(
        [
            "<!DOCTYPE html>",
            "<html lang=\"en\">",
            "<head>",
            "<meta charset=\"utf-8\" />",
            f"<title>{html_escape(report_title(record['mode']))} Journey View</title>",
            "<style>",
            "body{background:#0b0f14;color:#eef4fb;font-family:Segoe UI,Arial,sans-serif;margin:0;padding:24px;line-height:1.45}",
            ".wrap{max-width:1100px;margin:0 auto}",
            ".top{display:grid;grid-template-columns:2fr 1fr;gap:20px;align-items:start}",
            ".card{background:#111826;border:1px solid #243549;border-radius:14px;padding:16px}",
            "h1,h2,h3{margin:0 0 12px 0}",
            ".strip{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 18px 0}",
            ".pill{background:#192536;border:1px solid #34506c;border-radius:999px;padding:6px 10px;font-size:12px}",
            "code{color:#d8f0ff}",
            "a{color:#9ac7ff}",
            ".warnings summary,.node-card summary{cursor:pointer;font-weight:600}",
            ".node-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}",
            ".node-card{background:#0f1520;border:1px solid #2a3d52;border-radius:12px;padding:12px}",
            ".gate-list,.link-list{padding-left:18px}",
            "@media (max-width: 900px){.top,.node-grid{grid-template-columns:1fr}}",
            "</style>",
            "</head>",
            "<body>",
            "<div class=\"wrap\">",
            f"<h1>{html_escape(report_title(record['mode']))} Journey View</h1>",
            "<p>This visual surface is derived from the governed run artifacts and is intended to make the agent-team and harness progression easier to understand.</p>",
            "<div class=\"strip\">",
            f"<span class=\"pill\">Recommendation: <strong>{html_escape(record['decision'])}</strong></span>",
            f"<span class=\"pill\">Confidence: <strong>{html_escape(record['confidenceBand'])}</strong></span>",
            f"<span class=\"pill\">Current stage: <strong>{html_escape(record['workflowState']['currentStage'])}</strong></span>",
            f"<span class=\"pill\">Compact view: <strong>{'Yes' if journey_view['isCompact'] else 'No'}</strong></span>",
            "</div>",
            warnings_html,
            "<div class=\"top\">",
            "<section class=\"card\">",
            "<h2>Lifecycle And Branch Journey</h2>",
            _render_journey_svg(journey_view),
            "</section>",
            "<aside class=\"card\">",
            "<h2>Gate Card</h2>",
            "<ul class=\"gate-list\">",
            f"<li>Final recommendation: <code>{html_escape(gate_card['finalRecommendation'])}</code></li>",
            f"<li>Approval status: <code>{html_escape(gate_card['approvalStatus'])}</code></li>",
            f"<li>Gate status: <code>{html_escape(gate_card['gateStatus'])}</code></li>",
            f"<li>Boundary status: <code>{html_escape(gate_card.get('boundaryStatus') or 'clean')}</code></li>",
            f"<li>Blocked by: {html_escape(gate_card['blockerPrecedence'])}</li>",
            f"<li>Allowed next stage: <code>{html_escape(str(gate_card['allowedNextStage']))}</code></li>",
            f"<li>Decision owner: {html_escape(gate_card['decisionOwner'])}</li>",
            f"<li>Next owner: {html_escape(gate_card['nextOwner'])}</li>",
            f"<li>Current action: {html_escape(gate_card.get('currentAction') or 'None recorded.')}</li>",
            f"<li>Confirmation reason: {html_escape(gate_card.get('confirmationReason') or 'None recorded.')}</li>",
            f"<li>Resume guidance: {html_escape(gate_card['resumeGuidance'])}</li>",
            "</ul>",
            "</aside>",
            "</div>",
            "<section class=\"card\" style=\"margin-top:20px\">",
            "<h2>Node Details</h2>",
            "<div class=\"node-grid\">",
            *node_items,
            "</div>",
            "</section>",
            "<section class=\"card\" style=\"margin-top:20px\">",
            "<h2>Source Artifacts</h2>",
            "<ul class=\"link-list\">",
            f"<li><a href=\"{html_escape(record['artifacts']['runRecord'])}\">Run record</a></li>",
            f"<li><a href=\"{html_escape(record['artifacts']['approvals'])}\">Approvals</a></li>",
            f"<li><a href=\"{html_escape(record['artifacts']['deliberation'])}\">Deliberation</a></li>",
            f"<li><a href=\"{html_escape(record['artifacts']['summaryStandard'])}\">Standard summary</a></li>",
            f"<li><a href=\"{html_escape(record['artifacts']['summaryExec'])}\">Executive summary</a></li>",
            "</ul>",
            "</section>",
            "</div>",
            "</body>",
            "</html>",
        ]
    )


def _render_start_here(record: dict[str, Any], mode: str) -> str:
    return "\n".join(
        [
            f"# {report_title(mode)} Start Here",
            "",
            f"- Run ID: {record['runId']}",
            f"- Recommendation: `{record['decision']}`",
            f"- Confidence: `{record['confidenceBand']}`",
            f"- Current stage: `{record['workflowState']['currentStage']}`",
            f"- Next stage: `{record['workflowState']['nextStage']}`",
            f"- Gate status: `{record['workflowState']['gateStatus']}`",
            f"- Assess entry status: `{record['workflowState']['assessEntryStatus']}`",
            f"- Deliberate handoff status: `{record['workflowState']['deliberateHandoffStatus']}`",
            f"- Boundary status: `{record['runtimeState']['boundaryStatus']}`",
            f"- Human escalation required: `{'Yes' if record['deliberation']['overrideModel']['humanEscalationRequired'] else 'No'}`",
            "",
            "## What To Read First",
            "",
            f"- [Journey view]({record['artifacts']['journeyView']})",
            f"- [Standard summary]({record['artifacts']['summaryStandard']})",
            f"- [Executive summary]({record['artifacts']['summaryExec']})",
            f"- [Risk register]({record['artifacts']['riskRegister']})",
            f"- [Approvals]({record['artifacts']['approvals']})",
            "",
            "## Next Action",
            "",
            f"- {_next_action_summary(record)}",
            *[f"- {item}" for item in _next_action_items(record)],
            "",
            "## Continue Or Resume",
            "",
            f"- Proceed allowed: `{'Yes' if record['runtimeState']['proceedAllowed'] else 'No'}`",
            f"- Confirmation required: `{'Yes' if record['runtimeState']['confirmationRequired'] else 'No'}`",
            f"- Confirmation reason: {record['runtimeState']['confirmationReason']}",
            f"- Resume guidance: {record['runtimeState']['resumeGuidance']}",
            *[f"- Blocker: {item}" for item in record["runtimeState"]["proceedBlockers"]],
            "",
            "## Runtime Surface",
            "",
            f"- [Run record]({record['artifacts']['runRecord']})",
            f"- [Deliberation]({record['artifacts']['deliberation']})",
            f"- [Evidence index]({record['artifacts']['evidenceIndex']})",
            "",
            "## Key Point Summary",
            "",
            "- Open this file first when reviewing a new run folder.",
        ]
    )


def _render_markdown(record: dict[str, Any], mode: str) -> dict[str, str]:
    title = report_title(mode)
    rid = record["runId"]
    decision = record["decision"]
    confidence = record["confidenceBand"]
    created_text = _display_timestamp(record.get("createdAt"))
    updated_text = _display_timestamp(record.get("updatedAt"))
    run_status_lines = [
        f"- Current stage: `{record['workflowState']['currentStage']}`",
        f"- Next stage: `{record['workflowState']['nextStage']}`",
        f"- Gate status: `{record['workflowState']['gateStatus']}`",
        f"- Assess entry status: `{record['workflowState']['assessEntryStatus']}`",
        f"- Deliberate handoff status: `{record['workflowState']['deliberateHandoffStatus']}`",
        f"- Boundary status: `{record['runtimeState']['boundaryStatus']}`",
        f"- Trace status: `{record['runtimeState']['traceStatus']}`",
        f"- Active exception rule: `{record['workflowState']['activeExceptionRule'] or 'none'}`",
    ]
    approval_posture_lines = [
        f"- Approval posture: `{record['runtimeState']['approvalPosture']}`",
        f"- Human escalation required: `{'Yes' if record['deliberation']['overrideModel']['humanEscalationRequired'] else 'No'}`",
        f"- Current recommendation handling: `{_approval_recommendation(record)}`",
    ]
    return {
        "summary-short.md": "\n".join(
            [
                f"# {title}",
                "",
                f"- Run ID: {rid}",
                f"- Created: {created_text}",
                f"- Updated: {updated_text}",
                f"- Mode: {mode}",
                f"- Recommendation: {decision}",
                f"- Confidence: {confidence}",
                "",
                "## Recommendation Snapshot",
                "",
                "- Add the shortest possible decision statement here.",
                f"- Runtime boundary: [{record['runtimeAssets']['boundaryPanel']['name']}]({record['runtimeAssets']['boundaryPanel']['path']}).",
                "",
                "## Run Status",
                "",
                *run_status_lines,
                "",
                "## Approval Posture",
                "",
                *approval_posture_lines,
                "",
                "## Assessment Scope",
                "",
                "- Record what artifact bundle and decision horizon were assessed.",
                "",
                "## Top Concerns",
                "",
                "- Add evidence-backed bullets here.",
                "",
                "## Next Action",
                "",
                f"- Next action summary: {_next_action_summary(record)}",
                *[f"- {item}" for item in _next_action_items(record)],
                "",
                "## Continue Or Resume",
                "",
                f"- Proceed allowed: `{'Yes' if record['runtimeState']['proceedAllowed'] else 'No'}`",
                f"- Confirmation required: `{'Yes' if record['runtimeState']['confirmationRequired'] else 'No'}`",
                f"- Confirmation reason: {record['runtimeState']['confirmationReason']}",
                f"- Resume guidance: {record['runtimeState']['resumeGuidance']}",
                *[f"- Blocker: {item}" for item in record["runtimeState"]["proceedBlockers"]],
                "",
                "## Key Point Summary",
                "",
                "- Keep this section short and easy to scan.",
            ]
        ),
        "summary-standard.md": "\n".join(
            [
                f"# {title}",
                "",
                f"- Run ID: {rid}",
                f"- Created: {created_text}",
                f"- Updated: {updated_text}",
                f"- Mode: {mode}",
                f"- Recommendation: {decision}",
                f"- Confidence: {confidence}",
                "",
                "## Recommendation Snapshot",
                "",
                "- Add the top-line judgment here.",
                "",
                "## Run Status",
                "",
                *run_status_lines,
                "",
                "## Approval Posture",
                "",
                *approval_posture_lines,
                "",
                "## Assessment Scope And Decision Window",
                "",
                "- Record the inspected artifact boundary and the decision horizon.",
                f"- Workflow lifecycle: [{record['workflowAssets']['lifecycleMap']['name']}]({record['workflowAssets']['lifecycleMap']['path']}).",
                "",
                "## Decision Owner And Required Action",
                "",
                "- Record who must accept, escalate, or delay the decision.",
                "",
                "## Top Blockers Or Concerns",
                "",
                "- Add detailed bullet points here.",
                "",
                "## Mitigation Path",
                "",
                "- Add recommended mitigation steps here.",
                "",
                "## Confidence And Evidence Note",
                "",
                f"- Governed by: [{record['governanceAssets']['prompt']['name']}]({record['governanceAssets']['prompt']['path']}) and [{record['governanceAssets']['overlay']['name']}]({record['governanceAssets']['overlay']['path']}).",
                "- Explain evidence quality and any important uncertainty.",
                "",
                "## Residual Risk Note",
                "",
                "- Explain the expected residual risk if the listed mitigations are completed.",
                "",
                "## Next Action",
                "",
                f"- Next action summary: {_next_action_summary(record)}",
                *[f"- {item}" for item in _next_action_items(record)],
                "",
                "## Continue Or Resume",
                "",
                f"- Proceed allowed: `{'Yes' if record['runtimeState']['proceedAllowed'] else 'No'}`",
                f"- Confirmation required: `{'Yes' if record['runtimeState']['confirmationRequired'] else 'No'}`",
                f"- Confirmation reason: {record['runtimeState']['confirmationReason']}",
                f"- Resume guidance: {record['runtimeState']['resumeGuidance']}",
                *[f"- Blocker: {item}" for item in record["runtimeState"]["proceedBlockers"]],
                "",
                "## Key Point Summary",
                "",
                f"- Governed template: [{record['governanceAssets']['template']['name']}]({record['governanceAssets']['template']['path']}).",
                "- End with the shortest possible decision summary.",
            ]
        ),
        "summary-exec.md": "\n".join(
            [
                f"# {title}",
                "",
                f"- Run ID: {rid}",
                f"- Created: {created_text}",
                f"- Recommendation: {decision}",
                f"- Confidence: {confidence}",
                "",
                "## Architecture Recommendation" if mode == "architecture-validation" else "## Release Recommendation",
                "",
                "- Add the executive-facing architecture recommendation here." if mode == "architecture-validation" else "- Add the executive-facing release recommendation here.",
                "",
                "## Run Status",
                "",
                f"- Current stage: `{record['workflowState']['currentStage']}`",
                f"- Next stage: `{record['workflowState']['nextStage']}`",
                f"- Gate status: `{record['workflowState']['gateStatus']}`",
                f"- Assess entry status: `{record['workflowState']['assessEntryStatus']}`",
                f"- Deliberate handoff status: `{record['workflowState']['deliberateHandoffStatus']}`",
                f"- Boundary status: `{record['runtimeState']['boundaryStatus']}`",
                f"- Trace status: `{record['runtimeState']['traceStatus']}`",
                "",
                "## Decision Required",
                "",
                "- Record who must accept, escalate, or defer the decision.",
                f"- Active runtime factsheet: [{record['runtimeAssets']['governedRunFactsheet']['name']}]({record['runtimeAssets']['governedRunFactsheet']['path']}).",
                "",
                "## Top Blockers",
                "",
                "- Add the most important blockers or concerns here.",
                "",
                "## Mitigation Path",
                "",
                "- Add the executive-facing mitigation path here.",
                "",
                "## Proceed Conditions",
                "",
                "- Record what must be true before proceeding.",
                "",
                "## Residual Risk If Proceeding",
                "",
                "- Summarize the expected residual risk after mitigations.",
                "",
                "## Next Action",
                "",
                f"- Next action summary: {_next_action_summary(record)}",
                *[f"- {item}" for item in _next_action_items(record)],
                "",
                "## Continue Or Resume",
                "",
                f"- Proceed allowed: `{'Yes' if record['runtimeState']['proceedAllowed'] else 'No'}`",
                f"- Confirmation required: `{'Yes' if record['runtimeState']['confirmationRequired'] else 'No'}`",
                f"- Confirmation reason: {record['runtimeState']['confirmationReason']}",
                f"- Resume guidance: {record['runtimeState']['resumeGuidance']}",
                *[f"- Blocker: {item}" for item in record["runtimeState"]["proceedBlockers"]],
                "",
                "## Key Point Summary",
                "",
                "- Keep this section brief.",
            ]
        ),
        "risk-register.md": "\n".join(
            [
                "# PreMortemX Architecture Risk Register" if mode == "architecture-validation" else "# PreMortemX Risk Register",
                "",
                f"- Run ID: {rid}",
                f"- Created: {created_text}",
                "",
                "## Scope Reviewed",
                "",
                "- List the inspected design, architecture, code, release, and test artifacts.",
                f"- Workflow handoff contract: [{record['workflowAssets']['handoffs'][0]['name']}]({record['workflowAssets']['handoffs'][0]['path']}).",
                "",
                "## Detailed Risks",
                "",
                "- `R-01`",
                "  Cause-event-impact: because X, Y may happen, leading to Z impact.",
                "  Likelihood: ``",
                "  Impact: ``",
                "  Current risk: ``",
                "  Residual risk after mitigation: ``",
                "  Response: ``",
                "  Risk owner: ``",
                "  Treatment owner: ``",
                "  Status: ``",
                "  Review date: ``",
                "  Evidence refs: ``",
                "",
                "## Evidence References",
                "",
                "- `EV-01`: artifact, section, freshness, and trust note.",
                "",
                "## Mitigations",
                "",
                "- `R-01`: add mitigation actions here.",
                "",
                "## Unresolved Assumptions",
                "",
                "- Record material uncertainty here.",
                "",
                "## Key Point Summary",
                "",
                "- Keep this section brief and scannable.",
            ]
        ),
        "evidence-index.md": "\n".join(
            [
                "# Evidence Index",
                "",
                f"- Run ID: {rid}",
                "",
                "## Sources",
                "",
                "- `EV-01` | evidence type | artifact | owner/source | freshness | trust level | supports finding IDs | direct / inferred / missing",
            ]
        ),
    }


def _write_markdown_artifacts(run_dir: Path, record: dict[str, Any], mode: str) -> None:
    for name, content in _render_markdown(record, mode).items():
        _write(run_dir / name, content)
    _write(run_dir / "start-here.md", _render_start_here(record, mode))


def _write_journey_artifacts(run_dir: Path, record: dict[str, Any]) -> None:
    journey_view = _derive_journey_view(record)
    _write_json(run_dir / "journey-view.json", journey_view)
    _write(run_dir / "journey-view.html", _render_journey_html(record, journey_view))


def create_run(
    plugin_root: str | Path,
    project_slug: str,
    mode: str = "release-risk-gating",
    decision: str = "Warn",
    confidence_band_value: str = "Medium",
) -> dict[str, Any]:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"Invalid mode: {mode}")
    if decision not in ALLOWED_DECISIONS:
        raise ValueError(f"Invalid decision: {decision}")
    root = Path(plugin_root)
    now = utc_now()
    rid = run_id(project_slug, now)
    run_dir = root / "runs" / now.strftime("%Y") / now.strftime("%m") / rid
    ensure_dir(run_dir)

    record = default_record(root, project_slug, mode, decision, confidence_band_value, now, run_dir)
    record["runId"] = rid
    record["registryRefs"]["indexKey"] = f"{now.strftime('%Y-%m')}/{rid}"
    record["artifactPath"] = f"runs/{now.strftime('%Y')}/{now.strftime('%m')}/{rid}"

    _write_json(run_dir / "run-record.json", record)
    _write_markdown_artifacts(run_dir, record, mode)
    _write_journey_artifacts(run_dir, record)

    _write_json(
        run_dir / "analysis.json",
        {
            "generatedAt": record["createdAt"],
            "notes": [
                "Structured internal analysis output belongs here.",
                "Keep machine-oriented reasoning concise and auditable.",
            ],
            "decisionContext": {
                "decisionOwner": None,
                "decisionWindow": None,
                "scopeBoundary": None,
                "recommendedAction": None,
            },
            "findings": [
                {
                    "id": "R-01",
                    "title": "Add concise finding title here.",
                    "likelihood": None,
                    "impact": None,
                    "currentRisk": None,
                    "residualRisk": None,
                    "evidenceStrength": None,
                    "response": None,
                    "riskOwner": None,
                    "treatmentOwner": None,
                    "reviewDate": None,
                    "evidenceRefs": [],
                    "summary": "Add concise machine-readable finding summary here.",
                }
            ],
        },
    )
    _write_json(run_dir / "deliberation.json", record["deliberation"])
    _write_json(run_dir / "approvals.json", _approvals_payload(record))
    _write_json(
        run_dir / "retention.json",
        {
            "likelySensitive": False,
            "recommendation": "none",
            "encryptionDecision": "not-requested",
            "contextContract": record["runtimeAssets"]["contextContract"],
            "notes": ["Retention and sensitivity decisions belong here."],
        },
    )
    quality_log_path = root / "registry" / "quality-review-log.json"
    ensure_dir(quality_log_path.parent)
    if not quality_log_path.exists():
        _write_json(quality_log_path, {"items": []})

    return {
        "RunId": rid,
        "RunPath": str(run_dir),
        "RecordPath": str(run_dir / "run-record.json"),
    }


def _require_fields(record: dict[str, Any], fields: list[str]) -> None:
    for field in fields:
        if field not in record:
            raise ValueError(f"Missing required field '{field}' in run record.")


def validate_run_record(run_record_path: str | Path) -> dict[str, Any]:
    path = Path(run_record_path)
    if not path.exists():
        raise FileNotFoundError(f"Run record not found: {path}")
    record = json.loads(path.read_text(encoding="utf-8"))
    _require_fields(
        record,
        [
            "schemaVersion", "runId", "pluginVersion", "createdAt", "updatedAt", "status",
            "projectSlug", "taskType", "taskCategory", "executionMode", "approvalMode",
            "privacyMode", "retentionClass", "artifactPath", "registryRefs", "governanceAssets", "workflowAssets", "runtimeAssets", "workflowState", "runtimeState",
            "inputFingerprint", "mode", "decision", "confidenceBand", "inspectedInputs",
            "riskSummary", "calibrationState", "executionBoundary", "deliberation",
            "outputTiers", "permissionEscalationsRequested", "permissionEscalationsApproved",
            "guardrailRecommendations", "override", "sensitivityReview", "artifacts",
            "qualityFollowup",
        ],
    )
    _require_fields(record["governanceAssets"], ["version", "prompt", "overlay", "policyPack", "template", "roleCards", "controlCards"])
    _require_fields(record["workflowAssets"], ["version", "lifecycleMap", "stageDefinitions", "approvalPlaybooks", "handoffs", "exceptionRules", "modeBinding"])
    _require_fields(record["runtimeAssets"], ["version", "controlTowerView", "governedRunFactsheet", "boundaryPanel", "policyResolverRecord", "contextContract", "runtimeTraceSummary", "modeBinding"])
    _require_fields(record["workflowState"], ["lifecycle", "currentStage", "completedStages", "nextStage", "pendingApprovalPlaybook", "activeExceptionRule", "assessEntryStatus", "assessEntryBlockers", "deliberateHandoffStatus", "handoffBlockers", "gateStatus", "allowedNextStage", "blockedBy"])
    _require_fields(record["runtimeState"], ["activePolicyProfile", "runtimeMode", "approvalPosture", "allowedEvidenceClasses", "boundaryStatus", "blockedContextClasses", "carryForwardAllowed", "transformationStatus", "carryForwardLedger", "trustedInstructionSources", "openBreaches", "attentionItems", "traceStatus", "confirmationRequired", "confirmationReason", "resumeGuidance", "proceedAllowed", "proceedBlockers"])
    if not re.match(r"^pmx-[a-z0-9\-]+-\d{8}T\d{6}Z-[a-z0-9]{6}$", record["runId"]):
        raise ValueError(f"Run ID format is invalid: {record['runId']}")
    if record["decision"] not in ALLOWED_DECISIONS:
        raise ValueError("Decision must be one of: Pass, Warn, Block")
    if record["mode"] not in ALLOWED_MODES:
        raise ValueError("Mode must be one of: release-risk-gating, architecture-validation")
    if record["taskCategory"] not in ALLOWED_TASK_CATEGORIES:
        raise ValueError("Task category must be one of: risk-analysis, calibration")
    _require_fields(
        record["artifacts"],
        ["startHere", "journeyView", "journeyData", "summaryShort", "summaryStandard", "summaryExec", "riskRegister", "runRecord", "analysis", "approvals", "retention", "evidenceIndex", "deliberation"],
    )
    rubric = record["deliberation"]["rubric"]
    if rubric["gradingScale"] != "1-5":
        raise ValueError("Deliberation rubric grading scale must be '1-5'.")
    for field in ["confidence", "evidenceStrength", "riskSeverity", "evidenceCompleteness", "disagreementLevel", "policyFit", "decisionSensitivity"]:
        value = int(rubric[field])
        if value < 1 or value > 5:
            raise ValueError(f"Rubric field '{field}' must be within 1-5.")
    if record["calibrationState"]["promotionState"] not in ALLOWED_PROMOTION_STATES:
        raise ValueError("Promotion state must be one of: trusted, provisional, excluded")
    return {"Valid": True, "RunId": record["runId"], "Decision": record["decision"]}


def _new_default_specialist(role: str, decision: str) -> dict[str, Any]:
    return {
        "role": role,
        "recommendation": decision,
        "summary": f"{role} found no additional concerns beyond the current {decision} posture.",
        "evidenceRefs": [],
        "rubric": {
            "confidence": 3,
            "evidenceStrength": 3,
            "riskSeverity": 3,
            "evidenceCompleteness": 3,
            "disagreementLevel": 1,
            "policyFit": 3,
            "decisionSensitivity": 3,
        },
    }


def invoke_deliberation(run_record_path: str | Path, specialist_input_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(run_record_path)
    record = json.loads(path.read_text(encoding="utf-8"))
    run_dir = path.parent
    specialists: list[dict[str, Any]] = []

    if specialist_input_path:
        payload = json.loads(Path(specialist_input_path).read_text(encoding="utf-8"))
        specialists = list(payload.get("specialists", []))
        if payload.get("specialists") is None:
            raise ValueError("Specialist input must contain a 'specialists' array.")
    else:
        for role in record["deliberation"]["specialistRoles"]:
            specialists.append(_new_default_specialist(role, record["decision"]))

    if not specialists:
        raise ValueError("At least one specialist finding is required.")

    decision_groups = Counter(spec["recommendation"] for spec in specialists)
    consensus_decision = sorted(decision_groups.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    consensus_group = [s for s in specialists if s["recommendation"] == consensus_decision]
    minority_views = [s for s in specialists if s["recommendation"] != consensus_decision]

    def avg(field: str, specs: list[dict[str, Any]]) -> int:
        return round(sum(int(s["rubric"][field]) for s in specs) / len(specs))

    consensus_evidence_strength = avg("evidenceStrength", consensus_group)
    all_evidence_completeness = [int(s["rubric"]["evidenceCompleteness"]) for s in specialists]
    all_confidence = [int(s["rubric"]["confidence"]) for s in specialists]
    all_severity = [int(s["rubric"]["riskSeverity"]) for s in specialists]
    all_policy_fit = [int(s["rubric"]["policyFit"]) for s in specialists]
    all_sensitivity = [int(s["rubric"]["decisionSensitivity"]) for s in specialists]

    distinct_decisions = sorted(set(s["recommendation"] for s in specialists))
    disagreement_level = 1 if len(distinct_decisions) == 1 else (3 if len(distinct_decisions) == 2 else 5)
    final_decision = consensus_decision
    override_applied = False
    override_reason = None
    human_escalation_reasons: list[str] = []

    strongest_minority = None
    for minority in minority_views:
        if strongest_minority is None:
            strongest_minority = minority
            continue
        candidate_evidence = int(minority["rubric"]["evidenceStrength"])
        current_evidence = int(strongest_minority["rubric"]["evidenceStrength"])
        candidate_rank = decision_rank(minority["recommendation"])
        current_rank = decision_rank(strongest_minority["recommendation"])
        if candidate_evidence > current_evidence or (
            candidate_evidence == current_evidence and candidate_rank > current_rank
        ):
            strongest_minority = minority

    if strongest_minority is not None:
        minority_evidence = int(strongest_minority["rubric"]["evidenceStrength"])
        minority_rank = decision_rank(strongest_minority["recommendation"])
        consensus_rank = decision_rank(consensus_decision)
        if minority_evidence >= 4 and (minority_evidence - consensus_evidence_strength) >= 2 and minority_rank > consensus_rank:
            final_decision = strongest_minority["recommendation"]
            override_applied = True
            override_reason = "Evidence-gated override: minority specialist evidence materially exceeded the consensus evidence base."

    minimum_evidence_completeness = min(all_evidence_completeness)
    minimum_policy_fit = min(all_policy_fit)
    maximum_severity = max(all_severity)
    maximum_sensitivity = max(all_sensitivity)
    overall_confidence = round(sum(all_confidence) / len(all_confidence))

    if minimum_evidence_completeness <= 2 and decision_rank(final_decision) < 2:
        final_decision = "Warn"
        if not override_applied:
            override_applied = True
            override_reason = "Evidence-gated override: evidence completeness was too low to sustain a Pass."

    if disagreement_level >= 4 and overall_confidence <= 2 and decision_rank(final_decision) < 2:
        final_decision = "Warn"
        if not override_applied:
            override_applied = True
            override_reason = "Evidence-gated override: severe specialist disagreement and low confidence prevented a Pass."

    severe_views = [s for s in specialists if int(s["rubric"]["riskSeverity"]) >= 4 and int(s["rubric"]["evidenceStrength"]) >= 4]
    if maximum_severity >= 4 and severe_views:
        final_decision = "Block"
        if not override_applied or decision_rank(final_decision) > decision_rank(consensus_decision):
            override_applied = True
            override_reason = "Severity-and-policy override: a credible high-severity risk met the escalation threshold."

    if minimum_policy_fit <= 2 and decision_rank(final_decision) < 2:
        final_decision = "Warn"
        if not override_applied:
            override_applied = True
            override_reason = "Severity-and-policy override: policy fit was too weak to sustain a Pass."

    if maximum_sensitivity >= 4 and (minimum_evidence_completeness <= 2 or disagreement_level >= 4):
        human_escalation_reasons.append("High-sensitivity case retains unresolved uncertainty.")

    if len(record["permissionEscalationsRequested"]) > len(record["permissionEscalationsApproved"]):
        human_escalation_reasons.append("Permission broadening remains unresolved.")

    sorted_risk_views = sorted(
        specialists,
        key=lambda s: ((int(s["rubric"]["riskSeverity"]) * 10) + int(s["rubric"]["evidenceStrength"])),
        reverse=True,
    )
    top_risks = [
        {
            "role": s["role"],
            "recommendation": s["recommendation"],
            "summary": s["summary"],
            "evidenceRefs": list(s.get("evidenceRefs", [])),
        }
        for s in sorted_risk_views[:3]
    ]

    rule_triggered = (
        "severity-and-policy"
        if override_reason and override_reason.startswith("Severity-and-policy")
        else "evidence-gated"
        if override_reason and override_reason.startswith("Evidence-gated")
        else "consensus"
    )
    decision_path = [
        f"Consensus began at {consensus_decision} with disagreement level {disagreement_level}.",
        f"Overall confidence resolved to {overall_confidence} on the internal 1-5 scale.",
        f"Minimum evidence completeness resolved to {minimum_evidence_completeness} and minimum policy fit resolved to {minimum_policy_fit}.",
    ]
    if override_applied and override_reason:
        decision_path.append(f"Override path: {override_reason}")
    else:
        decision_path.append("No override applied; the adjudicated outcome remained aligned with the consensus decision.")

    uncertainty_drivers: list[str] = []
    if minimum_evidence_completeness <= 2:
        uncertainty_drivers.append("evidence completeness remained low")
    if disagreement_level >= 4:
        uncertainty_drivers.append("specialist disagreement remained high")
    if len(record["permissionEscalationsRequested"]) > len(record["permissionEscalationsApproved"]):
        uncertainty_drivers.append("permission broadening was unresolved")

    residual_risk = {"Pass": "Low", "Warn": "Low-Medium", "Block": "Medium"}[final_decision]

    record["deliberation"]["specialists"] = specialists
    record["deliberation"]["agreement"]["consensusDecision"] = consensus_decision
    record["deliberation"]["agreement"]["disagreementLevel"] = disagreement_level
    record["deliberation"]["agreement"]["summary"] = f"Consensus began at {consensus_decision} with disagreement level {disagreement_level}."
    record["deliberation"]["rubric"]["confidence"] = overall_confidence
    record["deliberation"]["rubric"]["evidenceStrength"] = round(sum(int(s["rubric"]["evidenceStrength"]) for s in specialists) / len(specialists))
    record["deliberation"]["rubric"]["riskSeverity"] = maximum_severity
    record["deliberation"]["rubric"]["evidenceCompleteness"] = minimum_evidence_completeness
    record["deliberation"]["rubric"]["disagreementLevel"] = disagreement_level
    record["deliberation"]["rubric"]["policyFit"] = minimum_policy_fit
    record["deliberation"]["rubric"]["decisionSensitivity"] = maximum_sensitivity
    record["deliberation"]["overrideModel"]["overrideApplied"] = override_applied
    record["deliberation"]["overrideModel"]["overrideReason"] = override_reason
    record["deliberation"]["overrideModel"]["humanEscalationRequired"] = bool(human_escalation_reasons)
    record["deliberation"]["overrideModel"]["humanEscalationReasons"] = human_escalation_reasons
    record["deliberation"]["overrideModel"]["overrideTestSummary"] = override_reason if override_applied and override_reason else "No override was applied because the consensus outcome remained acceptable under the configured rules."
    adjudication = record["deliberation"]["adjudication"]
    adjudication["finalDecision"] = final_decision
    adjudication["finalConfidenceBand"] = confidence_band(overall_confidence)
    adjudication["summary"] = override_reason if override_applied and override_reason else "Orchestrator adjudicated to the consensus outcome without override."
    adjudication["ruleTriggered"] = rule_triggered
    adjudication["humanEscalationConsidered"] = bool(human_escalation_reasons)
    adjudication["residualRiskAfterMitigation"] = residual_risk
    adjudication["decisionPath"] = decision_path
    adjudication["uncertaintyDrivers"] = uncertainty_drivers
    adjudication["supportingEvidence"] = [ref for risk in top_risks for ref in risk.get("evidenceRefs", []) if ref]

    record["deliberation"]["status"] = "completed"
    record["decision"] = final_decision
    record["confidenceBand"] = adjudication["finalConfidenceBand"]
    record["topRisks"] = top_risks
    record["workflowState"]["completedStages"] = ["Intake", "Assess", "Deliberate"]
    record["workflowState"]["currentStage"] = "Approve/Block"
    record["workflowState"]["nextStage"] = "Monitor" if final_decision in {"Pass", "Warn"} else "Revisit"
    record["workflowState"]["activeExceptionRule"] = (
        "Missing Evidence Re-entry Rule"
        if minimum_evidence_completeness <= 2
        else None
    )
    record["runtimeState"]["traceStatus"] = "completed"
    record["runtimeState"]["openBreaches"] = []
    if minimum_evidence_completeness <= 2:
        record["runtimeState"]["openBreaches"].append("Evidence completeness remained below the preferred threshold.")
    if final_decision == "Block":
        record["runtimeState"]["attentionItems"] = [
            "Escalate the blocked decision through the governed approval path.",
            "Resolve the evidence gap before the next revisit cycle.",
        ]
    elif final_decision == "Warn":
        record["runtimeState"]["attentionItems"] = [
            "Keep the monitored owner follow-up visible until residual risk is reduced."
        ]
    else:
        record["runtimeState"]["attentionItems"] = ["Continue standard monitoring for the approved path."]
    _refresh_derived_state(record)
    record["updatedAt"] = utc_now().isoformat().replace("+00:00", "Z")

    _write_json(path, record)
    _write_markdown_artifacts(run_dir, record, record["mode"])
    _write_journey_artifacts(run_dir, record)
    _write_json(run_dir / "deliberation.json", record["deliberation"])
    _write_json(run_dir / "approvals.json", _approvals_payload(record))
    return {
        "runId": record["runId"],
        "finalDecision": record["decision"],
        "finalConfidenceBand": record["confidenceBand"],
        "overrideApplied": override_applied,
        "humanEscalationRequired": bool(human_escalation_reasons),
    }
