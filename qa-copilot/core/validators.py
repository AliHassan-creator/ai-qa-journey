"""Deterministic validators for human-reviewed QA-Copilot test-case output."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).parent / "schemas" / "test_case_output.schema.json"


@dataclass(frozen=True)
class ValidationIssue:
    """One actionable validation finding."""

    code: str
    message: str
    path: str = ""

    def as_dict(self) -> dict[str, str]:
        """Return a JSON-serializable representation."""
        return {"code": self.code, "message": self.message, "path": self.path}


def _load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as schema_file:
        return json.load(schema_file)


def _normalize_text(value: str) -> str:
    """Normalize whitespace and case for deterministic comparisons."""
    return re.sub(r"\s+", " ", value).strip().casefold()


def _case_records(test_cases: Sequence[Any]) -> list[Mapping[str, Any]]:
    """Convert mappings or TestCase-like dataclasses to mapping records."""
    records: list[Mapping[str, Any]] = []
    for case in test_cases:
        if isinstance(case, Mapping):
            records.append(case)
        elif hasattr(case, "__dataclass_fields__"):
            records.append(
                {
                    field_name: getattr(case, field_name)
                    for field_name in case.__dataclass_fields__
                }
            )
        else:
            records.append({})
    return records


def validate_schema(payload: Any) -> list[ValidationIssue]:
    """Validate the complete generated-output contract using JSON Schema."""
    validator = Draft202012Validator(_load_schema())
    errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [
        ValidationIssue(
            code="schema_violation",
            message=error.message,
            path="/" + "/".join(str(part) for part in error.absolute_path),
        )
        for error in errors
    ]


def validate_duplicates(test_cases: Sequence[Any]) -> list[ValidationIssue]:
    """Find repeated IDs and exact normalized case-content duplicates.

    The content check compares title, preconditions, ordered steps, and expected
    result. It intentionally does not claim semantic duplicate detection.
    """
    issues: list[ValidationIssue] = []
    id_locations: dict[str, list[int]] = defaultdict(list)
    content_locations: dict[tuple[str, ...], list[int]] = defaultdict(list)

    records = _case_records(test_cases)
    for index, case in enumerate(records):
        case_id = case.get("id")
        if isinstance(case_id, str) and case_id.strip():
            id_locations[case_id.strip()].append(index)

        title = case.get("title")
        preconditions = case.get("preconditions")
        steps = case.get("steps")
        expected = case.get("expected")
        if (
            isinstance(title, str)
            and isinstance(preconditions, str)
            and isinstance(steps, list)
            and all(isinstance(step, str) for step in steps)
            and isinstance(expected, str)
        ):
            signature = (
                _normalize_text(title),
                _normalize_text(preconditions),
                str(len(steps)),
                *(_normalize_text(step) for step in steps),
                _normalize_text(expected),
            )
            content_locations[signature].append(index)

    for case_id, indices in id_locations.items():
        if len(indices) > 1:
            issues.append(
                ValidationIssue(
                    code="duplicate_id",
                    message=f"Test case ID {case_id!r} is used more than once.",
                    path="/test_cases",
                )
            )

    for indices in content_locations.values():
        if len(indices) > 1:
            case_ids = [str(records[index].get("id", "<missing>")) for index in indices]
            issues.append(
                ValidationIssue(
                    code="duplicate_case",
                    message=(
                        "Cases have identical normalized title, preconditions, "
                        f"steps, and expected result: {', '.join(case_ids)}."
                    ),
                    path="/test_cases",
                )
            )

    return issues


def validate_traceability(
    test_cases: Sequence[Any],
    acceptance_criteria: Sequence[str],
    coverage_notes: Any,
) -> list[ValidationIssue]:
    """Check criterion coverage and case references in coverage notes."""
    issues: list[ValidationIssue] = []
    cases = _case_records(test_cases)
    case_ids = {
        case["id"].strip()
        for case in cases
        if isinstance(case.get("id"), str) and case["id"].strip()
    }

    if not isinstance(coverage_notes, list):
        return [
            ValidationIssue(
                code="invalid_coverage_notes",
                message="coverage_notes must be a list.",
                path="/coverage_notes",
            )
        ]

    criterion_lookup = {
        _normalize_text(criterion): criterion
        for criterion in acceptance_criteria
        if isinstance(criterion, str) and criterion.strip()
    }
    covered_criteria: set[str] = set()
    traced_case_ids: set[str] = set()
    note_criteria_seen: set[str] = set()

    for note_index, note in enumerate(coverage_notes):
        note_path = f"/coverage_notes/{note_index}"
        if not isinstance(note, Mapping):
            issues.append(
                ValidationIssue(
                    code="invalid_coverage_note",
                    message="Each coverage note must be an object.",
                    path=note_path,
                )
            )
            continue

        criterion = note.get("criterion")
        normalized_criterion = (
            _normalize_text(criterion) if isinstance(criterion, str) else ""
        )
        if normalized_criterion not in criterion_lookup:
            issues.append(
                ValidationIssue(
                    code="unknown_criterion",
                    message=f"Coverage note criterion {criterion!r} is not in the supplied acceptance criteria.",
                    path=f"{note_path}/criterion",
                )
            )
        else:
            if normalized_criterion in note_criteria_seen:
                issues.append(
                    ValidationIssue(
                        code="duplicate_criterion_note",
                        message=f"Acceptance criterion {criterion!r} has more than one coverage note.",
                        path=f"{note_path}/criterion",
                    )
                )
            note_criteria_seen.add(normalized_criterion)

        references = note.get("covered_by")
        if not isinstance(references, list):
            issues.append(
                ValidationIssue(
                    code="invalid_case_references",
                    message="covered_by must be a list of test case IDs.",
                    path=f"{note_path}/covered_by",
                )
            )
            continue

        valid_references = 0
        for reference_index, reference in enumerate(references):
            if not isinstance(reference, str) or reference not in case_ids:
                issues.append(
                    ValidationIssue(
                        code="unknown_case_reference",
                        message=f"Coverage note references unknown test case ID {reference!r}.",
                        path=f"{note_path}/covered_by/{reference_index}",
                    )
                )
            else:
                traced_case_ids.add(reference)
                valid_references += 1

        if normalized_criterion in criterion_lookup and valid_references:
            covered_criteria.add(normalized_criterion)

    for normalized, criterion in criterion_lookup.items():
        if normalized not in covered_criteria:
            issues.append(
                ValidationIssue(
                    code="uncovered_criterion",
                    message=f"Acceptance criterion {criterion!r} has no coverage note.",
                    path="/coverage_notes",
                )
            )

    for case_id in sorted(case_ids - traced_case_ids):
        issues.append(
            ValidationIssue(
                code="untraceable_test_case",
                message=f"Test case {case_id!r} is not linked to any acceptance criterion.",
                path="/coverage_notes",
            )
        )

    return issues


def validate_test_case_output(
    payload: Any,
    acceptance_criteria: Sequence[str],
) -> list[ValidationIssue]:
    """Run schema, duplicate, and traceability checks on one output object."""
    schema_issues = validate_schema(payload)
    if schema_issues or not isinstance(payload, Mapping):
        return schema_issues

    test_cases = payload["test_cases"]
    return [
        *validate_duplicates(test_cases),
        *validate_traceability(
            test_cases,
            acceptance_criteria,
            payload["coverage_notes"],
        ),
    ]
