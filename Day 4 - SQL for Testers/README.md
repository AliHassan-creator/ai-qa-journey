# Day 4 Deliverable: SQL for Testers

## Learning objectives

- Practice filtering, sorting, pattern matching, aggregates, grouping, and joins.
- Use SQL checks to find inconsistent or orphaned data.
- Run the exercises against SQLite from Python's built-in `sqlite3` module.

## Files

- [`sql_exercises.sql`](sql_exercises.sql): 12 SELECT exercises, including a three-table join and `GROUP BY`/`HAVING`.
- [`sample_orders.sql`](sample_orders.sql): creates and seeds a small fictional orders database in memory.
- [`run_checks.py`](run_checks.py): runs all 12 queries and five validation checks.

The seed data intentionally contains one example each of a mismatched order
total, an orphan order item, a duplicate customer email, an order without line
items, and a non-positive item quantity. The runner treats detecting these
known issues as a successful verification of the checks. No database server or
additional package is required.

## Run in PowerShell

From the repository root:

```powershell
python ".\Day 4 - SQL for Testers\run_checks.py"
```

## Verification record

Run from the deliverable folder with the repository virtual environment on
2026-10-26:

- Command: `..\\.venv\\Scripts\\python.exe run_checks.py`
- Exit code: 0
- SQL exercises executed: 12
- Seeded data-quality issues detected as expected: 5

A passing run verifies the queries and checks against this small, deliberately
seeded sample database. It does not prove that the checks fit a real production
database schema.
