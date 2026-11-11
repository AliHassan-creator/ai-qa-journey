"""Run the Day 8 browser suite with standard pytest-playwright options."""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DAY8_DIR = PROJECT_ROOT / "Day 8 - Playwright basics"
TEST_FILE = DAY8_DIR / "test_saucedemo.py"
REPORTS_DIR = DAY8_DIR / "reports"


def build_pytest_command(marker=None, headed=False, run_id=None):
    """Build a reproducible pytest command for the browser test suite."""
    run_id = run_id or datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    artifacts_dir = REPORTS_DIR / "artifacts" / run_id
    command = [
        sys.executable,
        "-m",
        "pytest",
        str(TEST_FILE),
        "--browser=chromium",
        "--tracing=retain-on-failure",
        "--screenshot=only-on-failure",
        f"--output={artifacts_dir}",
        f"--junitxml={REPORTS_DIR / 'day8-junit.xml'}",
        f"--html={REPORTS_DIR / 'day8-report.html'}",
        "--self-contained-html",
    ]
    if marker:
        command.extend(["-m", marker])
    if headed:
        command.append("--headed")
    return command


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--marker", "-m", help="Optional pytest marker expression, such as ui.")
    parser.add_argument("--headed", action="store_true", help="Show the Chromium window while tests run.")
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    command = build_pytest_command(marker=args.marker, headed=args.headed)
    return subprocess.run(command, cwd=PROJECT_ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
