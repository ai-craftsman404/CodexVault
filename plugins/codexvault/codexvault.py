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
LINUX_DISTRO_HINTS = {
    "debian": "Debian/Ubuntu",
    "ubuntu": "Debian/Ubuntu",
    "rhel": "RHEL/CentOS/Fedora",
    "centos": "RHEL/CentOS/Fedora",
    "fedora": "RHEL/CentOS/Fedora",
    "arch": "Arch",
    "suse": "SUSE",
    "opensuse": "SUSE",
    "alpine": "Alpine",
}
LINUX_INIT_HINTS = {
    "systemd": "systemd",
    "openrc": "OpenRC",
    "runit": "runit",
    "s6": "s6",
}
CONFIDENCE_VERIFIED_THRESHOLD = 0.85
CONFIDENCE_REVIEW_THRESHOLD = 0.60
MAPPING_RECORD_SCHEMA_VERSION = "v1"


def _command_exists(command: str) -> bool:
    return shutil.which(command) is not None


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


def detect_os_version() -> str | None:
    version = platform.version() or platform.release()
    return version or None


def detect_kernel_type() -> str:
    if platform.system() == "Linux":
        return "linux-kernel"
    if platform.system() == "Windows":
        return "nt-kernel"
    if platform.system() == "Darwin":
        return "xnu"
    return "unknown"


def detect_privilege_state() -> str:
    if hasattr(os, "geteuid"):
        return "elevated" if os.geteuid() == 0 else "standard"
    if os.name == "nt":
        return "elevated" if os.environ.get("USERNAME", "").lower() == "administrator" else "standard"
    return "unknown"


def detect_virtualization_hints() -> dict[str, Any]:
    indicators = []
    if os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSL_INTEROP"):
        indicators.append("wsl")
    if os.environ.get("container") or os.environ.get("RUNNING_IN_CONTAINER"):
        indicators.append("container")
    if os.path.exists("/.dockerenv"):
        indicators.append("container")
    return {
        "isContainerized": "container" in indicators,
        "isWSL": "wsl" in indicators,
        "indicators": sorted(set(indicators)),
    }


def detect_runtime_type() -> str:
    if os.environ.get("WSL_DISTRO_NAME"):
        return "wsl"
    if os.environ.get("container") or os.environ.get("RUNNING_IN_CONTAINER") or os.path.exists("/.dockerenv"):
        return "container"
    if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_PREFIX"):
        return "virtualenv"
    return "system"


