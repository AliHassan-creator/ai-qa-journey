"""Validate Day 11 prompt examples against the existing Day 3 TestCase model."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DAY3_DIR = PROJECT_ROOT / "Day 3 - OOP, JSON and CSV"
TESTCASE_MODULE_SPEC = importlib.util.spec_from_file_location(
    "day3_testcase",
    DAY3_DIR / "testcase.py",
)
if TESTCASE_MODULE_SPEC is None or TESTCASE_MODULE_SPEC.loader is None:
    raise RuntimeError("Could not load the Day 3 TestCase model.")
TESTCASE_MODULE = importlib.util.module_from_spec(TESTCASE_MODULE_SPEC)
sys.modules[TESTCASE_MODULE_SPEC.name] = TESTCASE_MODULE
TESTCASE_MODULE_SPEC.loader.exec_module(TESTCASE_MODULE)
CaseModel = TESTCASE_MODULE.TestCase

DAY11_DIR = Path(__file__).resolve().parent
SAMPLE_FILES = [
    "sample_login_v2_output.json",
    "sample_payment_v2_output.json",
    "sample_search_v2_output.json",
]
TOP_LEVEL_KEYS = {
    "test_cases",
    "priority_rationales",
    "assumptions",
    "open_questions",
    "coverage_notes",
}
CASE_KEYS = {
    "id",
    "title",
    "preconditions",
    "steps",
    "expected",
    "priority",
    "type",
}
PRIORITIES = {"critical", "high", "medium", "low"}
TYPES = {"functional", "negative", "boundary", "security", "usability", "compatibility"}


@pytest.mark.parametrize("sample_file", SAMPLE_FILES)
def test_prompt_output_matches_day3_test_case_contract(sample_file):
    output = json.loads((DAY11_DIR / sample_file).read_text(encoding="utf-8"))

    assert set(output) == TOP_LEVEL_KEYS
    assert isinstance(output["test_cases"], list) and output["test_cases"]

    cases = []
    for record in output["test_cases"]:
        assert set(record) == CASE_KEYS
        assert record["priority"] in PRIORITIES
        assert record["type"] in TYPES
        cases.append(CaseModel.from_record(record))

    case_ids = {case.id for case in cases}
    rationale_ids = [item["id"] for item in output["priority_rationales"]]
    assert len(rationale_ids) == len(set(rationale_ids))
    assert set(rationale_ids) == case_ids
    assert all(item["rationale"].strip() for item in output["priority_rationales"])

    for note in output["coverage_notes"]:
        assert note["criterion"].strip()
        assert set(note["covered_by"]) <= case_ids
        assert all(isinstance(gap, str) for gap in note["gaps"])

    assert all(isinstance(item, str) for item in output["assumptions"])
    assert all(isinstance(item, str) for item in output["open_questions"])
