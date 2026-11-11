# QE Learning Progress

States are separate: **Learned** reflects the learner's completed workbook day, **Implemented** reflects repository artifacts, **Verified** requires an execution or other evidence recorded below, and **Presentable** requires the learner to explain and demonstrate the work independently.

| Day | Topic | Learned | Implemented | Verified | Presentable | Evidence and remaining work |
|---|---|---|---|---|---|---|
| 1 | Git and GitHub setup | Yes | Yes | Yes | Pending self-demo | Repository history, conflict practice, and Day 1 guide are present. Independently demonstrate branch/PR workflow and secret handling. |
| 2 | Python core for testers | Yes | Yes | Yes | Pending self-demo | Day 2 guide records 8 self-checks passing and a mock summary of 16 pass / 4 intentional failures. Explain functions, assertions, BVA, and equivalence classes. |
| 3 | OOP, files, JSON/CSV | Yes | Yes | Yes | Pending self-demo | Day 3 guide records 10 cases round-tripped and 4 checks passing. Explain dataclasses and serialization choices. |
| 4 | SQL for testers | Yes | Yes | Yes | Pending self-demo | Day 4 guide records 12 queries and 5 seeded data issues detected. Explain a join and one integrity check. |
| 5 | HTTP/REST and Postman | Yes | Yes | Partial | Pending self-demo | Collection/environment JSON and embedded script syntax were checked; the collection has not been run in Postman. Capture and review an actual Runner result. |
| 6 | API automation with requests and pytest | Yes | Yes | Yes, with limitation | Pending self-demo | A prior network-enabled run recorded 15 passing API cases. The current sandbox baseline could not reach the demo API (`WinError 10013`); repeat the live run when network access is available. |
| 7 | Advanced pytest and data-driven testing | Yes | Yes | Yes, offline | Pending self-demo | 11 local cases passed; 19 live API cases were deselected; all 30 cases collected. Explain fixture scope, parametrization IDs, markers, teardown, and JUnit XML. |
| 8 | Playwright basics | Yes | Yes | Yes | Pending self-demo | 13 Playwright tests passed with Chromium. Explain locator choice, Decimal price comparison, auto-waiting, and trace/report use. |
| 9 | Playwright framework design | Yes | Yes | Yes | Pending self-demo | Page objects, isolated storage-state fixtures, API/UI hybrid demo, and worker-safe parallel runs are implemented; all 9 Day 9 tests passed. Explain why SauceDemo sessionStorage needs explicit restoration. |
| 10 | CI/CD with GitHub Actions | In progress | Yes | Partial, local only | Pending self-demo | Local Python 3.13 checks passed: Ruff, 17 offline tests, 19 API tests, and 28 Day 8/9 browser cases. Verify Ubuntu and Python 3.12 matrix jobs plus the status badge in the first hosted run. |
| 11 | Prompting for test design | In progress | Yes | Partial, samples validated | Pending learner walkthrough | Saved prompt, three-story v1/v2 comparison, rubric, sample outputs, and automated TestCase-contract checks are present. Examples use fictional stories and are explicitly not external-model runs. Workbook completion still requires replacing them with three approved, sanitized real stories and reviewing the results. |
| 12 | Advanced AI test design | In progress | Yes | Yes, locally | Pending learner walkthrough | Five prompts and eight-point checklist are present; core JSON Schema, duplicate, and traceability validators have 10 unit tests. Combined Day 12 and Day 11 contract checks: 13 passed; Ruff passed. Practice the five prompts on approved, sanitized requirements and review/override AI output. |

## Day 7 evidence

- Deliverable: `Day 7 - Advanced pytest and data-driven testing/README.md` and `test_pytest_patterns.py`.
- Framework configuration: root `pytest.ini` registers the API, smoke, regression, negative, CRUD, and data-driven markers.
- API test organization: `api-tests/test_booking_api.py` marks the core read checks as smoke and all API cases as regression. The suite uses a read-only module-scoped API configuration fixture; sessions, tokens, and test-created bookings remain function-scoped.
- Verification command: `.\.venv\Scripts\python.exe -m pytest -q "Day 7 - Advanced pytest and data-driven testing"`.
- Result: 11 passed. The all-offline selection also passed 11 and deselected 19 API cases. Collection found 30 cases, including the schema test and 3 CSV cases. XML report generation succeeded. Pytest printed a non-blocking cache warning because `.pytest_cache` is not writable in this sandbox.

## Next

1. Practice the five Day 12 prompts and review checklist on approved, sanitized requirements; explain the deterministic validator results and limitations.
2. Complete Day 11 by running prompt v1 and v2 on three approved real stories and reviewing the results.
3. Complete Day 10 by checking the hosted Ubuntu/Python matrix and status badge.
