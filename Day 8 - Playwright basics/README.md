# Day 8 Deliverable: Playwright Basics

## Workbook objectives

- Use Playwright with Python and pytest.
- Locate controls by role, accessible name, placeholder, and test ID.
- Rely on Playwright's action auto-waiting and retrying assertions instead of fixed sleeps.
- Generate a test draft with Codegen, then review and clean it up.
- Record a trace and use Trace Viewer to investigate a failure.

## Practical suite

`test_saucedemo.py` contains 11 live SauceDemo workflow cases: login form, valid and invalid login, locked-out user, cart add/remove, cart contents, required checkout data, and successful checkout. The invalid-login test is parameterized for missing username, missing password, and incorrect credentials. A twelfth, network-free browser check verifies that the custom `data-test` selector configuration works.

The tests use Playwright's pytest `page` fixture. Each case receives an isolated browser context; locators and `expect` assertions wait for the relevant UI state. No `time.sleep()` calls are used. A session fixture configures `data-test` as Playwright's test-ID attribute because SauceDemo uses `data-test`, not Playwright's default `data-testid`. Login failures are located by their accessible `alert` role. The demo credentials are public training credentials; optional `SAUCEDEMO_USER`, `SAUCEDEMO_PASSWORD`, and `SAUCEDEMO_BASE_URL` environment variables can override them.

The `qa-copilot/runner/playwright_adapter.py` file is the Day 8 capstone increment. It builds the pytest command, selects Chromium, enables failure traces/screenshots, writes JUnit and HTML reports, and accepts optional marker and headed-mode arguments.

## Environment setup

The Day 8 dependencies are listed separately so the existing API-test environment stays unchanged. From the repository root in PowerShell:

```powershell
python -m pip install -r ".\Day 8 - Playwright basics\requirements.txt"
python -m playwright install chromium
```

## Run tests and reports

Run just the browser suite:

```powershell
$runId = Get-Date -Format "yyyyMMdd-HHmmss"
python -m pytest ".\Day 8 - Playwright basics\test_saucedemo.py" -v --browser chromium --tracing retain-on-failure --screenshot only-on-failure --output ".\Day 8 - Playwright basics\reports\artifacts\$runId" --junitxml ".\Day 8 - Playwright basics\reports\day8-junit.xml" --html ".\Day 8 - Playwright basics\reports\day8-report.html" --self-contained-html
```

Or run it through the QA-Copilot adapter:

```powershell
python ".\qa-copilot\runner\playwright_adapter.py"
```

Show the browser while it runs:

```powershell
python ".\qa-copilot\runner\playwright_adapter.py" --headed
```

Generated HTML and JUnit reports go under `Day 8 - Playwright basics/reports/`. The adapter places each run's screenshots and traces in a unique subfolder under `reports/artifacts/` to avoid collisions with older results. To open a failure trace:

```powershell
python -m playwright show-trace ".\Day 8 - Playwright basics\reports\artifacts\<run-id>\<test-trace>.zip"
```

## Codegen practice

Record a login and add-to-cart flow:

```powershell
playwright codegen --target=python https://www.saucedemo.com
```

Treat generated code as a draft: replace brittle selectors with role or test-ID locators where appropriate, add meaningful assertions, remove duplicate steps, and never add fixed sleeps.

## Sorting exercise

`test_product_sorting_low_to_high_price` logs in, selects the low-to-high sort option, checks the selected option, and compares the displayed prices with a numerically sorted copy. Prices use `Decimal` so currency values are compared exactly rather than as binary floating-point numbers. Run this case with `python -m pytest "Day 8 - Playwright basics/test_saucedemo.py" -k sorting -v --browser chromium`.

## Verification status and limits

- **Learned:** In progress; start with the objectives above and the Day 8 workbook row.
- **Implemented:** Browser tests, the runner adapter, and the low-to-high product-sorting check are present.
- **Verified:** The learner reported a local run with 12 passing tests before the sorting check was added. Two adapter unit tests and the network-free `data-test` browser check also passed. The sorting check has not yet been run. An earlier sandbox follow-up could not reach SauceDemo (`net::ERR_NETWORK_ACCESS_DENIED`).
- **Presentable:** Pending your walkthrough and independent sorting test.

The initial browser run collected 11 cases: 2 passed and 9 failed due to incorrect locators. Those failures led to the `data-test` and `alert` locator updates above. The learner subsequently reported 12 passing tests locally. The new sorting case still needs its targeted run and a full suite run. The public demo site can also change or be temporarily unavailable.

The current Playwright Python installation docs list Windows 11+, Windows Server 2019+, or WSL as supported Windows environments. This project environment is Windows 10, so browser installation and runtime support must be confirmed locally; WSL or a supported Windows host may be needed.

## Reference documentation

- [Playwright Python installation and pytest](https://playwright.dev/python/docs/intro)
- [Locators and auto-waiting](https://playwright.dev/python/docs/locators)
- [Pytest plugin options, including traces and screenshots](https://playwright.dev/python/docs/test-runners)
- [Codegen](https://playwright.dev/python/docs/codegen)
- [Trace Viewer](https://playwright.dev/python/docs/trace-viewer)
