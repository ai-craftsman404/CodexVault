# VaultGPT Scripts

Deterministic local operations implemented for the MVP foundation:

- vault initialization
- import/export
- indexing/search
- organization metadata
- prompt vault
- manual prompt chains
- privacy review
- audit logs
- status reports

Run tests:

```powershell
cd plugins/vaultgpt/scripts/vaultgpt
python -m unittest discover -s tests
```

Runtime vault data must stay outside the plugin source tree.
