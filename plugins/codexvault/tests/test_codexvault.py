from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "codexvault.py"


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

        manifest_envelope = run_cli("manifest", "--discovery", json.dumps(discovery), "--workspace", str(self.project_a))
        manifest = manifest_envelope["manifest"]
        self.assertEqual(manifest["schemaVersion"], "v1a")
        self.assertTrue(manifest["workspaceId"])

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

        report = run_cli("verify", "--plan", json.dumps(plan["plan"]), "--workspace", str(self.project_a))
        self.assertIn(report["report"]["validationStatus"], {"validated", "validated-with-warnings"})

        simulation = run_cli("simulate", "--scenario", json.dumps({"workspacePath": str(self.project_a)}), "--workspace", str(self.project_a))
        self.assertEqual(simulation["cleanupStatus"], "cleaned")
        self.assertTrue(simulation["adjudication"]["decision"])

    def test_backup_command_scans_all_projects_under_root(self) -> None:
        summary = run_cli("backup", "--workspace-root", str(self.root))
        self.assertEqual(summary["headline"], "Backup complete")
        self.assertIn("2 project(s) backed up", summary["status"])
        self.assertEqual(len(summary["projects"]), 2)
        self.assertEqual(summary["projects"][0]["checksumAlgorithm"], "SHA-256")
        self.assertEqual(summary["projects"][1]["simulationCleanup"], "cleaned")

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

    def test_python_cli_entrypoint(self) -> None:
        proc = subprocess.run([sys.executable, str(CLI), "--help"], cwd=str(ROOT), capture_output=True, text=True, check=True)
        self.assertIn("backup", proc.stdout)
        self.assertIn("discover", proc.stdout)
        backup_help = subprocess.run([sys.executable, str(CLI), "backup", "--help"], cwd=str(ROOT), capture_output=True, text=True, check=True)
        self.assertIn("workspace-root", backup_help.stdout)
        self.assertIn("dry-run", backup_help.stdout)


if __name__ == "__main__":
    unittest.main()
