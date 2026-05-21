import json
import os
import tempfile
import unittest
from pathlib import Path

from lib.audit import append_event, read_events
from lib.paths import default_vault_path, resolve_vault_path
from lib.vault import initialize_vault, write_record


class VaultGPTCoreTests(unittest.TestCase):
    def test_resolve_vault_path_prefers_explicit_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            explicit = Path(tmp) / "custom-vault"
            resolved = resolve_vault_path(explicit=explicit)
            self.assertEqual(resolved, explicit.resolve())

    def test_resolve_vault_path_prefers_environment_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / "env-vault"
            old_value = os.environ.get("VAULTGPT_HOME")
            os.environ["VAULTGPT_HOME"] = str(env_path)
            try:
                self.assertEqual(resolve_vault_path(), env_path.resolve())
            finally:
                if old_value is None:
                    os.environ.pop("VAULTGPT_HOME", None)
                else:
                    os.environ["VAULTGPT_HOME"] = old_value

    def test_default_vault_path_is_os_aware(self):
        path = default_vault_path()
        self.assertIsInstance(path, Path)
        self.assertIn("vaultgpt", str(path).lower())

    def test_initialize_vault_creates_expected_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = initialize_vault(Path(tmp) / "vault")
            self.assertTrue((root / "vault.json").is_file())
            self.assertTrue((root / "audit.jsonl").is_file())
            self.assertTrue((root / "conversations").is_dir())
            self.assertTrue((root / "prompts").is_dir())
            self.assertTrue((root / "chains").is_dir())
            self.assertTrue((root / "exports").is_dir())
            self.assertTrue((root / "indexes").is_dir())

            metadata = json.loads((root / "vault.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["schema_version"], "0.1")
            self.assertEqual(metadata["name"], "VaultGPT")

    def test_write_record_writes_json_with_schema_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = initialize_vault(Path(tmp) / "vault")
            record_path = write_record(
                root,
                "prompts",
                {
                    "id": "prompt_test",
                    "title": "Test Prompt",
                    "body": "Review {{artifact}}",
                },
            )

            data = json.loads(record_path.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "0.1")
            self.assertEqual(data["id"], "prompt_test")

    def test_append_event_is_append_only_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = initialize_vault(Path(tmp) / "vault")
            append_event(root, "vault.initialized", {"item_id": "vault"})
            append_event(root, "prompt.created", {"item_id": "prompt_test"})

            events = read_events(root)
            self.assertEqual([event["action"] for event in events], ["vault.initialized", "prompt.created"])
            self.assertTrue(all("timestamp" in event for event in events))
            self.assertTrue(all(event["actor"] == "local-user" for event in events))


if __name__ == "__main__":
    unittest.main()

