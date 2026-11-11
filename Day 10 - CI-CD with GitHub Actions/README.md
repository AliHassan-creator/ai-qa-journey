# Day 10: CI/CD with GitHub Actions

## Learning objective

Automatically run appropriate quality checks when code changes, preserve reports for investigation, and expose the latest workflow result on the repository page.

## CI/CD terms

- **Continuous Integration (CI):** every push or pull request runs repeatable checks so defects are found before changes are merged.
- **Continuous Delivery/Deployment (CD):** after CI passes, changes can be prepared for release or automatically deployed. This day's workflow implements CI; it does not deploy an application.
- **Workflow:** a YAML automation definition stored under `.github/workflows/`. It declares events, permissions, and jobs.
- **Event:** what starts a workflow. Here, `push`, `pull_request`, a UTC `schedule`, or a manual `workflow_dispatch` can start it.
- **Job:** a group of steps on a runner. Jobs are isolated unless explicitly connected or sharing artifacts.
- **Step:** one command or reusable action inside a job.
- **Runner:** the temporary machine that executes a job. This workflow uses GitHub-hosted Ubuntu runners.
- **Matrix:** repeats a job for multiple values. The API job checks both Python 3.12 and 3.13.
- **Artifact:** an uploaded output such as JUnit XML, a trace, screenshot, or video. Artifacts remain downloadable after a temporary runner is removed; they are not source-code commits.
- **Secret:** a private value stored in the repository or organization Actions settings and referenced in workflow expressions. Never print secrets or commit them. The public training API credentials are public defaults, so this workflow needs no credential secrets. If a private API is substituted, add credentials under **Settings → Secrets and variables → Actions → New repository secret** and pass them through `secrets.NAME`.
- **Status badge:** a small image linked to the workflow page. It communicates the latest status for the selected branch; it is not proof that every test or environment has been covered.

## Workflow behavior

The workflow at `.github/workflows/ci.yml` has three jobs:

1. `api-tests`: runs marked API tests on pushes and pull requests, with a Python-version matrix. These tests use a shared public demo service, so availability and external network behavior can affect results. Optional `RESTFUL_BOOKER_BASE_URL`, `RESTFUL_BOOKER_USERNAME`, and `RESTFUL_BOOKER_PASSWORD` repository variables/secrets override the demo defaults.
2. `qa-copilot-checks`: runs Ruff linting and offline Day 7/runner unit tests. It does not need external API credentials or browser installation.
3. `playwright-tests`: runs browser suites on pull requests, scheduled runs, and manual runs. It installs Chromium and uploads the JUnit report plus failure artifacts even when the tests fail.

A scheduled run is set for 02:00 UTC every day. GitHub may delay scheduled workflows during high load. Use **Actions → QA CI → Run workflow** to start a manual run.

The workflow has read-only repository permissions. The API demo credentials are not secrets. Do not expose private secrets to untrusted pull-request code, especially pull requests from forks.

## Trigger and matrix breakdown

- `push.branches: [main]` runs lightweight API and offline checks when changes reach `main`.
- `pull_request.branches: [main]` runs all three jobs before a pull request is merged.
- `schedule.cron` starts the full workflow on a UTC schedule.
- `workflow_dispatch` adds a manual button in GitHub Actions.
- `matrix.python-version` creates two independent API jobs. `fail-fast: false` lets the other Python version finish if one version fails.
- `if` on the Playwright job keeps the more expensive browser run off normal pushes while retaining PR, scheduled, and manual coverage.

## Test reports and failure investigation

Open a workflow run, select a job, and download the artifact from its **Artifacts** section. API JUnit XML and self-contained HTML reports, plus Playwright JUnit XML/HTML and browser artifacts, are uploaded by steps that use `if: always()` so reports remain available when tests fail. Artifacts are retained for 14 days; they can be downloaded but are not part of the repository history.

If a browser test fails, download `playwright-reports-and-artifacts`, locate the test folder's `trace.zip`, and inspect it with Playwright Trace Viewer. Screenshots and videos are included when the pytest-playwright plugin captures them for a failure.

## Status badge

The root README badge points at the `main` branch. A green badge means the latest applicable workflow run passed; a red badge links to the run that needs investigation.

## Local equivalent

From the repository root in PowerShell, run the pieces separately to reproduce CI locally:

- Offline lint: `ruff check qa-copilot`
- Offline unit tests: `python -m pytest -q "Day 7 - Advanced pytest and data-driven testing" "Day 8 - Playwright basics/test_playwright_adapter.py"`
- API checks (needs internet): `python -m pytest api-tests -m api -v`
- Browser checks (needs Chromium and network to SauceDemo): see the Day 9 README command with Chromium and artifact options.

The GitHub runner uses Linux while the learning workstation uses Windows. A green Linux run is useful evidence, but it does not guarantee every Windows-specific behavior.

## Verification record

- **Implemented:** workflow, matrix, schedule/manual triggers, artifacts, and README badge.
- **Verified locally on Python 3.13/Windows:** workflow YAML parsed and expected triggers/jobs were present; Ruff passed; offline CI tests passed (17); API matrix job command passed all 19 live API cases and generated JUnit/HTML reports; combined browser job passed all 28 Day 8/9 cases and generated JUnit/HTML reports. Artifact capture was separately verified earlier.
- **Verified on GitHub:** pending first Actions run after push.
- **Still unverified:** the Python 3.12 matrix leg and Ubuntu-hosted behavior. Review them in the first GitHub Actions run before marking the day complete.
- **Remaining:** inspect the first CI run, fix any runner-specific failures, and confirm the badge renders from the GitHub repository page.
