from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "codexvault.py"
sys.path.insert(0, str(ROOT))
import codexvault as cvx  # noqa: E402


def run_cli(*args: str, cwd: Path | None = None) -> dict:
    proc = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=str(cwd or ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


class CodexVaultCLITests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.project_a = self._make_project("alpha")
        self.project_b = self._make_project("beta")

    def _make_project(self, name: str) -> Path:
        project = self.root / "plugins" / name
        (project / ".codex-plugin").mkdir(parents=True)
        (project / ".codex-plugin" / "plugin.json").write_text('{"name":"codexvault"}', encoding="utf-8")
        (project / "README.md").write_text(f"# {name}\n", encoding="utf-8")
        (project / "notes.json").write_text('{"hello":"world"}', encoding="utf-8")
        (project / "scripts").mkdir()
        (project / "scripts" / "run.sh").write_text("echo hi\n", encoding="utf-8")
        return project

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_discover_manifest_snapshot_plan_verify_simulate(self) -> None:
        discovery = run_cli("discover", "--workspace", str(self.project_a))
        self.assertEqual(discovery["status"], "discovered")
        self.assertIn("adapter", discovery)
        self.assertIn("platform", discovery)
        self.assertIn("assetDependencyGraph", discovery)

        manifest_envelope = run_cli("manifest", "--discovery", json.dumps(discovery), "--workspace", str(self.project_a))
        manifest = manifest_envelope["manifest"]
        self.assertEqual(manifest["schemaVersion"], "v1b")
        self.assertTrue(manifest["workspaceId"])
        self.assertIn("normalizedDiscovery", manifest)
        self.assertIn("assetClassification", manifest)
        self.assertIn("riskSummary", manifest)

        snapshot = run_cli("snapshot", "--manifest", json.dumps(manifest), "--workspace", str(self.project_a))
        self.assertEqual(snapshot["checksumAlgorithm"], "SHA-256")
        archive = Path(snapshot["archivePath"])
        self.assertTrue(archive.exists())

        sidecar = archive.with_name(archive.name + ".sha256.json")
        self.assertTrue(sidecar.exists())

        with zipfile.ZipFile(archive, "r") as zf:
            names = set(zf.namelist())
        self.assertIn("README.md", names)
        self.assertIn("notes.json", names)

        plan = run_cli("plan", "--manifest", json.dumps(manifest), "--workspace", str(self.project_a))
        self.assertTrue(plan["plan"]["approvalRequired"])
        self.assertIn("validate archive", plan["plan"]["checkpoints"])
        self.assertIn("compatibility", plan["plan"])

        report = run_cli("verify", "--plan", json.dumps(plan["plan"]), "--workspace", str(self.project_a))
        self.assertIn(report["report"]["validationStatus"], {"validated", "validated-with-warnings"})
        self.assertIn("restore compatibility remains advisory only", report["report"]["reasons"])

        simulation = run_cli("simulate", "--scenario", json.dumps({"workspacePath": str(self.project_a)}), "--workspace", str(self.project_a))
        self.assertEqual(simulation["cleanupStatus"], "cleaned")
        self.assertTrue(simulation["adjudication"]["decision"])
        self.assertIn("mappingEvidence", simulation)
        self.assertEqual(simulation["mappingEvidence"]["status"], "reviewed")

    def test_backup_command_scans_all_projects_under_root(self) -> None:
        summary = run_cli("backup", "--workspace-root", str(self.root))
        self.assertEqual(summary["headline"], "Backup complete")
        self.assertIn("2 project(s) backed up", summary["status"])
        self.assertEqual(len(summary["projects"]), 2)
        self.assertEqual(summary["projects"][0]["checksumAlgorithm"], "SHA-256")
        self.assertEqual(summary["projects"][1]["simulationCleanup"], "cleaned")
        self.assertIn("mappingConfidence", summary["projects"][0])
        self.assertIn("mappingStatus", summary["projects"][0])
        self.assertEqual(summary["projects"][0]["mappingStatus"], "reviewed")

    def test_backup_dry_run_previews_full_workflow_without_artifacts(self) -> None:
        summary = run_cli("backup", "--workspace-root", str(self.root), "--dry-run")
        self.assertEqual(summary["headline"], "Backup dry run complete")
        self.assertIn("previewed", summary["status"])
        self.assertEqual(len(summary["projects"]), 2)
        first = summary["projects"][0]
        self.assertEqual(first["mode"], "dry-run")
        self.assertEqual(first["summary"]["headline"], "Backup preview")
        self.assertEqual(first["stepTrace"][0]["step"], "discover")
        self.assertEqual(first["stepTrace"][-1]["step"], "simulate")
        self.assertIn("no artifacts will be created", first["summary"]["highlights"])
        self.assertFalse((self.project_a / ".codexvault").exists())
        self.assertFalse((self.project_b / ".codexvault").exists())

    def test_backup_dry_run_targeted_single_project_is_artifact_free(self) -> None:
        summary = run_cli("backup", "--workspace", str(self.project_a), "--dry-run")
        self.assertEqual(summary["mode"], "dry-run")
        self.assertEqual(summary["projectPath"], str(self.project_a))
        self.assertEqual(summary["summary"]["headline"], "Backup preview")
        self.assertTrue(all(step["status"].startswith("would") for step in summary["stepTrace"]))
        self.assertFalse((self.project_a / ".codexvault").exists())

    def test_backup_command_falls_back_to_root_when_no_projects_found(self) -> None:
        empty_root = self.root / "empty"
        empty_root.mkdir()
        summary = run_cli("backup", "--workspace-root", str(empty_root))
        self.assertEqual(summary["headline"], "Backup complete")
        self.assertIn("1 project(s) backed up", summary["status"])
        self.assertEqual(summary["projects"][0]["projectPath"], str(empty_root.resolve()))

    def test_backup_command_prefers_plugin_projects_over_nested_noise(self) -> None:
        hidden = self.root / "plugins" / "alpha" / "node_modules"
        hidden.mkdir(parents=True)
        (hidden / "junk.txt").write_text("ignore", encoding="utf-8")
        summary = run_cli("backup", "--workspace-root", str(self.root))
        self.assertEqual(len(summary["projects"]), 2)
        for project in summary["projects"]:
            self.assertNotIn("node_modules", project["archivePath"])

    def test_targeted_project_override_still_works(self) -> None:
        summary = run_cli("backup", "--workspace", str(self.project_a))
        self.assertEqual(summary["headline"], "Backup complete")
        self.assertEqual(summary["projectPath"], str(self.project_a))
        self.assertEqual(summary["checksumAlgorithm"], "SHA-256")

    def test_temp_restore_isolated_cleanup(self) -> None:
        simulation = run_cli("simulate", "--scenario", json.dumps({"workspacePath": str(self.project_a)}), "--workspace", str(self.project_a))
        self.assertEqual(simulation["cleanupStatus"], "cleaned")
        self.assertTrue(Path(simulation["simulationPath"]).exists())

    def test_snapshot_excludes_hidden_and_generated_paths(self) -> None:
        (self.project_a / ".git").mkdir()
        (self.project_a / ".git" / "config").write_text("secret", encoding="utf-8")
        (self.project_a / ".codexvault").mkdir()
        (self.project_a / ".codexvault" / "internal.json").write_text("skip", encoding="utf-8")

        discovery = run_cli("discover", "--workspace", str(self.project_a))
        manifest = run_cli("manifest", "--discovery", json.dumps(discovery), "--workspace", str(self.project_a))["manifest"]
        snapshot = run_cli("snapshot", "--manifest", json.dumps(manifest), "--workspace", str(self.project_a))

        with zipfile.ZipFile(snapshot["archivePath"], "r") as zf:
            names = set(zf.namelist())
        self.assertNotIn(".git/config", names)
        self.assertNotIn(".codexvault/internal.json", names)

    def test_verify_not_validated_without_checkpoints(self) -> None:
        report = run_cli("verify", "--plan", json.dumps({"schemaVersion": "v1a", "status": "planning restore", "checkpoints": []}), "--workspace", str(self.project_a))
        self.assertEqual(report["report"]["validationStatus"], "not-validated")
        self.assertIn("missing checkpoints", report["report"]["reasons"][0])

    def test_fixture_contracts_and_examples(self) -> None:
        fixtures = ROOT / "tests" / "fixtures"
        expected_manifest = json.loads((fixtures / "manifest" / "expected-v1a.json").read_text(encoding="utf-8"))
        expected_plan = json.loads((fixtures / "restore" / "expected-plan.json").read_text(encoding="utf-8"))
        expected_report = json.loads((fixtures / "verify" / "expected-report.json").read_text(encoding="utf-8"))
        expected_adjudication = json.loads((fixtures / "simulation" / "expected-adjudication.json").read_text(encoding="utf-8"))
        config_schema = json.loads((ROOT / ".." / ".." / "research" / "codexvault" / "codexvault.config.schema.json").resolve().read_text(encoding="utf-8"))
        windows_cfg = json.loads((ROOT / ".." / ".." / "research" / "codexvault" / "examples" / "windows-codexvault.config.json").resolve().read_text(encoding="utf-8"))

        self.assertEqual(expected_manifest["schemaVersion"], "v1a")
        self.assertTrue(expected_plan["approvalRequired"])
        self.assertEqual(expected_report["validationStatus"], "validated-with-warnings")
        self.assertEqual(expected_adjudication["status"], "simulation complete")
        self.assertEqual(config_schema["properties"]["schemaVersion"]["enum"][0], "v1b")
        self.assertEqual(windows_cfg["paths"]["backupDestination"], "D:\\CodexVault\\snapshots")

    def test_local_mapping_artifacts_define_windows_and_wsl_scope(self) -> None:
        mapping_dir = ROOT / ".." / ".." / "research" / "codexvault" / "local-mapping"
        schema = json.loads((mapping_dir / "mapping-record.schema.json").resolve().read_text(encoding="utf-8"))
        windows_desktop = json.loads((mapping_dir / "examples" / "windows-desktop.json").resolve().read_text(encoding="utf-8"))
        windows_cli = json.loads((mapping_dir / "examples" / "windows-cli.json").resolve().read_text(encoding="utf-8"))
        macos_desktop = json.loads((mapping_dir / "examples" / "macos-desktop.json").resolve().read_text(encoding="utf-8"))
        wsl_linux_cli = json.loads((mapping_dir / "examples" / "wsl-linux-cli.json").resolve().read_text(encoding="utf-8"))

        self.assertEqual(schema["properties"]["platform"]["enum"], ["Windows", "Linux"])
        self.assertEqual(schema["properties"]["codexSurface"]["enum"], ["desktop", "cli"])
        self.assertIn("confidence", schema["properties"])
        self.assertIn("confidence", schema["properties"]["paths"]["items"]["properties"])
        self.assertIn("seed", schema["properties"]["status"]["enum"])
        self.assertIn("verified", schema["properties"]["status"]["enum"])
        self.assertEqual(windows_desktop["platform"], "Windows")
        self.assertEqual(windows_desktop["codexSurface"], "desktop")
        self.assertEqual(windows_desktop["status"], "verified")
        self.assertGreater(windows_desktop["confidence"], 0.9)
        self.assertEqual(windows_cli["platform"], "Windows")
        self.assertEqual(windows_cli["codexSurface"], "cli")
        self.assertEqual(windows_cli["status"], "verified")
        self.assertGreater(windows_cli["confidence"], 0.9)
        self.assertEqual(macos_desktop["platform"], "macOS")
        self.assertEqual(macos_desktop["codexSurface"], "desktop")
        self.assertEqual(macos_desktop["status"], "seed")
        self.assertGreater(macos_desktop["confidence"], 0.7)
        self.assertEqual(wsl_linux_cli["platform"], "Linux")
        self.assertEqual(wsl_linux_cli["status"], "placeholder")
        self.assertTrue(wsl_linux_cli["wsl"])
        self.assertEqual(wsl_linux_cli["codexSurface"], "cli")
        self.assertIn("Windows: Codex Desktop and Codex CLI", (mapping_dir / "README.md").read_text(encoding="utf-8"))
        self.assertIn("Confidence model", (mapping_dir / "README.md").read_text(encoding="utf-8"))

    def test_windows_discovery_run_and_ledger_are_written(self) -> None:
        mapping_dir = ROOT / ".." / ".." / "research" / "codexvault" / "local-mapping"
        run_record = json.loads((mapping_dir / "runs" / "2026-05-19-windows-discovery.json").resolve().read_text(encoding="utf-8"))
        ledger_lines = (mapping_dir / "ledger.jsonl").resolve().read_text(encoding="utf-8").strip().splitlines()
        ledger = [json.loads(line) for line in ledger_lines if line.strip()]
        windows_ledger = [entry for entry in ledger if entry["runId"] == "2026-05-19-windows-discovery"]

        self.assertEqual(run_record["runId"], "2026-05-19-windows-discovery")
        self.assertEqual(run_record["platform"], "Windows")
        self.assertEqual(len(run_record["surfaces"]), 2)
        self.assertEqual(run_record["surfaces"][0]["status"], "verified")
        self.assertEqual(run_record["surfaces"][1]["status"], "verified")
        self.assertGreaterEqual(len(windows_ledger), 8)
        self.assertTrue(all(entry["runId"] == "2026-05-19-windows-discovery" for entry in windows_ledger))
        self.assertTrue(any(entry["path"].endswith("OpenAI.Codex_2p2nqsd0c76g0\\LocalState") for entry in ledger))
        self.assertTrue(any(entry["path"].endswith("OpenAI.Codex_2p2nqsd0c76g0\\RoamingState") for entry in ledger))

    def test_wsl_discovery_run_is_recorded_independently(self) -> None:
        mapping_dir = ROOT / ".." / ".." / "research" / "codexvault" / "local-mapping"
        run_record = json.loads((mapping_dir / "runs" / "2026-05-19-wsl-ubuntu-discovery.json").resolve().read_text(encoding="utf-8"))
        ledger_lines = (mapping_dir / "ledger.jsonl").resolve().read_text(encoding="utf-8").strip().splitlines()
        ledger = [json.loads(line) for line in ledger_lines if line.strip()]
        wsl_entries = [entry for entry in ledger if entry["runId"] == "2026-05-19-wsl-ubuntu-discovery"]

        self.assertEqual(run_record["runId"], "2026-05-19-wsl-ubuntu-discovery")
        self.assertEqual(run_record["distribution"], "Ubuntu")
        self.assertTrue(run_record["wsl"])
        self.assertGreaterEqual(len(wsl_entries), 6)
        self.assertTrue(all(entry["platform"] == "Linux" for entry in wsl_entries))
        self.assertTrue(any(entry["path"].endswith("/AppData/Local/OpenAI/Codex/bin") for entry in wsl_entries))

    def test_mapping_evidence_updater_promotes_and_rejects_paths(self) -> None:
        record = {
            "platform": "Windows",
            "codexSurface": "desktop",
            "captureMode": "install-tree",
            "status": "seed",
            "confidence": 0.4,
            "paths": [
                {"path": "C:/Codex", "kind": "install-root", "confidence": 0.4, "status": "seed", "source": "heuristic"},
                {"path": "C:/Sensitive", "kind": "runtime", "confidence": 0.7, "status": "seed", "source": "heuristic"},
            ],
        }

        updated = cvx.update_mapping_record(
            record,
            {
                "reviewed": True,
                "confidence": 0.9,
                "observedPaths": ["C:/Codex"],
                "rejectedPaths": ["C:/Sensitive"],
                "notes": "observed in backup run",
                "source": "backup",
            },
        )

        self.assertEqual(updated["status"], "reviewed")
        self.assertGreaterEqual(updated["confidence"], 0.8)
        promoted = next(item for item in updated["paths"] if item["path"] == "C:/Codex")
        rejected = next(item for item in updated["paths"] if item["path"] == "C:/Sensitive")
        self.assertEqual(promoted["status"], "verified")
        self.assertEqual(rejected["status"], "rejected")
        self.assertIn("observed in backup run", updated["notes"])
        self.assertEqual(updated["reviewPolicy"]["action"], "auto-verify")

    def test_confidence_threshold_prompts_only_for_review_band(self) -> None:
        self.assertEqual(cvx.confidence_review_policy(0.92)["action"], "auto-verify")
        self.assertFalse(cvx.confidence_review_policy(0.92)["promptUser"])
        self.assertEqual(cvx.confidence_review_policy(0.75)["action"], "prompt-user")
        self.assertTrue(cvx.confidence_review_policy(0.75)["promptUser"])
        self.assertEqual(cvx.confidence_review_policy(0.42)["action"], "no-prompt")
        self.assertFalse(cvx.confidence_review_policy(0.42)["promptUser"])

    def test_dry_run_surfaces_confidence_review_candidates(self) -> None:
        candidates = cvx.confidence_review_candidates(
            [
                {"path": "A", "confidence": 0.9},
                {"path": "B", "confidence": 0.75},
            ]
        )
        self.assertTrue(candidates)
        self.assertTrue(all(item["reviewPolicy"]["promptUser"] for item in candidates))
        self.assertTrue(all(item["confidenceBand"] == "review" for item in candidates))

        instructions = cvx.review_instructions()
        self.assertIn("Confirm or reject", instructions["userAction"])
        self.assertIn("checkbox", " ".join(instructions["instructions"]).lower())

    def test_review_flow_e2e_json_is_aligned_with_instructions(self) -> None:
        discovery = {
            "workspacePath": str(self.project_a),
            "timestamp": cvx.stable_timestamp(),
            "os": "Linux",
            "shell": "bash",
            "assets": [
                {"path": "A", "confidence": 0.75, "status": "seed", "reviewPolicy": cvx.confidence_review_policy(0.75)},
                {"path": "B", "confidence": 0.9, "status": "verified", "reviewPolicy": cvx.confidence_review_policy(0.9)},
            ],
            "assetDependencyGraph": [],
            "platform": {"family": "Debian/Ubuntu"},
        }

        manifest = cvx.manifest_from_discovery(discovery)
        candidates = cvx.confidence_review_candidates(discovery["assets"])
        preview = {
            "summary": {
                "headline": "Backup preview",
                "reviewInstructions": cvx.review_instructions(),
                "confidenceReviewCandidates": candidates,
            }
        }

        self.assertEqual(preview["summary"]["headline"], "Backup preview")
        self.assertEqual(preview["summary"]["reviewInstructions"]["userAction"], "Confirm or reject the listed candidates after the dry-run preview.")
        self.assertEqual(manifest["assetClassification"]["confidence"], 0.9)

    def test_review_flow_e2e_rejected_paths_do_not_reappear(self) -> None:
        candidates = cvx.confidence_review_candidates(
            [
                {"path": "A", "confidence": 0.75, "status": "seed"},
            ]
        )
        rejected = cvx.update_mapping_record(
            {"platform": "Windows", "codexSurface": "desktop", "captureMode": "install-tree", "status": "seed", "confidence": 0.75, "paths": candidates},
            {"reviewed": True, "rejectedPaths": ["A"], "confidence": 0.75, "source": "manual-review"},
        )
        self.assertEqual(rejected["paths"][0]["status"], "rejected")
        self.assertEqual(cvx.confidence_review_candidates(rejected["paths"]), [])

    def test_review_flow_no_candidates_when_all_verified_or_heuristic(self) -> None:
        candidates = cvx.confidence_review_candidates(
            [
                {"path": "A", "confidence": 0.91, "status": "verified"},
                {"path": "B", "confidence": 0.55, "status": "heuristic"},
            ]
        )
        self.assertEqual(candidates, [])

    def test_review_flow_confirmed_candidate_disappears(self) -> None:
        record = {
            "platform": "Windows",
            "codexSurface": "desktop",
            "captureMode": "install-tree",
            "status": "seed",
            "confidence": 0.75,
            "paths": [{"path": "C:/Codex/Desktop", "kind": "install-root", "confidence": 0.75, "status": "seed", "source": "heuristic"}],
        }
        approved = cvx.update_mapping_record(
            record,
            {
                "reviewed": True,
                "confidence": 0.9,
                "observedPaths": ["C:/Codex/Desktop"],
                "source": "manual-review",
                "notes": "user confirmed the candidate",
            },
        )
        self.assertEqual(approved["paths"][0]["status"], "verified")
        self.assertEqual(cvx.confidence_review_candidates(approved["paths"]), [])

    def test_review_flow_rejected_candidate_stays_excluded(self) -> None:
        record = {
            "platform": "Windows",
            "codexSurface": "desktop",
            "captureMode": "install-tree",
            "status": "seed",
            "confidence": 0.75,
            "paths": [{"path": "C:/NotCodex", "kind": "install-root", "confidence": 0.75, "status": "seed", "source": "heuristic"}],
        }
        rejected = cvx.update_mapping_record(
            record,
            {
                "reviewed": True,
                "confidence": 0.75,
                "rejectedPaths": ["C:/NotCodex"],
                "source": "manual-review",
                "notes": "user rejected the candidate",
            },
        )
        self.assertEqual(rejected["paths"][0]["status"], "rejected")
        self.assertEqual(cvx.confidence_review_candidates(rejected["paths"]), [])

    def test_confidence_bands_and_review_candidates(self) -> None:
        self.assertEqual(cvx.classify_confidence_band(0.91), "verified")
        self.assertEqual(cvx.classify_confidence_band(0.7), "review")
        self.assertEqual(cvx.classify_confidence_band(0.4), "heuristic")

        candidates = cvx.confidence_review_candidates(
            [
                {"path": "A", "confidence": 0.9},
                {"path": "B", "confidence": 0.75},
                {"path": "C", "confidence": 0.55},
            ]
        )
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["path"], "B")
        self.assertEqual(candidates[0]["confidenceBand"], "review")

    def test_review_instructions_are_guided_and_non_interactive(self) -> None:
        instructions = cvx.review_instructions()
        self.assertIn("Inspect each listed path", instructions["instructions"][0])
        self.assertIn("Checkbox or mark paths you trust", instructions["instructions"][1])
        self.assertIn("Confirm or reject", instructions["userAction"])

    def test_persist_mapping_run_writes_run_file_and_ledger(self) -> None:
        workspace = self.root / "persist"
        workspace.mkdir()
        record = {
            "platform": "Windows",
            "codexSurface": "cli",
            "captureMode": "install-tree",
            "status": "reviewed",
            "confidence": 0.88,
            "paths": [{"path": "C:/Codex", "kind": "install-root", "confidence": 0.88, "status": "verified"}],
        }
        evidence = {"source": "backup", "observedPaths": ["C:/Codex"]}

        paths = cvx.persist_mapping_run(workspace, "unit-test-run", evidence, record)
        run_path = Path(paths["runPath"])
        ledger_path = Path(paths["ledgerPath"])
        self.assertTrue(run_path.exists())
        self.assertTrue(ledger_path.exists())
        run_payload = json.loads(run_path.read_text(encoding="utf-8"))
        ledger_payload = json.loads(ledger_path.read_text(encoding="utf-8").strip().splitlines()[-1])
        self.assertEqual(run_payload["schemaVersion"], "v1")
        self.assertEqual(run_payload["runId"], "unit-test-run")
        self.assertEqual(run_payload["confidenceBand"], "verified")
        self.assertEqual(ledger_payload["schemaVersion"], "v1")
        self.assertEqual(ledger_payload["runId"], "unit-test-run")

    def test_linux_installer_layout_seed_and_metadata(self) -> None:
        layout = self.project_a / "installer-layout.json"
        layout.write_text(json.dumps({"candidateRoots": ["plugins/codexvault", "cache/codex"]}), encoding="utf-8")

        with patch.object(cvx.platform, "system", return_value="Linux"), patch.dict(
            cvx.os.environ,
            {"HOME": str(self.root), "XDG_CONFIG_HOME": str(self.root / ".config"), "XDG_CACHE_HOME": str(self.root / ".cache")},
            clear=False,
        ):
            discovery = cvx.discover_workspace(self.project_a)

        self.assertEqual(discovery["os"], "Linux")
        self.assertIn("linux", discovery)
        self.assertIn("assets", discovery)
        self.assertTrue(any(item["source"] == "installer-bundle" for item in discovery["assets"]))
        self.assertIsInstance(discovery["assetDependencyGraph"], list)

    def test_installer_layout_rejects_absolute_and_traversal_paths(self) -> None:
        layout = self.project_a / "installer-layout.json"
        layout.write_text(
            json.dumps(
                {
                    "candidateRoots": [
                        "/tmp/evil",
                        "../outside",
                        "",
                        123,
                        "plugins/codexvault",
                    ]
                }
            ),
            encoding="utf-8",
        )

        with patch.object(cvx.platform, "system", return_value="Linux"), patch.dict(cvx.os.environ, {"HOME": str(self.root)}, clear=False):
            discovery = cvx.discover_workspace(self.project_a)

        seeded = [item for item in discovery["assets"] if item.get("source") == "installer-bundle"]
        self.assertEqual(len(seeded), 1)
        self.assertEqual(Path(seeded[0]["path"]).parts[-2:], ("plugins", "codexvault"))
        self.assertLess(seeded[0]["confidence"], 0.9)

    def test_linux_discovery_skips_sensitive_store_paths_by_default(self) -> None:
        home = self.root
        for rel in [".ssh", ".gnupg", ".local/share/keyrings", ".cache/secret-store"]:
            target = home / rel
            target.mkdir(parents=True, exist_ok=True)
            (target / "token.txt").write_text("secret", encoding="utf-8")

        with patch.object(cvx.platform, "system", return_value="Linux"), patch.dict(cvx.os.environ, {"HOME": str(home)}, clear=False):
            discovery = cvx.discover_workspace(self.project_a)

        paths = [item["path"] for item in discovery["assets"]]
        self.assertTrue(all(".ssh" not in path and ".gnupg" not in path and "keyrings" not in path for path in paths))

    def test_discovery_metadata_surfaces_linux_specific_fields(self) -> None:
        with patch.object(cvx.platform, "system", return_value="Linux"), patch.dict(cvx.os.environ, {"WSL_DISTRO_NAME": "Ubuntu-22.04", "VIRTUAL_ENV": "/tmp/venv"}, clear=False):
            discovery = cvx.discover_workspace(self.project_a)
        self.assertIn("osVersion", discovery)
        self.assertIn("privilegeState", discovery)
        self.assertIn("runtimeType", discovery)
        self.assertIn("virtualization", discovery)
        self.assertEqual(discovery["runtimeType"], "wsl")

    def test_python_cli_entrypoint(self) -> None:
        proc = subprocess.run([sys.executable, str(CLI), "--help"], cwd=str(ROOT), capture_output=True, text=True, check=True)
        self.assertIn("backup", proc.stdout)
        self.assertIn("discover", proc.stdout)
        backup_help = subprocess.run([sys.executable, str(CLI), "backup", "--help"], cwd=str(ROOT), capture_output=True, text=True, check=True)
        self.assertIn("workspace-root", backup_help.stdout)
        self.assertIn("dry-run", backup_help.stdout)


if __name__ == "__main__":
    unittest.main()