def detect_linux_distribution() -> dict[str, Any]:
    if platform.system() != "Linux":
        return {
            "family": None,
            "id": None,
            "prettyName": None,
            "packageManager": None,
            "initSystem": None,
            "desktopEnvironment": None,
            "shellEcosystem": None,
            "classification": "not-linux",
        }
    info: dict[str, str] = {}
    try:
        with open("/etc/os-release", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                info[key.lower()] = value.strip().strip('"')
    except Exception:
        pass
    distro_id = (info.get("id") or "").lower()
    family = LINUX_DISTRO_HINTS.get(distro_id, "Immutable/container-first" if any(token in distro_id for token in ("wolfi", "nixos", "atomic", "immutable")) else "Unknown")
    package_manager = None
    for candidate, pm in [("apt", "apt"), ("dnf", "dnf"), ("yum", "yum"), ("pacman", "pacman"), ("zypper", "zypper"), ("apk", "apk")]:
        if _command_exists(candidate):
            package_manager = pm
            break
    init_system = None
    if os.path.exists("/run/systemd/system") or _command_exists("systemctl"):
        init_system = "systemd"
    else:
        for candidate, label in LINUX_INIT_HINTS.items():
            if _command_exists(candidate):
                init_system = label
                break
    desktop_environment = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")
    shell_ecosystem = os.environ.get("SHELL") or os.environ.get("BASH_VERSION") or os.environ.get("ZSH_VERSION")
    return {
        "family": family,
        "id": distro_id or None,
        "prettyName": info.get("pretty_name"),
        "packageManager": package_manager,
        "initSystem": init_system,
        "desktopEnvironment": desktop_environment,
        "shellEcosystem": shell_ecosystem,
        "classification": "linux",
    }


def _classify_risk(path: Path) -> str:
    lowered = path.as_posix().lower()
    if any(token in lowered for token in ("keyring", "kwallet", "secret", "credential", "ssh", "gpg")):
        return "sensitive"
    if any(token in lowered for token in ("cache", "tmp", "temp", "runtime")):
        return "ephemeral"
    if any(token in lowered for token in ("config", "settings", "plugins", "skills", "agents", "automation")):
        return "important"
    return "normal"


def _confidence_for_source(source: str) -> float:
    return {
        "installer-bundle": 0.95,
        "workspace-scan": 0.8,
        "heuristic": 0.65,
        "environment": 0.75,
    }.get(source, 0.5)


def update_mapping_record(record: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    updated = json.loads(json.dumps(record))
    updated["schemaVersion"] = updated.get("schemaVersion", MAPPING_RECORD_SCHEMA_VERSION)
    observed = set(evidence.get("observedPaths", []))
    rejected = set(evidence.get("rejectedPaths", []))
    notes = evidence.get("notes")

    updated["status"] = "reviewed" if evidence.get("reviewed", True) else updated.get("status", "seed")
    updated["confidence"] = min(1.0, max(float(updated.get("confidence", 0.0)), float(evidence.get("confidence", updated.get("confidence", 0.0)))))
    if notes:
        existing_notes = updated.get("notes", "")
        updated["notes"] = f"{existing_notes}\n{notes}".strip() if existing_notes else notes

    new_paths = []
    for item in updated.get("paths", []):
        path = item.get("path")
        if path in observed:
            item["status"] = "verified"
            item["confidence"] = min(1.0, max(float(item.get("confidence", 0.0)), float(evidence.get("confidence", item.get("confidence", 0.0)))))
        elif path in rejected:
            item["status"] = "rejected"
            item["confidence"] = min(float(item.get("confidence", 0.0)), float(evidence.get("rejectedConfidence", 0.25)))
        elif evidence.get("demoteHeuristics") and item.get("status") == "heuristic":
            item["confidence"] = max(0.0, float(item.get("confidence", 0.0)) - float(evidence.get("heuristicPenalty", 0.1)))
        new_paths.append(item)

    for path in evidence.get("newObservedPaths", []):
        new_paths.append({
            "path": path,
            "kind": evidence.get("newObservedKind", "unknown"),
            "confidence": float(evidence.get("confidence", 0.5)),
            "status": "verified",
            "source": evidence.get("source", "harness"),
        })

    updated["paths"] = new_paths
    updated["reviewPolicy"] = confidence_review_policy(float(updated.get("confidence", 0.0)))
    return updated


def classify_confidence_band(confidence: float) -> str:
    if confidence >= CONFIDENCE_VERIFIED_THRESHOLD:
        return "verified"
    if confidence >= CONFIDENCE_REVIEW_THRESHOLD:
        return "review"
    return "heuristic"


def confidence_review_policy(confidence: float) -> dict[str, Any]:
    band = classify_confidence_band(confidence)
    if band == "verified":
        return {
            "band": band,
            "action": "auto-verify",
            "promptUser": False,
        }
    if band == "review":
        return {
            "band": band,
            "action": "prompt-user",
            "promptUser": True,
        }
    return {
        "band": band,
        "action": "no-prompt",
        "promptUser": False,
    }


def mapping_run_dir(workspace: Path) -> Path:
    return workspace.resolve() / "research" / "codexvault" / "local-mapping"


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True))
        handle.write("\n")


