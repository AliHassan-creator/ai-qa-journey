
import csv
import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "qa_test_data.json"
REPORT_FILE = BASE_DIR / "qa_test_report.csv"


class TestCase(BaseModel):
    name: str = Field(min_length=1)
    expected_status: int = Field(ge=100, le=599)
    actual_status: int = Field(ge=100, le=599)


def run_test(test: TestCase) -> str:
    return (
        "PASS"
        if test.expected_status == test.actual_status
        else "FAIL"
    )


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        test_data = json.load(file)

    results = []
    passed = 0
    failed = 0
    invalid = 0

    for record in test_data:
        try:
            test = TestCase(**record)
            result = run_test(test)
            expected = test.expected_status
            actual = test.actual_status
            name = test.name

        except ValidationError:
            name = str(record.get("name", "Unnamed test"))
            expected = record.get("expected_status", "")
            actual = record.get("actual_status", "")
            result = "INVALID DATA"
            invalid += 1

        if result == "PASS":
            passed += 1
        elif result == "FAIL":
            failed += 1

        results.append({
            "name": name,
            "expected_status": expected,
            "actual_status": actual,
            "result": result,
        })

        print(f"{name}: {result}")

    with REPORT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        columns = [
            "name",
            "expected_status",
            "actual_status",
            "result",
        ]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    print("\n--- QA Summary ---")
    print(f"Total records: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Invalid data: {invalid}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
