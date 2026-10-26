
def validate_api_test(test):
    try:
        actual = test["actual_status"]
        expected = test["expected_status"]

        assert actual == expected, (
            f"Expected {expected}, got {actual}"
        )

        return "PASS"

    except KeyError as error:
        return f"FAIL: Missing field {error}"

    except AssertionError as error:
        return f"FAIL: {error}"


test_cases = [
    {
        "name": "Valid login",
        "expected_status": 200,
        "actual_status": 200
    },
    {
        "name": "Invalid password",
        "expected_status": 401,
        "actual_status": 401
    },
    {
        "name": "Unauthorized request",
        "expected_status": 401,
        "actual_status": 403
    },
    {
        "name": "Missing status",
        "expected_status": 200
    }
]

passed = 0
failed = 0

for test in test_cases:
    result = validate_api_test(test)
    print(f"{test['name']}: {result}")

    if result == "PASS":
        passed += 1
    else:
        failed += 1

print("\n--- Test Summary ---")
print(f"Total: {len(test_cases)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