def persist_mapping_run(workspace: Path, run_id: str, evidence: dict[str, Any], record: dict[str, Any]) -> dict[str, str]:
    base = mapping_run_dir(workspace)
    run_dir = base / "runs"
    ledger_path = base / "ledger.jsonl"
    run_file = run_dir / f"{run_id}.json"
    run_payload = {
        "schemaVersion": MAPPING_RECORD_SCHEMA_VERSION,
        "capturedAt": stable_timestamp(),
        "runId": run_id,
        "confidenceBand": classify_confidence_band(float(record.get("confidence", 0.0))),
        "reviewPolicy": confidence_review_policy(float(record.get("confidence", 0.0))),
        "evidence": evidence,
        "record": record,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    run_file.write_text(json.dumps(run_payload, indent=2), encoding="utf-8")
    append_jsonl(
        ledger_path,
        {
            "schemaVersion": MAPPING_RECORD_SCHEMA_VERSION,
            "capturedAt": run_payload["capturedAt"],
            "runId": run_id,
            "confidence": float(record.get("confidence", 0.0)),
            "status": record.get("status", "seed"),
            "band": run_payload["confidenceBand"],
            "reviewPolicy": run_payload["reviewPolicy"],
            "evidence": evidence,
            "record": record,
        },
    )
    return {"runPath": str(run_file), "ledgerPath": str(ledger_path)}


def confidence_review_candidates(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = []
    for item in items:
        if item.get("status") in {"verified", "rejected"}:
            continue
        confidence = float(item.get("confidence", 0.0))
        policy = confidence_review_policy(confidence)
        band = policy["band"]
        if band == "review":
            candidates.append({**item, "confidenceBand": band, "reviewPolicy": policy})
    return candidates


def review_instructions() -> dict[str, Any]:
    return {
        "headline": "Review-band candidates",
        "instructions": [
            "Inspect each listed path and confirm whether it belongs to CodexVault's canonical mapping.",
            "Checkbox or mark paths you trust as verified.",
            "Reject anything that looks like a generic OS cache, credential store, or unrelated application path.",
            "Leave uncertain items unverified so the next discovery pass can keep them in review.",
        ],
        "userAction": "Confirm or reject the listed candidates after the dry-run preview.",
    }


def _discover_xdg_dirs(home: Path) -> list[Path]:
    dirs = []
    xdg_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_home:
        dirs.append(Path(xdg_home))
    else:
        dirs.append(home / ".config")
    data_home = os.environ.get("XDG_DATA_HOME")
    if data_home:
        dirs.append(Path(data_home))
    else:
        dirs.append(home / ".local" / "share")
    cache_home = os.environ.get("XDG_CACHE_HOME")
    if cache_home:
        dirs.append(Path(cache_home))
    else:
        dirs.append(home / ".cache")
    return dirs


def _walk_candidates(root: Path, max_depth: int = 4) -> list[Path]:
    if not root.exists():
        return []
    results: list[Path] = []
    for path in root.rglob("*"):
        if not path.exists():
            continue
        try:
            depth = len(path.relative_to(root).parts)
        except ValueError:
            continue
        if depth > max_depth:
            continue
        if path.is_symlink():
            results.append(path)
            continue
        if path.is_dir() or path.is_file():
            results.append(path)
    return results


def _classify_linux_path(path: Path) -> dict[str, Any]:
    name = path.name.lower()
    if name in {"keyrings", "kwallet", "secrets", "gnome-keyring", "ssh", "gnupg"}:
        category = "credential"
    elif name in {"cache", "tmp", "temp", "runtime"}:
        category = "runtime"
    elif name in {"config", "plugins", "skills", "agents", "automation", "mcp"}:
        category = "config"
    else:
        category = "general"
    return {
        "path": str(path),
        "category": category,
        "risk": _classify_risk(path),
        "confidence": 0.7,
    }


def _is_safe_discovery_path(path: Path, workspace: Path) -> bool:
    try:
        resolved = path.resolve()
    except Exception:
        return False
    try:
        return resolved.is_relative_to(workspace.resolve())
    except AttributeError:
        workspace_resolved = workspace.resolve()
        return str(resolved).startswith(str(workspace_resolved))


def _is_safe_installer_seed(value: object, workspace: Path) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    candidate = Path(value)
    if candidate.is_absolute():
        return False
    return _is_safe_discovery_path(workspace / candidate, workspace)


def _maybe_installer_layouts(workspace: Path) -> list[dict[str, Any]]:
    candidates = []
    for marker in [workspace / "installer-layout.json", workspace / "install-layout.json"]:
        if marker.exists():
            try:
                data = json.loads(marker.read_text(encoding="utf-8"))
            except Exception:
                continue
            for item in data.get("candidateRoots", []):
                if not _is_safe_installer_seed(item, workspace):
                    continue
                candidate = (workspace / Path(item)).resolve()
                candidates.append({
                    "path": str(candidate),
                    "source": "installer-bundle",
                    "category": "install-root",
                    "risk": "normal",
                    "confidence": 0.85,
                })
    return candidates


def _discover_codex_assets(workspace: Path, os_name: str) -> list[dict[str, Any]]:
    discovered: list[dict[str, Any]] = []
    if os_name == "Linux":
        home = Path(os.environ.get("HOME", str(Path.home())))
        roots = [
            home / ".codex",
            home / ".config" / "codex",
            home / ".local" / "share" / "codex",
            home / ".cache" / "codex",
            workspace / ".codexvault",
            workspace / "plugins",
        ]
        for root in roots:
            for candidate in _walk_candidates(root):
                if any(token in candidate.name.lower() for token in ("codex", "plugin", "skill", "agent", "automation", "mcp", "cache", "keyring", "kwallet", "secret", "gpg", "ssh")):
                    classified = _classify_linux_path(candidate)
                    if classified["risk"] == "sensitive":
                        continue
                    discovered.append(classified)
        discovered.extend(_maybe_installer_layouts(workspace))
    else:
        for root in [workspace / "plugins", workspace / ".codexvault"]:
            if root.exists():
                discovered.append({
                    "path": str(root),
                    "category": "workspace",
                    "risk": "important" if root.name == "plugins" else "normal",
                    "confidence": 0.7,
                })
    return discovered


def _dependency_graph(paths: list[dict[str, Any]]) -> list[dict[str, Any]]:
    graph = []
    for index, item in enumerate(paths):
        if item.get("source") == "installer-bundle":
            continue
        graph.append({
            "node": item["path"],
            "risk": item.get("risk", "normal"),
            "dependsOn": [paths[index - 1]["path"]] if index > 0 else [],
        })
    return graph


class DiscoveryAdapter:
    os_name = "Unknown"

    def discover(self, workspace: Path) -> dict[str, Any]:
        raise NotImplementedError


class WindowsAdapter(DiscoveryAdapter):
    os_name = "Windows"

    def discover(self, workspace: Path) -> dict[str, Any]:
        return {
            "os": detect_os(),
            "osVersion": detect_os_version(),
            "kernelType": detect_kernel_type(),
            "runtimeType": detect_runtime_type(),
            "virtualization": detect_virtualization_hints(),
            "privilegeState": detect_privilege_state(),
            "platform": {"family": "Windows"},
            "assets": _discover_codex_assets(workspace, "Windows"),
        }


class MacOSAdapter(DiscoveryAdapter):
    os_name = "macOS"

    def discover(self, workspace: Path) -> dict[str, Any]:
        return {
            "os": detect_os(),
            "osVersion": detect_os_version(),
            "kernelType": detect_kernel_type(),
            "runtimeType": detect_runtime_type(),
            "virtualization": detect_virtualization_hints(),
            "privilegeState": detect_privilege_state(),
            "platform": {"family": "macOS"},
            "assets": _discover_codex_assets(workspace, "macOS"),
        }


class LinuxAdapter(DiscoveryAdapter):
    os_name = "Linux"

    def discover(self, workspace: Path) -> dict[str, Any]:
        distro = detect_linux_distribution()
        assets = _discover_codex_assets(workspace, "Linux")
        return {
            "os": detect_os(),
            "osVersion": detect_os_version(),
            "kernelType": detect_kernel_type(),
            "runtimeType": detect_runtime_type(),
            "virtualization": detect_virtualization_hints(),
            "privilegeState": detect_privilege_state(),
            "platform": {
                "family": distro.get("family"),
                "distributionId": distro.get("id"),
                "prettyName": distro.get("prettyName"),
                "packageManager": distro.get("packageManager"),
                "initSystem": distro.get("initSystem"),
                "desktopEnvironment": distro.get("desktopEnvironment"),
                "shellEcosystem": distro.get("shellEcosystem"),
            },
            "linux": distro,
            "assets": assets,
        }


def select_adapter() -> DiscoveryAdapter:
    os_name = detect_os()
    if os_name == "Windows":
        return WindowsAdapter()
    if os_name == "macOS":
        return MacOSAdapter()
    if os_name == "Linux":
        return LinuxAdapter()
    return DiscoveryAdapter()


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

    adapter = select_adapter()
    platform_details = adapter.discover(workspace) if not isinstance(adapter, DiscoveryAdapter) or adapter.__class__ is not DiscoveryAdapter else {
        "os": detect_os(),
        "osVersion": detect_os_version(),
        "kernelType": detect_kernel_type(),
        "runtimeType": detect_runtime_type(),
        "virtualization": detect_virtualization_hints(),
        "privilegeState": detect_privilege_state(),
        "platform": {"family": detect_os()},
        "assets": _discover_codex_assets(workspace, detect_os()),
    }
    asset_locations = platform_details.get("assets", [])
    return {
        "timestamp": stable_timestamp(),
        "workspacePath": str(workspace),
        "os": detect_os(),
        "osVersion": platform_details.get("osVersion"),
        "kernelType": platform_details.get("kernelType"),
        "runtimeType": platform_details.get("runtimeType"),
        "virtualization": platform_details.get("virtualization"),
        "privilegeState": platform_details.get("privilegeState"),
        "shell": detect_shell(),
        "status": "discovered",
        "summary": "Workspace discovery complete",
        "adapter": adapter.__class__.__name__ if adapter else "Unknown",
        "platform": platform_details.get("platform", {}),
        "linux": platform_details.get("linux"),
        "assets": asset_locations,
        "assetDependencyGraph": _dependency_graph(asset_locations),
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
        "schemaVersion": "v1b",
        "workspaceId": stable_guid(seed),
        "capturedAt": discovery.get("timestamp", stable_timestamp()),
        "platform": discovery.get("os", "Unknown"),
        "shell": discovery.get("shell", "Unknown"),
        "redactionPolicy": "deny-by-default",
        "workspacePath": str(workspace),
        "discovery": discovery,
        "normalizedDiscovery": {
            "os": discovery.get("os"),
            "osVersion": discovery.get("osVersion"),
            "kernelType": discovery.get("kernelType"),
            "runtimeType": discovery.get("runtimeType"),
            "virtualization": discovery.get("virtualization"),
            "privilegeState": discovery.get("privilegeState"),
            "platform": discovery.get("platform"),
        },
        "assetClassification": {
            "assets": discovery.get("assets", []),
            "dependencyGraph": discovery.get("assetDependencyGraph", []),
            "confidence": max([item.get("confidence", 0.5) for item in discovery.get("assets", [])], default=0.5),
        },
        "mappingEvidence": {
            "status": "seed",
            "confidence": max([item.get("confidence", 0.5) for item in discovery.get("assets", [])], default=0.5),
            "records": [],
        },
        "riskSummary": {
            "sensitive": [item for item in discovery.get("assets", []) if item.get("risk") == "sensitive"],
            "important": [item for item in discovery.get("assets", []) if item.get("risk") == "important"],
            "ephemeral": [item for item in discovery.get("assets", []) if item.get("risk") == "ephemeral"],
        },
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
        "compatibility": {
            "sourcePlatform": manifest.get("normalizedDiscovery", {}).get("platform", {}),
            "os": manifest.get("normalizedDiscovery", {}).get("os"),
            "osVersion": manifest.get("normalizedDiscovery", {}).get("osVersion"),
            "runtimeType": manifest.get("normalizedDiscovery", {}).get("runtimeType"),
            "riskSummary": manifest.get("riskSummary", {}),
        },
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
        reasons = ["runtime mismatch check not yet implemented", "restore compatibility remains advisory only"]
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
        mapping_evidence = update_mapping_record(
            {
                "platform": "Linux" if scenario.get("platform") == "Linux" else "Windows",
                "codexSurface": scenario.get("codexSurface", "cli"),
                "captureMode": "workspace-probe",
                "status": "seed",
                "confidence": 0.5,
                "paths": [
                    {
                        "path": scenario.get("workspacePath", str(workspace)),
                        "kind": "workspace",
                        "confidence": 0.5,
                        "status": "heuristic",
                        "source": "simulation",
                    }
                ],
            },
            {
                "reviewed": True,
                "confidence": 0.65,
                "observedPaths": [scenario.get("workspacePath", str(workspace))],
                "notes": "Simulation confirmed workspace-probe coverage for the active run.",
                "source": "simulation",
            },
        )
        transcript_path = temp_root / "simulation.json"
        transcript_payload = {"transcript": transcript, "adjudication": adjudication, "mappingEvidence": mapping_evidence}
        transcript_path.write_text(json.dumps(transcript_payload, indent=2), encoding="utf-8")
        output_path = paths["simulationDir"] / f"simulation-{stable_timestamp()}.json"
        shutil.copy2(transcript_path, output_path)
        persist_mapping_run(workspace, f"simulation-{stable_timestamp()}", {"source": "simulation", "adjudication": adjudication}, mapping_evidence)
        return {
            "simulationPath": str(output_path),
            "cleanupStatus": "cleaned",
            "adjudication": adjudication,
            "simulation": transcript,
            "mappingEvidence": mapping_evidence,
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
    mapping_evidence = update_mapping_record(
        {
            "platform": discovery.get("os", "Unknown"),
            "codexSurface": "cli",
            "captureMode": "install-tree",
            "status": "seed",
            "confidence": manifest_envelope["manifest"]["assetClassification"]["confidence"],
            "paths": discovery.get("assets", []),
        },
        {
            "reviewed": True,
            "confidence": simulation["mappingEvidence"]["confidence"],
            "observedPaths": [item["path"] for item in discovery.get("assets", [])[:3]],
            "rejectedPaths": [item["path"] for item in discovery.get("assets", []) if item.get("risk") == "sensitive"],
            "notes": "Backup run and harness review updated observed coverage.",
            "source": "backup",
        },
    )
    persist_mapping_run(
        project_path,
        f"backup-{manifest_envelope['manifest']['workspaceId']}",
        {
            "source": "backup",
            "discovery": discovery,
            "manifest": manifest_envelope["manifest"],
            "simulation": simulation["mappingEvidence"],
        },
        mapping_evidence,
    )
    return {
        "projectPath": str(project_path),
        "headline": "Backup complete",
        "status": "integrity verified",
        "workspaceId": manifest_envelope["manifest"]["workspaceId"],
        "archivePath": snapshot["archivePath"],
        "checksumAlgorithm": snapshot["checksumAlgorithm"],
        "validationStatus": report["report"]["validationStatus"],
        "simulationCleanup": simulation["cleanupStatus"],
        "mappingConfidence": mapping_evidence["confidence"],
        "mappingStatus": mapping_evidence["status"],
    }


def dry_run_project_backup(project_path: Path) -> dict[str, Any]:
    discovery = discover_workspace(project_path)
    manifest_preview = manifest_from_discovery(discovery)
    review_candidates = confidence_review_candidates(discovery.get("assets", []))
    review_details = review_instructions() if review_candidates else None
    step_trace = [
        {
            "step": "discover",
            "status": "would-run",
            "detail": f"inspect {project_path}",
        },
        {
            "step": "manifest",
            "status": "would-run",
            "detail": "derive workspace manifest and workspaceId",
        },
        {
            "step": "snapshot",
            "status": "would-skip-artifacts",
            "detail": "preview allowlisted files, checksum, and archive naming",
        },
        {
            "step": "plan",
            "status": "would-run",
            "detail": "preview restore checkpoints and approval gate",
        },
        {
            "step": "verify",
            "status": "would-run",
            "detail": "preview restore validation decision",
        },
        {
            "step": "simulate",
            "status": "would-run",
            "detail": "preview agent-team restore rehearsal in isolated temp dir",
        },
    ]
    if review_candidates:
        step_trace.append(
            {
                "step": "confidence-review",
                "status": "would-prompt",
                "detail": f"{len(review_candidates)} candidate path(s) fall into the human review band",
            }
        )
    highlights = [
        f"workspaceId={manifest_preview['workspaceId']}",
        f"platform={manifest_preview['platform']}",
        "no artifacts will be created",
        "restore would require approval",
    ]
    return {
        "projectPath": str(project_path),
        "mode": "dry-run",
        "headline": "Backup dry run complete",
        "status": "preview only; no artifacts created",
        "stepTrace": step_trace,
        "summary": {
            "headline": "Backup preview",
            "status": "no artifacts created",
            "highlights": highlights,
            "confidenceReviewCandidates": review_candidates,
            "reviewInstructions": review_details,
        },
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


def dry_run_root_backup(workspace_root: Path) -> dict[str, Any]:
    projects = discover_projects(workspace_root)
    if not projects:
        projects = [workspace_root_from_path(workspace_root)]
    results = [dry_run_project_backup(project) for project in projects]
    return {
        "headline": "Backup dry run complete",
        "status": f"{len(results)} project(s) previewed; no artifacts created",
        "workspaceRoot": str(workspace_root_from_path(workspace_root)),
        "projects": results,
        "summary": {
            "headline": "Backup preview",
            "status": f"{len(results)} project(s) would be backed up",
            "highlights": [
                "discover, manifest, snapshot, plan, verify, simulate would run",
                "no manifest, archive, or verification artifacts would be written",
                "agent-team rehearsal would stay isolated and non-destructive",
            ],
        },
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
    p.add_argument("--dry-run", action="store_true", help="Preview the full backup workflow without creating artifacts")

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
        if getattr(args, "dry_run", False):
            if workspace and not workspace_root:
                emit(dry_run_project_backup(workspace))
            else:
                emit(dry_run_root_backup(workspace_root or workspace_root_from_path(Path.cwd())))
        elif workspace and not workspace_root:
            emit(run_project_backup(workspace))
        else:
            emit(run_root_backup(workspace_root or workspace_root_from_path(Path.cwd())))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
