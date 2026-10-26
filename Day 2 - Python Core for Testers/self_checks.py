"""Small self-checks and a 20-record pass/fail summary for Day 2."""

from bva import boundary_values
from ep import partition


def main() -> None:
    # Five independent checks covering boundary points and each age class.
    assert boundary_values(1, 10) == [0, 1, 2, 9, 10, 11]
    assert partition(12) == "child"
    assert partition(15) == "teenager"
    assert partition(30) == "adult"
    assert partition(65) == "senior"
    assert partition(-1) == "invalid"
    assert partition(121) == "invalid"
    assert partition("18") == "invalid"
    print("Self-checks: 8 passed")

    mock_results = [
        {"name": f"Mock check {number:02}", "passed": number % 5 != 0}
        for number in range(1, 21)
    ]
    for result in mock_results:
        print(f"{result['name']}: {'PASS' if result['passed'] else 'FAIL'}")

    passed = sum(result["passed"] for result in mock_results)
    failed = len(mock_results) - passed
    print(f"\nSummary: {len(mock_results)} total, {passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
