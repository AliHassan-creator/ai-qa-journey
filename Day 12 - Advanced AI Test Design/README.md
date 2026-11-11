# Day 12: Advanced AI Test Design

## Workbook scope

Day 12 adds five practices around AI-assisted quality work:

1. Convert ambiguous requirements into questions for a business analyst/product owner.
2. Generate synthetic valid, invalid, boundary, Unicode, and long test data.
3. Use evidence-based risk prioritization, then record the human override and reason.
4. Convert verified raw observations into a concise bug-report draft.
5. Review AI output with an eight-point quality checklist.

The workbook deliverable is a **five-prompt library plus review checklist**. The QA-Copilot capstone increment is deterministic validators for schema, duplicate cases, and acceptance-criteria traceability.

## Prompt library

The five prompts are versioned in `qa-copilot/prompts/`:

| Prompt | Purpose | Output boundary |
|---|---|---|
| `testcase_gen.md` | Draft manual cases from story and acceptance criteria | Day 3 `TestCase` records plus review metadata |
| `ambiguity_finder.md` | Find vague, conflicting, or missing requirement details | Questions/options, not invented answers |
| `test_data_generator.md` | Create synthetic values for defined partitions and boundaries | Labeled data; unspecified outcomes marked for clarification |
| `risk_prioritizer.md` | Rank existing cases using provided impact/likelihood evidence | Preserve all input IDs; expose unknown evidence; human approves overrides |
| `bug_report_writer.md` | Turn observed notes into a bug-report draft | Observation separated from hypothesis; no invented root cause |

## Core deterministic validators

`qa-copilot/core/validators.py` implements:

- **Schema validation:** checks the Day 11 output contract and each test case's required fields, types, and allowed priority/type values, using `core/schemas/test_case_output.schema.json`.
- **Duplicate checks:** catches repeated IDs and exact normalized duplicates based on title, preconditions, ordered steps, and expected result. This is intentionally a deterministic duplicate check, not semantic duplicate detection.
- **Traceability checks:** confirms each supplied acceptance criterion has at least one valid coverage reference, each referenced case ID exists, and each case maps to a criterion.
- **Combined validation:** `validate_test_case_output` runs schema validation first, then duplicate and traceability checks. It returns `ValidationIssue` objects with stable codes and paths; it does not rewrite or silently discard content.

The validators are deliberately deterministic. They do not decide whether a test is a good test, whether requirements are true, or whether two differently worded scenarios are semantically duplicates. A human reviewer still uses [the eight-point checklist](REVIEW_CHECKLIST.md), also available in the versioned prompt library.

## Run the focused tests

From the repository root in PowerShell:

```powershell
& ".\.venv\Scripts\python.exe" -m pytest -v "qa-copilot/tests/test_validators.py" "Day 11 - Prompting for Test Design/test_prompt_outputs.py" --basetemp ".pytest_cache\day12-validation"
```

Breakdown:

- `&` executes the quoted program in PowerShell.
- `.\.venv\Scripts\python.exe` uses the project's virtual environment.
- `-m pytest` runs pytest from that environment.
- `-v` lists each test.
- The two paths select Day 12 core-validator tests and the Day 11 sample-contract tests.
- `--basetemp` directs pytest temporary files into the ignored project cache.

Install the QA-Copilot dependency if needed:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install -r ".\qa-copilot\requirements.txt"
```

## Workbook hands-on work

For learning evidence, choose an approved, sanitized requirement and practice each prompt. Never send real credentials, payment data, personal data, or confidential requirements to an unapproved AI provider.

For the risk-prioritizer exercise, include only evidence you have (impact, history/likelihood, and detectability). If likelihood is unknown, keep it unknown; do not let an AI invent a probability. Record your override reason next to the AI's suggestion.

For bug-writing, keep an untouched copy of the raw observation and compare the AI draft against it. Expected behavior must cite a requirement; if none exists, mark it for clarification instead of calling the behavior a defect.

## Verification state

- **Implemented:** five prompts, the eight-point checklist, JSON Schema contract, and deterministic schema/duplicate/traceability validators.
- **Verified:** 10 Day 12 validator tests and 3 Day 11 output-contract tests passed (13 focused tests); the full offline CI selection passed 30 tests; Ruff passed for all QA-Copilot code.
- **Learned:** in progress until the prompts are practiced and the validator findings can be explained.
- **Presentable:** pending independent demonstration.
