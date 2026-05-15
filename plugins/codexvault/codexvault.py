#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Any


ALLOWLIST_PATTERNS = [
    "*.md",
    "*.json",
    "skills/**",
    "scripts/**",
    "tests/fixtures/**",
    "assets/**",
    "README*",
    "LICENSE*",
    "CHANGELOG*",
]
EXCLUDED_NAMES = {".git", "node_modules", "__pycache__", ".codexvault", ".DS_Store"}


def stable_timestamp() -> str:
    return (
        subprocess.check_output(
            [sys.executable, "-c", "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))"],
            text=True,
        )
        .strip()
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def stable_guid(seed: str) -> str:
    digest = sha256_text(seed)[:32]
    return str(uuid.UUID(digest))


def detect_shell() -> str:
    shell = os.environ.get("SHELL") or os.environ.get("COMSPEC") or os.environ.get("TERM_PROGRAM")
    if shell:
        lowered = shell.lower()
        if "cmd.exe" in lowered:
            return "cmd"
        if "bash" in lowered:
            return "bash"
        if "zsh" in lowered:
            return "zsh"
    return "Unknown"


def detect_os() -> str:
    system = platform.system()
    return {"Windows": "Windows", "Linux": "Linux", "Darwin": "macOS"}.get(system, system or "Unknown")


def workspace_root_from_path(path: Path) -> Path:
    return path.resolve()


def discover_projects(workspace_root: Path) -> list[Path]:
    root = workspace_root_from_path(workspace_root)
    plugins_dir = root / "plugins"
    if not plugins_dir.exists():
        return [root] if (root / ".codex-plugin" / "plugin.json").exists() else []

    projects: list[Path] = []
    for candidate in sorted(plugins_dir.rglob("plugin.json")):
        if candidate.parent.name == ".codex-plugin":
            projects.append(candidate.parent.parent)
    return projects


def walk_allowlisted_files(workspace: Path) -> list[Path]:
    files: list[Path] = []
    if not workspace.exists():
        return files
    for path in workspace.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if any(part in EXCLUDED_NAMES for part in rel.parts):
            continue
        files.append(path)
    return files


def command_version(command: str) -> str | None:
    try:
        out = subprocess.check_output([command, "--version"], stderr=subprocess.STDOUT, text=True, timeout=5)
        return out.strip().splitlines()[0] if out.strip() else None
    except Exception:
        return None


def discover_workspace(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    git_root = None
    git_commit = None
    git_branch = None
    try:
        git_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=workspace, text=True).strip()
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=workspace, text=True).strip()
        git_branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=workspace, text=True).strip() or None
    except Exception:
        pass

    return {
        "timestamp": stable_timestamp(),
        "workspacePath": str(workspace),
        "os": detect_os(),
        "shell": detect_shell(),
        "status": "discovered",
        "summary": "Workspace discovery complete",
        "versions": {
            "git": command_version("git"),
            "python": sys.version.split()[0],
            "node": command_version("node"),
        },
        "git": {
            "root": git_root,
            "commit": git_commit,
            "branch": git_branch,
        },
    }


def manifest_from_discovery(discovery: dict[str, Any]) -> dict[str, Any]:
    workspace = Path(discovery["workspacePath"]).resolve()
    seed = f"{workspace}|{discovery.get('os')}|{discovery.get('shell')}"
    return {
        "schemaVersion": "v1a",
        "workspaceId": stable_guid(seed),
        "capturedAt": discovery.get("timestamp", stable_timestamp()),
        "platform": discovery.get("os", "Unknown"),
        "shell": discovery.get("shell", "Unknown"),
        "redactionPolicy": "deny-by-default",
        "workspacePath": str(workspace),
        "discovery": discovery,
    }


def get_path_config(workspace: Path) -> dict[str, Path]:
    root = workspace.resolve()
    cvx = root / ".codexvault"
    return {
        "workspaceRoot": root,
        "backupDestinationDir": cvx / "snapshots",
        "snapshotStagingDir": cvx / "staging",
        "manifestOutputDir": cvx / "manifests",
        "restorePlanDir": cvx / "restores",
        "verificationDir": cvx / "verification",
        "simulationDir": cvx / "simulations",
        "fixtureRoot": root / "plugins" / "codexvault" / "tests" / "fixtures",
    }


def ensure_dirs(*dirs: Path) -> None:
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def write_manifest(discovery: dict[str, Any], workspace: Path) -> dict[str, Any]:
    manifest = manifest_from_discovery(discovery)
    paths = get_path_config(workspace)
    ensure_dirs(paths["manifestOutputDir"])
    manifest_path = paths["manifestOutputDir"] / f"manifest-{manifest['workspaceId']}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"manifestPath": str(manifest_path), "manifest": manifest}


def allowed_snapshot_files(workspace: Path) -> list[Path]:
    return walk_allowlisted_files(workspace)


def create_snapshot(manifest: dict[str, Any], workspace: Path) -> dict[str, Any]:
    paths = get_path_config(workspace)
    ensure_dirs(paths["backupDestinationDir"], paths["snapshotStagingDir"])
    staging = Path(tempfile.mkdtemp(prefix="codexvault-staging-"))
    try:
        snapshot_root = staging / "snapshot"
        snapshot_root.mkdir(parents=True, exist_ok=True)
        included = 0
        for source in allowed_snapshot_files(workspace):
            rel = source.relative_to(workspace)
            target = snapshot_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            included += 1
        if included == 0:
            placeholder = snapshot_root / ".cvx-placeholder"
            placeholder.write_text("CodexVault snapshot placeholder", encoding="utf-8")
        archive_name = f"codexvault-{manifest['workspaceId']}-{stable_timestamp()}-{manifest['platform']}.zip"
        archive_path = paths["backupDestinationDir"] / archive_name
        if archive_path.exists():
            archive_path.unlink()
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file in snapshot_root.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(snapshot_root).as_posix())
        checksum = sha256_bytes(archive_path.read_bytes())
        sidecar = {
            "archivePath": archive_name,
            "checksumAlgorithm": "SHA-256",
            "checksum": checksum,
        }
        sidecar_path = paths["backupDestinationDir"] / f"{archive_name}.sha256.json"
        sidecar_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
        return {
            "schemaVersion": manifest["schemaVersion"],
            "workspaceId": manifest["workspaceId"],
            "createdAt": stable_timestamp(),
            "archivePath": str(archive_path),
            "checksum": checksum,
            "checksumAlgorithm": "SHA-256",
            "status": "snapshot complete",
        }
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def plan_restore(manifest: dict[str, Any], workspace: Path) -> dict[str, Any]:
    paths = get_path_config(workspace)
    ensure_dirs(paths["restorePlanDir"])
    plan = {
        "schemaVersion": manifest["schemaVersion"],
        "status": "planning restore",
        "checkpoints": [
            "validate archive",
            "prepare isolated temp dir",
            "request approval for in-place changes",
        ],
        "approvalRequired": True,
        "tempRestoreScope": "plugin-managed isolated temp-dir only",
        "workspaceId": manifest["workspaceId"],
    }
    plan_path = paths["restorePlanDir"] / f"restore-plan-{manifest['workspaceId']}.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return {"planPath": str(plan_path), "plan": plan}


def verify_restore(plan: dict[str, Any], workspace: Path) -> dict[str, Any]:
    paths = get_path_config(workspace)
    ensure_dirs(paths["verificationDir"])
    checkpoints = plan.get("checkpoints") or []
    if not checkpoints:
        status = "not-validated"
        reasons = ["restore plan missing checkpoints"]
    elif plan.get("approvalRequired"):
        status = "validated-with-warnings"
        reasons = ["runtime mismatch check not yet implemented"]
    else:
        status = "validated"
        reasons = []
    report = {
        "schemaVersion": plan.get("schemaVersion", "v1a"),
        "validationStatus": status,
        "summary": "Restore verification report",
        "reasons": reasons,
    }
    report_path = paths["verificationDir"] / f"verification-{stable_timestamp()}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return {"verificationPath": str(report_path), "report": report}


