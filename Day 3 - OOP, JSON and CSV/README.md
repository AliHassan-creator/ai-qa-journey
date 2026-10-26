# Day 3 Deliverable: OOP, JSON and CSV

## Learning objectives

- Represent a manual test case with a Python dataclass.
- Read test cases from CSV and write/read them as JSON.
- Keep sample test data sanitized and verify that a format conversion preserves it.

## Files

- [`testcase.py`](testcase.py) defines the `TestCase` dataclass and reusable CSV/JSON readers and writers.
- [`sample_test_cases.csv`](sample_test_cases.csv) contains ten fictional test cases for a sample booking application.
- [`sample_test_cases.json`](sample_test_cases.json) is generated from the CSV when the script runs.

The sample application rules are illustrative. In particular, the equal-date
case asks the application to follow its documented minimum-stay rule rather
than assuming what that rule should be. All sample people and credentials are
fictional; no customer or production data is included.

## Run in PowerShell

From the repository root:

```powershell
python ".\Day 3 - OOP, JSON and CSV\testcase.py"
```

This reads the CSV, writes the JSON export, reloads it, and checks that the
records round-trip without changes.

## Verification record

Run from the deliverable folder with the repository virtual environment on
2026-10-26:

- Command: `..\\.venv\\Scripts\\python.exe testcase.py`
- Exit code: 0
- Records loaded from CSV and exported/reloaded from JSON: 10
- Dataclass and CSV/JSON round-trip checks: 4 passed

A successful run verifies the included ten records and these conversions; it
does not validate a real application or a formal JSON Schema.
