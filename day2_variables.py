
test_name = "Login API - valid credentials"
expected_status = 200
actual_status = 200
response_time = 1.45
test_passed = actual_status == expected_status

print("Test:", test_name)
print("Expected:", expected_status)
print("Actual:", actual_status)
print("Response time:", response_time)
print("Passed:", test_passed)


status_codes = [200, 201, 400, 401, 500]

print(status_codes[0])  # First item: 200
print(status_codes[3])  # Fourth item: 401

status_codes.append(403)  # Add another test value
print(status_codes)


login_test = {
    "username": "qa_user",
    "expected_status": 200,
    "actual_status": 200,
    "response_time": 1.2
}

print(login_test["username"])
print(login_test["expected_status"])

if login_test["actual_status"] == login_test["expected_status"]:
    print("PASS")
else:
    print("FAIL")

test_cases = [
    {"name": "Valid login", "expected": 200, "actual": 200},
    {"name": "Invalid password", "expected": 401, "actual": 401},
    {"name": "Missing username", "expected": 400, "actual": 500}
]

for test in test_cases:
    result = "PASS" if test["expected"] == test["actual"] else "FAIL"
    print(test["name"], ":", result)



def check_status(expected, actual):
    return expected == actual


test_cases = [
    {"name": "Valid login", "expected": 200, "actual": 200},
    {"name": "Invalid password", "expected": 401, "actual": 401},
    {"name": "Unauthorized request", "expected": 401, "actual": 403},
]

for test in test_cases:
    passed = check_status(test["expected"], test["actual"])
    result = "PASS" if passed else "FAIL"
    print(f"{test['name']}: {result}")