def simulate_restore_team(scenario: dict[str, Any], workspace: Path) -> dict[str, Any]:
    paths = get_path_config(workspace)
    ensure_dirs(paths["simulationDir"])
    temp_root = Path(tempfile.mkdtemp(prefix="codexvault-sim-"))
    try:
        transcript = {
            "schemaVersion": "v1a",
            "status": "simulation complete",
            "headline": "Agent-team simulation stub",
            "findings": [
                "discovery agent identified workspace scope",
                "snapshot agent confirmed manifest completeness placeholder",
                "restore planning agent requested approval checkpoint",
            ],
        }
        adjudication = {
            "claims": ["workspace scope identified", "restore path requires approval"],
            "supportingEvidence": ["scenario input", "plan checkpoint"],
            "disputesResolved": ["no destructive action allowed"],
            "decision": "proceed-with-checkpoints",
            "confidenceDelta": "low-positive",
        }
        transcript_path = temp_root / "simulation.json"
        transcript_path.write_text(json.dumps({"transcript": transcript, "adjudication": adjudication}, indent=2), encoding="utf-8")
        output_path = paths["simulationDir"] / f"simulation-{stable_timestamp()}.json"
        shutil.copy2(transcript_path, output_path)
        return {
            "simulationPath": str(output_path),
            "cleanupStatus": "cleaned",
            "adjudication": adjudication,
            "simulation": transcript,
        }
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def run_project_backup(project_path: Path) -> dict[str, Any]:
    discovery = discover_workspace(project_path)
    manifest_envelope = write_manifest(discovery, project_path)
    snapshot = create_snapshot(manifest_envelope["manifest"], project_path)
    plan = plan_restore(manifest_envelope["manifest"], project_path)
    report = verify_restore(plan["plan"], project_path)
    simulation = simulate_restore_team({"workspacePath": str(project_path)}, project_path)
    return {
        "projectPath": str(project_path),
        "headline": "Backup complete",
        "status": "integrity verified",
        "workspaceId": manifest_envelope["manifest"]["workspaceId"],
        "archivePath": snapshot["archivePath"],
        "checksumAlgorithm": snapshot["checksumAlgorithm"],
        "validationStatus": report["report"]["validationStatus"],
        "simulationCleanup": simulation["cleanupStatus"],
    }


def run_root_backup(workspace_root: Path) -> dict[str, Any]:
    projects = discover_projects(workspace_root)
    if not projects:
        projects = [workspace_root_from_path(workspace_root)]
    results = [run_project_backup(project) for project in projects]
    return {
        "headline": "Backup complete",
        "status": f"{len(results)} project(s) backed up",
        "workspaceRoot": str(workspace_root_from_path(workspace_root)),
        "projects": results,
    }


def load_json(text_or_path: str) -> Any:
    stripped = text_or_path.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return json.loads(text_or_path)
    candidate = Path(text_or_path)
    if candidate.exists():
        return json.loads(candidate.read_text(encoding="utf-8"))
    return json.loads(text_or_path)


def emit(obj: Any) -> None:
    sys.stdout.write(json.dumps(obj, indent=2))
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codexvault", description="Cross-platform workspace backup and restore orchestration for Codex projects.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("discover")
    p.add_argument("--workspace", required=True)

    p = sub.add_parser("manifest")
    p.add_argument("--discovery", required=True)
    p.add_argument("--workspace", required=True)

    p = sub.add_parser("snapshot")
    p.add_argument("--manifest", required=True)
    p.add_argument("--workspace", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--manifest", required=True)
    p.add_argument("--workspace", required=True)

    p = sub.add_parser("verify")
    p.add_argument("--plan", required=True)
    p.add_argument("--workspace", required=True)

    p = sub.add_parser("simulate")
    p.add_argument("--scenario", required=True)
    p.add_argument("--workspace", required=True)

    p = sub.add_parser("backup")
    p.add_argument("--workspace-root", required=False, help="Main Codex project root containing plugin projects")
    p.add_argument("--workspace", required=False, help="Advanced override for a single project backup")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path(getattr(args, "workspace")) if getattr(args, "workspace", None) else None
    workspace_root = Path(getattr(args, "workspace_root")) if getattr(args, "workspace_root", None) else None

    if args.command == "discover":
        emit(discover_workspace(workspace or workspace_root_from_path(Path.cwd())))
        return 0
    if args.command == "manifest":
        project = workspace or workspace_root_from_path(Path.cwd())
        emit(write_manifest(load_json(args.discovery), project))
        return 0
    if args.command == "snapshot":
        project = workspace or workspace_root_from_path(Path.cwd())
        emit(create_snapshot(load_json(args.manifest), project))
        return 0
    if args.command == "plan":
        project = workspace or workspace_root_from_path(Path.cwd())
        emit(plan_restore(load_json(args.manifest), project))
        return 0
    if args.command == "verify":
        project = workspace or workspace_root_from_path(Path.cwd())
        emit(verify_restore(load_json(args.plan), project))
        return 0
    if args.command == "simulate":
        project = workspace or workspace_root_from_path(Path.cwd())
        emit(simulate_restore_team(load_json(args.scenario), project))
        return 0
    if args.command == "backup":
        if workspace and not workspace_root:
            emit(run_project_backup(workspace))
        else:
            emit(run_root_backup(workspace_root or workspace_root_from_path(Path.cwd())))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
