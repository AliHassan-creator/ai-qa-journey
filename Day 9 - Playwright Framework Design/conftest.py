import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import Browser

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session", autouse=True)
def configure_saucedemo_test_id_attribute(playwright):
    """Use SauceDemo's data-test attributes with Playwright test IDs."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def authenticated_state(browser: Browser, request, configure_saucedemo_test_id_attribute):
    """Log in once and save the browser storage state for later tests."""
    _ = configure_saucedemo_test_id_attribute
    from pages.login_page import LoginPage

    worker_id = getattr(request.config, "workerinput", {}).get("workerid", "master")
    state_directory = ROOT.parent / ".pytest_cache" / "day9-auth" / worker_id
    state_directory.mkdir(parents=True, exist_ok=True)
    state_path = state_directory / "saucedemo-auth.json"
    context = browser.new_context()
    page = context.new_page()
    try:
        LoginPage(page).open().login()
        page.wait_for_url("**/inventory.html")
        context.storage_state(path=state_path)
        session_storage = page.evaluate(
            "() => Object.fromEntries(Object.entries(sessionStorage))"
        )
    finally:
        context.close()

    try:
        yield state_path, session_storage
    finally:
        state_path.unlink(missing_ok=True)
        state_directory.rmdir()


@pytest.fixture
def authenticated_page(browser: Browser, authenticated_state):
    """Provide a clean page that starts with the saved authenticated state."""
    from pages.login_page import LoginPage

    state_path, session_storage = authenticated_state
    context = browser.new_context(storage_state=state_path)
    session_storage_json = json.dumps(session_storage)
    context.add_init_script(
        f"""(() => {{
            const savedSession = {session_storage_json};
            for (const [key, value] of Object.entries(savedSession)) {{
                sessionStorage.setItem(key, value);
            }}
        }})();"""
    )
    page = context.new_page()
    page.goto(f"{LoginPage.BASE_URL}/inventory.html")
    yield page
    context.close()


@pytest.fixture(scope="session")
def demo_base_url():
    """Start an isolated local API/UI demo server for this pytest worker."""
    with socket.socket() as port_socket:
        port_socket.bind(("127.0.0.1", 0))
        port = port_socket.getsockname()[1]

    server_script = ROOT / "demo_app.py"
    process = subprocess.Popen(
        [sys.executable, str(server_script), "--port", str(port)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"
    health_url = f"{base_url}/health"
    deadline = time.monotonic() + 10

    while time.monotonic() < deadline:
        if process.poll() is not None:
            pytest.fail("The local API/UI demo server stopped during startup.")
        try:
            with urllib.request.urlopen(health_url, timeout=0.5) as response:
                if response.status == 200:
                    break
        except OSError:
            time.sleep(0.1)
    else:
        process.terminate()
        pytest.fail("The local API/UI demo server did not become ready in 10 seconds.")

    yield base_url

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


@pytest.fixture
def demo_api(playwright, demo_base_url):
    """Create a Playwright API context connected to the local demo app."""
    api_context = playwright.request.new_context(base_url=demo_base_url)
    yield api_context
    api_context.dispose()
