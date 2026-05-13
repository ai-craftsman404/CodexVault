# Test Matrix

## Plugin

- Plugin name:
- Version:
- Test date:
- Tester:

## Testing Category Coverage

Record coverage decisions using `knowledge-base/testing-categories-policy.md`.

| Category | Priority | In Scope? | Validation Approach | Result / Gap | Notes |
| --- | --- | --- | --- | --- | --- |
| Example: Unit testing | Mandatory | Yes | `pytest` for prompt builder and parser units | Pass |  |
| Example: Multi-modal input security | Mandatory | No | N/A | N/A | Text-only plugin |

Do not omit categories silently. If a category is not in scope, record why.

## Installation

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Local plugin path is valid |  |  |  |
| `.codex-plugin/plugin.json` exists |  |  |  |
| Manifest JSON parses |  |  |  |
| Manifest paths start with `./` |  |  |  |
| Plugin can be installed or discovered locally |  |  |  |

## Invocation

| Test | Prompt | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- |
| Explicit plugin invocation |  |  |  |  |
| Explicit skill invocation |  |  |  |  |
| Implicit skill trigger |  |  |  |  |
| Should-not-trigger prompt |  |  |  |  |

## Functional Behavior

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Main workflow succeeds |  |  |  |
| Edge case handled |  |  |  |
| Invalid input handled |  |  |  |
| Script failure is understandable |  |  |  |
| Output matches documented format |  |  |  |

## Environment

| Test | Expected Result | Actual Result | Status |
| --- | --- | --- | --- |
| Works without network when expected |  |  |  |
| Handles missing credentials |  |  |  |
| Windows path behavior checked |  |  |  |
| No private files required for public example |  |  |  |

## Result

- Release candidate: yes / no
- Blocking issues:
- Follow-up:
