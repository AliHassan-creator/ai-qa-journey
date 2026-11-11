# Day 7 Deliverable: Advanced pytest and Data-Driven Testing

## Learning objectives

- Choose fixture scope based on how long the resource can safely be shared.
- Use parameterization to check several values with one focused test.
- Use registered markers to select test categories.
- Set up and clean up a temporary test resource with a yield fixture.
- Generate HTML, JUnit XML, and JSON summary reports for review and CI readers.

## What this adds

- `test_pytest_patterns.py` contains deterministic, offline examples: a session-scoped context, a module-scoped sample, a function-scoped temporary JSON file with teardown, parameterized status-family checks, and invalid-input checks.
- `pytest.ini` registers `api`, `smoke`, `regression`, `negative`, `crud`, and `data_driven` markers.
- `api-tests/test_booking_api.py` uses those markers to make external API tests selectable and has a module-scoped, read-only configuration fixture. Its function-scoped session, authentication token, and booking factory keep API state isolated.
- `api-tests/data/booking_id_cases.csv` supplies inputs for the API test that demonstrates CSV-driven parameterization.

The API configuration is read once per test module because it is stable for a test run. Fixtures that authenticate, hold a session, or create booking data remain function-scoped so tests do not share mutable remote state. The session fixture in the local exercise also holds only stable context, which is safe to reuse.

## Run from the repository root in PowerShell

Run just the offline Day 7 exercises:

```powershell
.\.venv\Scripts\python.exe -m pytest -q ".\Day 7 - Advanced pytest and data-driven testing"
```

Run all offline tests while excluding requests to the external API:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -m "not api"
```

Run the critical API smoke checks (requires network access to Restful Booker):

```powershell
.\.venv\Scripts\python.exe -m pytest -q -m "api and smoke"
```

Run the broader API regression suite (requires network access to Restful Booker):

```powershell
.\.venv\Scripts\python.exe -m pytest -q -m "api and regression"
```

Select only API negative tests (requires network access to Restful Booker):

```powershell
.\.venv\Scripts\python.exe -m pytest -q -m "api and negative"
```

Run the full suite and write a JUnit XML report (the report path is ignored by Git):

```powershell
.\.venv\Scripts\python.exe -m pytest -q --junitxml="api-tests/report.xml"
```

Run the API suite through the Day 7 runner and generate all three reports:

```powershell
.\.venv\Scripts\python.exe ".\Day 7 - Advanced pytest and data-driven testing\day7_runner.py"
```

Run only API tests marked as regression:

```powershell
.\.venv\Scripts\python.exe ".\Day 7 - Advanced pytest and data-driven testing\day7_runner.py" --marker regression
```

Run only the critical smoke tests:

```powershell
.\.venv\Scripts\python.exe ".\Day 7 - Advanced pytest and data-driven testing\day7_runner.py" --marker smoke
```

The two core GET checks are marked `smoke` only. The other 17 API cases are marked `regression`, including boundary, authentication, schema, and CRUD coverage. This keeps the smoke and regression selections distinct.

The runner writes its reports into `Day 7 - Advanced pytest and data-driven testing/reports/`:

- `day7-report.html` — browser-readable pytest report.
- `day7-junit.xml` — JUnit XML for CI integrations.
- `day7-summary.json` — normalized counts and per-test outcomes.

The API tests contact the public Restful Booker service, so report outcomes depend on that service and network access.

To see fixture setup and teardown output for the temporary-file example:

```powershell
.\.venv\Scripts\python.exe -m pytest --setup-show ".\Day 7 - Advanced pytest and data-driven testing"
```

## Verification record

The Day 7 exercise suite passed: **11 passed**. Running `-m "not api"` also passed all 11 local cases and deselected the 19 external API cases. After adding the module-scoped API configuration, CSV-driven examples, and schema check, collection found 30 total cases, including 9 marked API and data-driven. JUnit XML was generated at `api-tests/report.xml` from the offline selection. Pytest emitted one cache warning because this environment cannot write to `.pytest_cache`; it did not affect test execution or the report.

The baseline full suite was attempted before Day 7 changes. The sandbox blocked outbound HTTPS to Restful Booker with `WinError 10013`, producing 7 request failures and 8 fixture setup errors; this run does not establish the API's current behavior. Re-run the full suite in an environment that can reach the demo API to verify its live tests.

## Progress states

- **Learned:** Day 7 topics are on the workbook tracker; this deliverable explains the fixture, parameterization, marker, teardown, selection, and reporting choices.
- **Implemented:** Yes; see the three files listed above.
- **Verified:** Yes; 11 local exercise cases passed, 19 external API cases were deselected, 30 total cases collected, and an offline JUnit report was generated.
- **Presentable:** Pending your own walkthrough of fixture scope and why remote booking fixtures stay function-scoped.

## Limits

The local examples verify pytest mechanics without the network. The API tests still depend on a shared public demo service, and JUnit XML reports test outcomes rather than proving production quality.
