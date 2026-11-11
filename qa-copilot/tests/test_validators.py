"""Unit tests for deterministic QA-Copilot output validators."""

import sys
from pathlib import Path

QA_COPILOT_DIR = Path(__file__).resolve().parents[1]
if str(QA_COPILOT_DIR) not in sys.path:
    sys.path.insert(0, str(QA_COPILOT_DIR))

from core.validators import (
    validate_duplicates,
    validate_schema,
    validate_test_case_output,
    validate_traceability,
)


def make_case(case_id="TC-001", title="Submit valid form", steps=None, expected="Success"):
    return {
        "id": case_id,
        "title": title,
        "preconditions": "The form is open.",
        "steps": steps or ["Enter valid data", "Submit the form"],
        "expected": expected,
        "priority": "high",
        "type": "functional",
    }


def make_output(test_cases=None, coverage_notes=None):
    test_cases = test_cases or [make_case()]
    criteria = ["AC1: A valid submission succeeds."]
    return {
        "test_cases": test_cases,
        "priority_rationales": [
            {"id": case["id"], "rationale": "High impact; likelihood is unassessed."}
            for case in test_cases
        ],
        "assumptions": [],
        "open_questions": [],
        "coverage_notes": coverage_notes
        if coverage_notes is not None
        else [{"criterion": criteria[0], "covered_by": [case["id"] for case in test_cases], "gaps": []}],
    }


def test_schema_accepts_valid_output():
    assert validate_schema(make_output()) == []


def test_schema_rejects_invalid_priority_and_extra_case_field():
    output = make_output()
    output["test_cases"][0]["priority"] = "urgent"
    output["test_cases"][0]["new_behavior"] = "invented"

    issues = validate_schema(output)

    assert issues
    assert all(issue.code == "schema_violation" for issue in issues)


def test_schema_requires_every_top_level_contract_field():
    output = make_output()
    del output["coverage_notes"]

    issues = validate_schema(output)

    assert any("coverage_notes" in issue.message for issue in issues)


def test_duplicate_validator_finds_reused_id_and_exact_normalized_case():
    first = make_case(case_id="TC-001")
    identical_with_whitespace_changes = make_case(
        case_id="TC-001",
        title="  SUBMIT   VALID FORM ",
        steps=[" enter valid data ", "SUBMIT the form"],
        expected=" success ",
    )

    issues = validate_duplicates([first, identical_with_whitespace_changes])

    assert {issue.code for issue in issues} == {"duplicate_id", "duplicate_case"}


def test_duplicate_validator_keeps_distinct_expected_behaviors():
    first = make_case(case_id="TC-001")
    second = make_case(
        case_id="TC-002",
        title=first["title"],
        steps=["Enter invalid data", "Submit the form"],
        expected="Validation error is shown",
    )

    assert validate_duplicates([first, second]) == []


def test_traceability_finds_uncovered_criterion_unknown_case_and_untraced_case():
    cases = [make_case(), make_case(case_id="TC-002", title="Second behavior")]
    criteria = ["AC1: A valid submission succeeds.", "AC2: An invalid submission is rejected."]
    coverage = [
        {"criterion": criteria[0], "covered_by": ["TC-404"], "gaps": []}
    ]

    issues = validate_traceability(cases, criteria, coverage)

    assert {issue.code for issue in issues} == {
        "unknown_case_reference",
        "uncovered_criterion",
        "untraceable_test_case",
    }


def test_traceability_requires_at_least_one_valid_case_per_criterion():
    cases = [make_case()]
    criteria = ["AC1: A valid submission succeeds."]
    coverage = [{"criterion": criteria[0], "covered_by": [], "gaps": []}]

    issues = validate_traceability(cases, criteria, coverage)

    assert {issue.code for issue in issues} == {"uncovered_criterion", "untraceable_test_case"}


def test_traceability_flags_criterion_not_in_requirement_list():
    cases = [make_case()]
    coverage = [{"criterion": "AC9: Unprovided criterion.", "covered_by": ["TC-001"], "gaps": []}]

    issues = validate_traceability(cases, ["AC1: A valid submission succeeds."], coverage)

    assert {issue.code for issue in issues} == {"unknown_criterion", "uncovered_criterion"}


def test_combined_validator_accepts_complete_traceable_output():
    criteria = ["AC1: A valid submission succeeds."]
    output = make_output()

    assert validate_test_case_output(output, criteria) == []


def test_combined_validator_rejects_schema_before_semantic_checks():
    output = make_output()
    output["test_cases"][0]["priority"] = "urgent"

    issues = validate_test_case_output(output, ["AC1: A valid submission succeeds."])

    assert issues
    assert all(issue.code == "schema_violation" for issue in issues)
