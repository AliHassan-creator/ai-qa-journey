
test_name = "Valid login test"
expected_status = 200
actual_status = 200
response_time = 1.25

test_passed = actual_status == expected_status

print("Test:", test_name)
print("Expected status:", expected_status)
print("Actual status:", actual_status)
print("Response time:", response_time, "seconds")
print("Result:", test_passed)
expected_status = 200
actual_status = 401

if actual_status == expected_status:
    print("PASS: API returned the expected status")
else:
    print("FAIL: API returned an unexpected status")