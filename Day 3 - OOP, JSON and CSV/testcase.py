"""Load sanitized test cases from CSV and export them as JSON."""

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


@dataclass
class TestCase:
    """A manual test case with the fields specified in the learning plan."""

    id: str
    title: str
    preconditions: str
    steps: list[str]
    expected: str
    priority: str
    type: str

    def __post_init__(self) -> None:
        required_text = {
            "id": self.id,
            "title": self.title,
            "expected": self.expected,
            "priority": self.priority,
            "type": self.type,
        }
        for field_name, value in required_text.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.preconditions, str):
            raise TypeError("preconditions must be a string")
        if not isinstance(self.steps, list) or not self.steps:
            raise ValueError("steps must be a non-empty list")
        if not all(isinstance(step, str) and step.strip() for step in self.steps):
            raise ValueError("each step must be a non-empty string")

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "TestCase":
        """Build a case from a CSV or JSON record."""
        data = dict(record)
        steps = data.get("steps")
        if isinstance(steps, str):
            data["steps"] = json.loads(steps)
        return cls(**data)


def load_csv(file_path: Path) -> list[TestCase]:
    """Read test cases from a CSV file whose steps cell contains a JSON list."""
    with file_path.open("r", newline="", encoding="utf-8") as source:
        return [TestCase.from_record(row) for row in csv.DictReader(source)]


def save_csv(cases: list[TestCase], file_path: Path) -> None:
    """Write test cases to CSV, encoding each steps list as JSON."""
    fieldnames = ["id", "title", "preconditions", "steps", "expected", "priority", "type"]
    with file_path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        for case in cases:
            record = asdict(case)
            record["steps"] = json.dumps(case.steps, ensure_ascii=False)
            writer.writerow(record)


def load_json(file_path: Path) -> list[TestCase]:
    """Read a JSON array of test-case records."""
    with file_path.open("r", encoding="utf-8") as source:
        records = json.load(source)
    if not isinstance(records, list):
        raise ValueError("JSON test-case data must be an array")
    return [TestCase.from_record(record) for record in records]


def save_json(cases: list[TestCase], file_path: Path) -> None:
    """Write test cases as a readable JSON array."""
    with file_path.open("w", encoding="utf-8") as destination:
        json.dump(
            [asdict(case) for case in cases],
            destination,
            indent=2,
            ensure_ascii=False,
        )
        destination.write("\n")


def main() -> None:
    folder = Path(__file__).parent
    csv_file = folder / "sample_test_cases.csv"
    json_file = folder / "sample_test_cases.json"

    cases_from_csv = load_csv(csv_file)
    save_json(cases_from_csv, json_file)
    cases_from_json = load_json(json_file)

    with TemporaryDirectory() as temporary_folder:
        csv_round_trip_file = Path(temporary_folder) / "round_trip.csv"
        save_csv(cases_from_csv, csv_round_trip_file)
        cases_from_csv_round_trip = load_csv(csv_round_trip_file)

    assert len(cases_from_csv) == 10, "Expected 10 sample test cases"
    assert cases_from_json == cases_from_csv, "CSV-to-JSON round trip changed data"
    assert cases_from_csv_round_trip == cases_from_csv, (
        "CSV write/read round trip changed data"
    )
    assert all(isinstance(case, TestCase) for case in cases_from_json)

    print(f"Loaded {len(cases_from_csv)} test cases from CSV")
    print(f"Exported and reloaded {len(cases_from_json)} test cases from JSON")
    print("Round-trip checks: 4 passed")


if __name__ == "__main__":
    main()
