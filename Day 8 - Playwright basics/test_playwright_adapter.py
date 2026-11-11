import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_DIR = PROJECT_ROOT / "qa-copilot" / "runner"
sys.path.insert(0, str(ADAPTER_DIR))

from playwright_adapter import build_pytest_command


def test_adapter_builds_headless_chromium_report_command():
    command = build_pytest_command(run_id="unit-test-run")

    assert command[0:3] == [sys.executable, "-m", "pytest"]
    assert "--browser=chromium" in command
    assert "--tracing=retain-on-failure" in command
    assert any(arg.endswith("day8-junit.xml") for arg in command)
    assert any(arg.endswith("day8-report.html") for arg in command)
    output_argument = next(arg for arg in command if arg.startswith("--output="))
    assert Path(output_argument.split("=", 1)[1]).name == "unit-test-run"
    assert "--headed" not in command


def test_adapter_passes_marker_and_headed_options():
    command = build_pytest_command(marker="ui", headed=True)

    assert command[-3:] == ["-m", "ui", "--headed"]
