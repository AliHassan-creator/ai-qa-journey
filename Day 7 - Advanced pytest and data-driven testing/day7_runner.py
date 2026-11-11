import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

DAY7_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DAY7_DIR.parent
REPORTS_DIR = DAY7_DIR / "reports"
XML_REPORT = REPORTS_DIR / "day7-junit.xml"
HTML_REPORT = REPORTS_DIR / "day7-report.html"
JSON_REPORT = REPORTS_DIR / "day7-summary.json"


def parse_junit_report(xml_path):
    """Parse JUnit XML and return normalized test results."""
    root = ET.parse(xml_path).getroot()

    test_cases = root.findall(".//testcase")

    results = {
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "summed_test_duration_seconds": 0.0,
        "test_cases": [],
    }

    for case in test_cases:
        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")

        if failure is not None:
            status = "failed"
            details = failure.get("message") or failure.text
            results["failed"] += 1
        elif error is not None:
            status = "error"
            details = error.get("message") or error.text
            results["errors"] += 1
        elif skipped is not None:
            status = "skipped"
            details = skipped.get("message") or skipped.text
            results["skipped"] += 1
        else:
            status = "passed"
            details = None
            results["passed"] += 1

        try:
            duration = float(case.get("time", "0"))
        except (TypeError, ValueError):
            duration = 0.0

        results["summed_test_duration_seconds"] += duration

        results["test_cases"].append(
            {
                "name": case.get("name", "unknown"),
                "classname": case.get("classname", ""),
                "status": status,
                "duration_seconds": duration,
                "details": details,
            }
        )

    results["summed_test_duration_seconds"] = round(
        results["summed_test_duration_seconds"], 3
    )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Run the API test suite and generate Day 7 reports."
    )
    parser.add_argument(
        "--marker",
        "-m",
        help=(
            "Optional pytest marker expression, such as 'regression' or "
            "'smoke'. By default, run all API tests."
        ),
    )
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "pytest",
        str(PROJECT_ROOT / "api-tests"),
        f"--junitxml={XML_REPORT}",
        f"--html={HTML_REPORT}",
        "--self-contained-html",
        "-v",
    ]
    if args.marker:
        command.extend(["-m", args.marker])

    selection = f" selected by marker '{args.marker}'" if args.marker else ""
    print(f"Running API tests{selection}...\n")

    test_run = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=False,
    )

    if not XML_REPORT.exists():
        print("ERROR: Pytest did not generate the JUnit XML report.")
        return test_run.returncode or 1

    try:
        results = parse_junit_report(XML_REPORT)
    except (ET.ParseError, OSError) as exc:
        print(f"ERROR: Could not parse the JUnit XML report: {exc}")
        return 1

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pytest_exit_code": test_run.returncode,
        "results": results,
    }

    JSON_REPORT.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print("\nNormalized test summary:")
    print(json.dumps(summary, indent=2))
    print(f"\nJSON report saved to: {JSON_REPORT}")

    return test_run.returncode


if __name__ == "__main__":
    raise SystemExit(main())
