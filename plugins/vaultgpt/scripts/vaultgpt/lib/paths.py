"""Cross-platform path helpers for VaultGPT."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def default_vault_path() -> Path:
    """Return the OS-native default VaultGPT data directory."""
    if sys.platform.startswith("win"):
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        if base:
            return Path(base) / "VaultGPT"
        return Path.home() / "AppData" / "Local" / "VaultGPT"

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "VaultGPT"

    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "vaultgpt"
    return Path.home() / ".local" / "share" / "vaultgpt"


def resolve_vault_path(explicit: str | Path | None = None) -> Path:
    """Resolve a vault path using explicit value, env override, then OS default."""
    if explicit:
        return Path(explicit).expanduser().resolve()

    env_path = os.environ.get("VAULTGPT_HOME")
    if env_path:
        return Path(env_path).expanduser().resolve()

    return default_vault_path().expanduser().resolve()

