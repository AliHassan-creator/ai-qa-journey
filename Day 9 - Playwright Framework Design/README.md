# Day 9: Playwright Framework Design

## Goal

Refactor the working Day 8 SauceDemo workflows into page objects and reusable pytest fixtures. This keeps page-specific selectors and actions out of the test cases.

## Framework structure

- `pages/base_page.py` — shared URL and browser-page behavior.
- `pages/login_page.py` — login controls, credentials, and login error alert.
- `pages/inventory_page.py` — product heading, add-to-cart action, and cart badge.
- `pages/cart_page.py` — cart heading and checkout action.
- `pages/checkout_page.py` — customer details, checkout validation, and order completion.
- `conftest.py` — shared selector setup and browser-state fixtures.
- `tests/test_framework_design.py` — tests that describe workflows using page objects.
- `demo_app.py` — local standard-library API and UI used for hybrid testing.
- `tests/test_api_ui_hybrid.py` — creates a record over HTTP and verifies the same record in the browser.
- `CODING_CONVENTIONS.md` — framework rules to carry into future AI assistant instructions.

## How the authenticated-state fixture works

1. `authenticated_state` creates one temporary browser context.
2. It logs in with the configured SauceDemo credentials and saves cookies/local storage to a temporary JSON file.
3. SauceDemo also keeps its login marker in `sessionStorage`, which Playwright's standard storage-state file does not include. The fixture captures that value separately.
4. Each test requesting `authenticated_page` creates its own isolated browser context, restores the standard state, and injects the saved session value before the app loads.
5. Each test can therefore start signed in without sharing cart state or page state with another test.

The state file is temporary and should not be committed. Do not store real personal accounts or sensitive credentials in a checked-in state file. Set `SAUCEDEMO_USER`, `SAUCEDEMO_PASSWORD`, or `SAUCEDEMO_BASE_URL` in the environment to override the demo defaults.

## Run the Day 9 tests

From the repository root in PowerShell:

```powershell
& ".\.venv\Scripts\python.exe" -m pytest ".\Day 9 - Playwright Framework Design\tests" -v --browser chromium --basetemp ".\.pytest_cache\day9-tmp"
```

Command breakdown:

- `&` tells PowerShell to execute the quoted program path.
- `.\.venv\Scripts\python.exe` uses this repository's Python environment.
- `-m pytest` runs pytest as a Python module from that environment.
- The quoted path after it selects all Day 9 test modules.
- `-v` prints each test name and its result.
- `--browser chromium` tells pytest-playwright to run the browser tests in Chromium.

The browser plugin and Chromium should already be installed from Day 8. If not, install the Day 8 requirements and the Chromium browser using the setup steps in the Day 8 README.

## Install parallel-run support

Install the base Playwright requirements from Day 8, then the Day 9 addition:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install -r ".\Day 8 - Playwright basics\requirements.txt" -r ".\Day 9 - Playwright Framework Design\requirements.txt"
```

The second requirements file adds `pytest-xdist`. The `-r` option tells pip to read package names from the specified requirements file.

## Run with failure artifacts

```powershell
New-Item -ItemType Directory -Force -Path ".\.pytest_cache\day9-playwright-temp" | Out-Null
$env:TEMP = (Resolve-Path ".\.pytest_cache\day9-playwright-temp").Path
$env:TMP = $env:TEMP
& ".\.venv\Scripts\python.exe" -m pytest ".\Day 9 - Playwright Framework Design\tests" -v --browser chromium --tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure --output ".\.pytest_cache\d9-artifacts" --basetemp ".\.pytest_cache\day9-tmp"
```

Command options:

- `--tracing retain-on-failure` keeps a Playwright trace only when a test fails.
- `--screenshot only-on-failure` captures a screenshot only for failed tests.
- `--video retain-on-failure` records browser video and keeps it only for failed tests.
- `--output` sets the directory for Playwright artifacts. Use a short path on Windows; the installed plugin now shortens each test folder based on the full destination path.
- `--basetemp` puts pytest's temporary files in the ignored project cache. This is useful on this Windows setup because the default user temp location denied access.

Verified on 2026-11-11 with a temporary intentional failure: all three files were retained together (`test-failed-1.png`, `trace.zip`, and `video.webm`) under `.pytest_cache/d9-artifacts/`. The temporary failing probe was then removed.

## Run in parallel

```powershell
& ".\.venv\Scripts\python.exe" -m pytest ".\Day 9 - Playwright Framework Design\tests" -v --browser chromium -n 2 --basetemp ".\.pytest_cache\day9-tmp"
```

`-n 2` asks pytest-xdist to run tests in two worker processes. Each worker gets its own authentication-state file under the ignored pytest cache. Each test still gets a fresh browser context, so cart state is not shared across tests. `--basetemp` also keeps pytest-xdist's worker temp folders out of the restricted Windows user temp location.

## Environment configuration

The page objects already read `SAUCEDEMO_BASE_URL`, `SAUCEDEMO_USER`, and `SAUCEDEMO_PASSWORD` from the process environment, falling back to the public SauceDemo training defaults. In PowerShell, set a variable for the current terminal session with `$env:NAME = "value"`; do not commit real credentials or storage-state files.

## API + UI hybrid test

SauceDemo has no supported API to create product or cart data, so it is not appropriate to send a record to an unrelated service and claim that the SauceDemo UI verified it. For practice, `demo_app.py` provides a small paired target on loopback using Python's standard library:

1. A pytest session fixture starts one local server per worker on an available port and waits for `/health`.
2. The test sends `POST /api/records` through Playwright's API request context and checks the `201` response and returned record.
3. The test opens `/records/<id>` in Chromium; that page fetches the same record from the API and renders its ID, title, and description.
4. The server process is stopped after the worker's session. Each worker has its own in-memory record store.

Run only the hybrid workflow:

```powershell
& ".\.venv\Scripts\python.exe" -m pytest ".\Day 9 - Playwright Framework Design\tests\test_api_ui_hybrid.py" -v --browser chromium --basetemp ".\.pytest_cache\day9-hybrid-tmp"
```

Command breakdown: `&` runs the specified executable in PowerShell; the venv's `python.exe` selects the project interpreter; `-m pytest` launches pytest; the quoted path selects this one test file; `-v` prints the test name and result; `--browser chromium` runs its UI portion in Chromium; and `--basetemp` keeps pytest temporary data under the ignored project cache.

## Current learning boundary

The POM, authenticated-state reuse, worker-safe parallel setup, environment-variable configuration, failure artifact options, coding conventions, and a local API-to-UI hybrid example are implemented. The local demo is a focused learning target, not a production application. SauceDemo-specific API-created shopping data remains unsupported by the public demo.
