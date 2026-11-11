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
| 8 | Playwright basics | In progress | Yes | Partial | Pending self-demo | The learner reported 12 local tests passing after the locator fixes. A low-to-high price sorting test has now been added, bringing the expected suite total to 13; that new case and the updated full suite still need to be run. Explain locator choice, Decimal price comparison, auto-waiting, and trace/report use. |

## Day 7 evidence

- Deliverable: `Day 7 - Advanced pytest and data-driven testing/README.md` and `test_pytest_patterns.py`.
- Framework configuration: root `pytest.ini` registers the API, smoke, regression, negative, CRUD, and data-driven markers.
- API test organization: `api-tests/test_booking_api.py` marks the core read checks as smoke and all API cases as regression. The suite uses a read-only module-scoped API configuration fixture; sessions, tokens, and test-created bookings remain function-scoped.
- Verification command: `.\.venv\Scripts\python.exe -m pytest -q "Day 7 - Advanced pytest and data-driven testing"`.
- Result: 11 passed. The all-offline selection also passed 11 and deselected 19 API cases. Collection found 30 cases, including the schema test and 3 CSV cases. XML report generation succeeded. Pytest printed a non-blocking cache warning because `.pytest_cache` is not writable in this sandbox.

## Next

1. Run the marked API selections and full report command in PowerShell with network access; compare the external-service results with the recorded sandbox limitation.
2. Walk through one session fixture, one function fixture with teardown, and a parametrized test without reading the guide.
3. Continue with Day 8 only after the Day 7 walkthrough and any live API verification desired by the learner.
