# Playwright Python Coding Conventions

These conventions apply to the Day 9 framework and can later be adapted into repository-level AI assistant instructions.

## Test design

- Name tests `test_<behavior>_<expected_result>` and test one observable behavior at a time.
- Keep test functions focused on workflow and assertions; put page-specific selectors and actions in page objects.
- Use pytest parametrization for related input variations, with readable case IDs.
- Mark browser tests with `@pytest.mark.ui`; keep API and UI tests distinguishable by markers.
- Assert user-visible behavior and outcomes, not implementation details that users cannot observe.

## Playwright locators and synchronization

- Prefer accessible locators: role and accessible name, label, and placeholder.
- Use the application's stable test-ID attribute when semantic locators are unavailable; SauceDemo uses `data-test`.
- Do not use positional selectors, brittle CSS chains, or fixed sleeps as a first choice.
- Use Playwright actions and web-first `expect` assertions for synchronization; do not add `time.sleep()`.

## Page objects

- Use one page-object class per meaningful page or workflow boundary.
- Keep locators close to the page object that owns them.
- Expose intent-revealing actions such as `login()` and `add_backpack_to_cart()` rather than raw locator details.
- Return the next page object when an action changes pages; avoid making page objects hold test assertions.
- Share only genuinely common behavior in `BasePage`.

## Fixtures and test isolation

- Use pytest fixtures for browser setup and reusable test state.
- Give each test its own browser context; do not share mutable cart or page state between tests.
- Keep session-level setup read-only or explicitly isolated, and make any worker-created files unique per worker.
- Close contexts in fixture teardown, including when setup or assertions fail.
- Use Playwright `storage_state` only for test accounts and keep generated state files out of version control. Restore app-specific state, such as `sessionStorage`, explicitly when required.

## Configuration and security

- Read base URLs and credentials from environment variables, with safe public demo defaults only where appropriate.
- Never commit secrets, personal credentials, or authenticated state files.
- Keep environment-specific values out of page-object selectors and test assertions.

## Reporting and maintenance

- Capture traces, screenshots, and video on failure; store outputs in ignored report directories.
- Use unique output paths when running workers or repeated local runs to avoid artifact collisions.
- Keep test data deterministic and clean up records created against a shared demo service.
- Update this guide when the framework makes a deliberate exception; do not silently weaken assertions or selectors to make a test pass.
