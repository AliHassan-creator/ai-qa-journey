# Day 2 Deliverable: Python Core for Testers

## Learning objectives

- Apply robust boundary-value analysis to an inclusive integer range.
- Divide an age-based ticket rule into valid and invalid equivalence classes.
- Use assertions and loops to check behavior and summarize test results.

## Deliverables

- [`bva.py`](bva.py): returns the six robust BVA points: just below the minimum, the minimum, just above the minimum, just below the maximum, the maximum, and just above the maximum.
- [`ep.py`](ep.py): classifies ages using the assumptions documented in the function.
- [`self_checks.py`](self_checks.py): runs eight assertions and summarizes 20 mock results.

The ticket-pricing thresholds are an explicit exercise assumption because the
workbook does not define them: child 0-12, teenager 13-17, adult 18-64, senior
65-120; values outside 0-120 and non-integer inputs are invalid.

## Run in PowerShell

From the repository root:

```powershell
.\.venv\Scripts\python.exe ".\Day 2 - Python Core for Testers\self_checks.py"
```

Expected result: `Self-checks: 8 passed`, followed by 20 mock checks and a
summary of 16 passed and 4 failed. The four mock failures are intentional
demonstration data, not failures of the self-checks.

## Verification record

Run from the deliverable folder with the repository virtual environment on
2026-10-26:

- Command: `..\\.venv\\Scripts\\python.exe self_checks.py`
- Exit code: 0
- Self-checks: 8 passed
- Mock summary: 16 passed, 4 intentionally failed

A passing self-check run verifies these specific examples; it does not
establish that the exercise covers every possible input or a real ticket-pricing
policy.
