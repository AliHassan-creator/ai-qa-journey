"""Run API status checks from test_cases.json and write a CSV report."""

import csv
import json
from pathlib import Path


from pydantic import BaseModel, Field, ValidationError


class TestCase(BaseModel):
    name: str = Field(min_length=1)
    expected_status: int = Field(ge=100, le=599)
    actual_status: int = Field(ge=100, le=599)


valid_case = {
    "name": "Valid login",
    "expected_status": 200,
    "actual_status": 200,
}

invalid_case = {
    "name": "Invalid login",
    "expected_status": 200,
    "actual_status": "not-a-number",
}

for data in [valid_case, invalid_case]:
    try:
        test = TestCase(**data)
        print(f"VALID: {test.name}")
    except ValidationError as error:
        print("INVALID TEST DATA:")
        print(error)


class TestCase:
    """One API test with expected and actual HTTP status codes."""

    def __init__(self, name: str, expected_status: int, actual_status: int) -> None:
        self.name = name
        self.expected_status = expected_status
        self.actual_status = actual_status

    def run(self) -> str:
        """Return PASS when the observed status matches the expected status."""
        if self.expected_status == self.actual_status:
            return "PASS"
        return "FAIL"


class TestRunner:
    """Load test cases, run them, and save their results as CSV."""

    def __init__(self, input_file: Path, output_file: Path) -> None:
        self.input_file = input_file
        self.output_file = output_file

    def load_test_cases(self) -> list[TestCase]:
        with self.input_file.open("r", encoding="utf-8") as source:
            data = json.load(source)

        return [
            TestCase(
                name=item["name"],
                expected_status=int(item["expected_status"]),
                actual_status=int(item["actual_status"]),
            )
            for item in data
        ]

    def run(self) -> None:
        test_cases = self.load_test_cases()
        results = []

        for test_case in test_cases:
            result = test_case.run()
            results.append(
                {
                    "name": test_case.name,
                    "expected_status": test_case.expected_status,
                    "actual_status": test_case.actual_status,
                    "result": result,
                }
            )
            print(f"{test_case.name}: {result}")

        with self.output_file.open("w", newline="", encoding="utf-8") as report:
            fieldnames = [
                "name",
                "expected_status",
                "actual_status",
                "result",
            ]
            writer = csv.DictWriter(report, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        passed = sum(result["result"] == "PASS" for result in results)
        failed = len(results) - passed

        print("\n--- Test Summary ---")
        print(f"Total: {len(results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Report saved to: {self.output_file}")


def main() -> None:
    folder = Path(__file__).parent
    runner = TestRunner(
        input_file=folder / "test_cases.json",
        output_file=folder / "test_results.csv",
    )
    runner.run()


if __name__ == "__main__":
    main()
