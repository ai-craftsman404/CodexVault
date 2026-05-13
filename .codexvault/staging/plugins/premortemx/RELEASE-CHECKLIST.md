# PreMortemX Release Checklist

## Identity

- [x] plugin name is `premortemx`
- [x] display name is `PreMortemX`
- [x] version is `0.2.0`

## Plugin package

- [x] `.codex-plugin/plugin.json` is present
- [x] `skills/premortemx/SKILL.md` is present
- [x] scripts are present under `scripts/`
- [x] design package is present under `design/`

## Documentation

- [x] `README.md` is complete
- [x] `CHANGELOG.md` is updated
- [x] `LICENSE` is present
- [x] `TEST-MATRIX.md` is present
- [x] `SECURITY-REVIEW.md` is present

## Validation

- [x] local script tests pass
- [x] run artifact conventions are documented
- [x] run-record schema is documented
- [x] adversarial evaluator cases are documented

## Marketplace and discovery

- [x] repo-local marketplace entry includes `premortemx`
- [x] marketplace path points to `./plugins/premortemx`

## Scope discipline

- [x] release-risk mode remains supported
- [x] architecture validation ships in v2
- [x] no mandatory external service dependency has been introduced
