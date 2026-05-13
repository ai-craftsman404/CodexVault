from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


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


def main() -> None:
    tests_run = 0

    code, output = run_script("New-PreMortemXRun.py", "--ProjectSlug", "operator-surface", "--Decision", "Warn")
    assert_true(code == 0, f"Operator-surface run initialization should succeed.\n{output}")
    created = json.loads(output)
    run_path = Path(created["RunPath"])
    record_path = Path(created["RecordPath"])

    try:
        start_here = (run_path / "start-here.md").read_text(encoding="utf-8")
        summary_short = (run_path / "summary-short.md").read_text(encoding="utf-8")
        summary_standard = (run_path / "summary-standard.md").read_text(encoding="utf-8")
        summary_exec = (run_path / "summary-exec.md").read_text(encoding="utf-8")

        assert_true("# PreMortemX Release Assessment Start Here" in start_here, "Start-here should be the run-folder landing file.")
        assert_true("## What To Read First" in start_here, "Start-here should guide the reading order.")
        assert_true("[Standard summary](summary-standard.md)" in start_here, "Start-here should link to the standard summary.")
        assert_true("## Next Action" in start_here, "Start-here should surface next action guidance.")
        assert_true("## Continue Or Resume" in start_here, "Start-here should surface continue or resume guidance.")
        assert_true("Confirmation required: `Yes`" in start_here, "Start-here should show confirmation requirement.")
        assert_true("Proceed allowed: `No`" in start_here, "Start-here should show blocked progression when confirmation is still required.")
        assert_true("Assess entry status: `ready`" in start_here, "Start-here should show assess entry status.")
        assert_true("Deliberate handoff status: `pending-assess`" in start_here, "Start-here should show deliberate handoff status.")
        assert_true("Boundary status: `clean`" in start_here, "Start-here should show the boundary status.")
        tests_run += 1

        assert_true("## Run Status" in summary_short, "Short summary should show run status.")
        assert_true("## Approval Posture" in summary_short, "Short summary should show approval posture.")
        assert_true("## Next Action" in summary_short, "Short summary should show next action.")
        assert_true("## Continue Or Resume" in summary_short, "Short summary should show continue or resume guidance.")
        assert_true("Assess entry status: `ready`" in summary_short, "Short summary should show assess entry status.")
        assert_true("Deliberate handoff status: `pending-assess`" in summary_short, "Short summary should show deliberate handoff status.")
        assert_true("Boundary status: `clean`" in summary_short, "Short summary should show the boundary status.")
        assert_true("## Run Status" in summary_standard, "Standard summary should show run status.")
        assert_true("## Approval Posture" in summary_standard, "Standard summary should show approval posture.")
        assert_true("## Next Action" in summary_standard, "Standard summary should show next action.")
        assert_true("## Continue Or Resume" in summary_standard, "Standard summary should show continue or resume guidance.")
        assert_true("## Next Action" in summary_exec, "Exec summary should show next action.")
        assert_true("## Continue Or Resume" in summary_exec, "Exec summary should show continue or resume guidance.")
        assert_true("Boundary status: `clean`" in summary_exec, "Exec summary should show boundary status.")
        tests_run += 1

        specialist_input = run_path / "specialists-operator-surface.json"
        specialist_input.write_text(
            json.dumps(
                {
                    "specialists": [
                        {
                            "role": "Domain Risk Specialist",
                            "recommendation": "Warn",
                            "summary": "The rollout has meaningful unresolved delivery uncertainty.",
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
                            "summary": "Operational controls are mostly manageable.",
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
                            "summary": "Sensitive evidence controls are not strong enough.",
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
        assert_true(code == 0, f"Operator-surface deliberation should succeed.\n{output}")
        payload = json.loads(output)
        assert_true(payload["finalDecision"] == "Block", "Operator-surface case should reach Block.")
        tests_run += 1

        start_here_after = (run_path / "start-here.md").read_text(encoding="utf-8")
        summary_short_after = (run_path / "summary-short.md").read_text(encoding="utf-8")
        summary_standard_after = (run_path / "summary-standard.md").read_text(encoding="utf-8")
        summary_exec_after = (run_path / "summary-exec.md").read_text(encoding="utf-8")

        assert_true("Current stage: `Approve/Block`" in start_here_after, "Start-here should refresh the current stage.")
        assert_true("Assess entry status: `ready`" in start_here_after, "Start-here should preserve assess entry status after deliberation.")
        assert_true("Deliberate handoff status: `ready`" in start_here_after, "Start-here should refresh deliberate handoff status after deliberation.")
        assert_true("Boundary status: `clean`" in start_here_after, "Start-here should keep the boundary status visible after deliberation.")
        assert_true("Human escalation required: `Yes`" in start_here_after, "Start-here should refresh escalation posture.")
        assert_true("Resume guidance: Resume from `Revisit` after resolving the active exception rule." in start_here_after, "Start-here should refresh resume guidance.")
        assert_true("Proceed allowed: `No`" in start_here_after, "Start-here should keep progression blocked after a Block decision.")
        assert_true("- Escalate the current decision before the run can return for revisit." in start_here_after, "Start-here should align next action summary with the governed current action.")
        assert_true("Next action summary: Escalate the current decision before the run can return for revisit." in summary_short_after, "Short summary should refresh next action guidance.")
        assert_true("Trace status: `completed`" in summary_short_after, "Short summary should refresh trace status.")
        assert_true("Assess entry status: `ready`" in summary_short_after, "Short summary should preserve assess entry status after deliberation.")
        assert_true("Deliberate handoff status: `ready`" in summary_short_after, "Short summary should refresh deliberate handoff status after deliberation.")
        assert_true("Boundary status: `clean`" in summary_short_after, "Short summary should keep the boundary status visible after deliberation.")
        assert_true("Confirmation reason: Human escalation is required before the workflow can proceed." in summary_short_after, "Short summary should refresh confirmation reason.")
        assert_true("Blocker: An active exception rule must be resolved before proceeding." in summary_short_after, "Short summary should show the active exception blocker.")
        assert_true("Human escalation required: `Yes`" in summary_standard_after, "Standard summary should refresh escalation posture.")
        assert_true("Next action summary: Escalate the current decision before the run can return for revisit." in summary_standard_after, "Standard summary should refresh next action guidance.")
        assert_true("Resume guidance: Resume from `Revisit` after resolving the active exception rule." in summary_standard_after, "Standard summary should refresh resume guidance.")
        assert_true("Next action summary: Escalate the current decision before the run can return for revisit." in summary_exec_after, "Exec summary should refresh next action guidance.")
        assert_true("Confirmation reason: Human escalation is required before the workflow can proceed." in summary_exec_after, "Exec summary should refresh confirmation reason.")
        assert_true("Boundary status: `clean`" in summary_exec_after, "Exec summary should preserve boundary status after deliberation.")
        tests_run += 1

    finally:
        if run_path.exists():
            shutil.rmtree(run_path)

    print(f"PreMortemX operator-surface tests passed: {tests_run}")


if __name__ == "__main__":
    main()
