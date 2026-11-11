import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace

import pytest

import day7_runner
from day7_runner import parse_junit_report


@pytest.fixture
def sample_dir():
    """Create test files inside the project, where the runner has write access."""
    fixture_dir = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="pytest-sample-", dir=fixture_dir) as temp_dir:
        yield Path(temp_dir)


def test_parser_counts_passed_failed_and_skipped_tests(sample_dir):
    xml_content = """\
    <testsuites>
        <testsuite name="sample" tests="4" failures="1" errors="1" skipped="1">
            <testcase classname="sample" name="test_pass" time="0.10" />
            <testcase classname="sample" name="test_failure" time="0.20">
                <failure message="Assertion failed">Expected 200</failure>
            </testcase>
            <testcase classname="sample" name="test_error" time="0.30">
                <error message="Unexpected exception">RuntimeError</error>
            </testcase>
            <testcase classname="sample" name="test_skip" time="0.05">
                <skipped message="Not applicable" />
            </testcase>
        </testsuite>
    </testsuites>
    """

    xml_file = sample_dir / "sample-results.xml"
    xml_file.write_text(xml_content, encoding="utf-8")

    results = parse_junit_report(xml_file)

    assert results["total"] == 4
    assert results["passed"] == 1
    assert results["failed"] == 1
    assert results["errors"] == 1
    assert results["skipped"] == 1

    assert results["test_cases"][0]["status"] == "passed"
    assert results["test_cases"][1]["status"] == "failed"
    assert results["test_cases"][2]["status"] == "error"
    assert results["test_cases"][3]["status"] == "skipped"


def test_parser_handles_all_passing_tests(sample_dir):
    xml_content = """\
    <testsuite name="sample" tests="2" failures="0" errors="0">
        <testcase classname="sample" name="test_one" time="0.10" />
        <testcase classname="sample" name="test_two" time="0.20" />
    </testsuite>
    """

    xml_file = sample_dir / "passing-results.xml"
    xml_file.write_text(xml_content, encoding="utf-8")

    results = parse_junit_report(xml_file)

    assert results["total"] == 2
    assert results["passed"] == 2
    assert results["failed"] == 0
    assert results["errors"] == 0
    assert results["skipped"] == 0
    assert results["summed_test_duration_seconds"] == 0.3

def test_parser_rejects_malformed_xml(sample_dir):
    xml_file = sample_dir / "malformed.xml"
    xml_file.write_text(
        "<testsuite><testcase></testsuite>",
        encoding="utf-8",
    )

    with pytest.raises(ET.ParseError):
        parse_junit_report(xml_file)


def test_runner_passes_marker_expression_to_pytest(sample_dir, monkeypatch, capsys):
    reports_dir = sample_dir / "reports"
    xml_report = reports_dir / "day7-junit.xml"
    html_report = reports_dir / "day7-report.html"
    json_report = reports_dir / "day7-summary.json"
    captured = {}

    def fake_run(command, cwd, check):
        captured["command"] = command
        xml_argument = next(arg for arg in command if arg.startswith("--junitxml="))
        Path(xml_argument.split("=", 1)[1]).write_text(
            '<testsuite tests="0"/>',
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(day7_runner, "REPORTS_DIR", reports_dir)
    monkeypatch.setattr(day7_runner, "XML_REPORT", xml_report)
    monkeypatch.setattr(day7_runner, "HTML_REPORT", html_report)
    monkeypatch.setattr(day7_runner, "JSON_REPORT", json_report)
    monkeypatch.setattr(day7_runner.subprocess, "run", fake_run)
    monkeypatch.setattr(
        day7_runner.sys,
        "argv",
        ["day7_runner.py", "--marker", "regression"],
    )

    assert day7_runner.main() == 0
    assert captured["command"][-2:] == ["-m", "regression"]
    assert json_report.exists()
    capsys.readouterr()
