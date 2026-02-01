# API Test Automation Prompt Template for Claude AI

## 📋 Template 1: Yeni Test Case Ekleme

```
You are a senior QA automation engineer. I have an existing Python pytest API test automation project.

Project details:
- Framework: pytest
- API Client Library: requests
- Base URL: https://restful-booker.herokuapp.com
- Project Structure:
  - config/config.py (configuration & constants)
  - data/test_data.py (test payloads & data)
  - utils/api_client.py (APIClient & AssertionHelper classes)
  - tests/test_booking_api.py (test cases)

Existing APIClient methods:
- post(endpoint: str, payload: dict) -> requests.Response
- get(endpoint: str) -> requests.Response

Existing AssertionHelper methods:
- assert_status_code(response, expected_codes)
- assert_response_contains_keys(response, required_keys)
- assert_booking_response_structure(response)
- assert_field_value(response, field_path, expected_value)

Now, I need you to:
1. Create a new test case for [DESCRIBE YOUR TEST SCENARIO]
2. Add necessary test data/payload to data/test_data.py if needed
3. Follow the existing code style and patterns
4. Include comprehensive logging
5. Make assertions clear and meaningful

Test scenario: [PROVIDE DETAILED REQUIREMENTS]
Expected assertions: [DESCRIBE WHAT SHOULD BE VALIDATED]

Please provide:
- Complete Python code for the test case
- Any helper functions needed
- Clear comments explaining each step
```

---

## 📋 Template 2: API Endpoint Testing

```
You are a senior QA automation engineer. I want to create API test automation for a new endpoint.

Endpoint Details:
- Method: [GET/POST/PUT/DELETE/PATCH]
- URL: [API_ENDPOINT]
- Authentication: [if required]

Request Payload (if applicable):
[PROVIDE SAMPLE JSON]

Expected Response (success case):
[PROVIDE SAMPLE JSON]

Test Scenarios to Cover:
1. [Scenario 1]
2. [Scenario 2]
3. [Scenario 3]
4. [Edge case 1]
5. [Edge case 2]

Using the existing project structure, please generate:
1. test_data.py functions for payload creation
2. Complete test cases with assertions
3. Any additional utility functions needed

Follow the existing patterns in the project:
- Use APIClient for HTTP requests
- Use AssertionHelper for validations
- Include comprehensive logging
- Parameterize tests where applicable
```

---

## 📋 Template 3: Adding Helper Utilities

```
You are a senior QA automation engineer working with pytest and requests.

I need to add a utility function to my API testing framework.

Requirements:
- Function name: [FUNCTION_NAME]
- Purpose: [DESCRIBE PURPOSE]
- Input parameters: [LIST PARAMETERS]
- Expected output: [DESCRIBE OUTPUT]
- Edge cases to handle: [LIST EDGE CASES]

Current project uses:
- requests library for HTTP calls
- pytest for testing
- logging for output

Please provide:
- Complete Python function with type hints
- Comprehensive docstring
- Error handling
- Usage examples
- Unit test (if applicable)

Location in project: [WHERE TO ADD THIS - utils/api_client.py, data/test_data.py, etc.]
```

---

## 📋 Template 4: Test Scenario Planning

```
I'm planning test scenarios for an API endpoint. Help me structure comprehensive test coverage.

Endpoint: [API_ENDPOINT]
Method: [HTTP_METHOD]
Expected Status Codes: [200, 201, etc.]

Main Happy Path:
[DESCRIBE NORMAL OPERATION]

Edge Cases to Test:
1. [Edge case 1]
2. [Edge case 2]
3. [Edge case 3]

Error Scenarios:
1. [Error scenario 1]
2. [Error scenario 2]

Data Variations:
[DESCRIBE DIFFERENT INPUT VARIATIONS]

Please provide:
1. A comprehensive test plan with all scenarios
2. Suggested test data sets for parameterization
3. Assertions that should be validated
4. Recommended test case names
5. Implementation hints using my existing framework
```

---

## 📋 Template 5: Bug Report & Test Case

```
I found a bug in the API. Help me create a test case that validates the fix.

Bug Description:
[DESCRIBE THE BUG]

Expected Behavior:
[WHAT SHOULD HAPPEN]

Current Behavior:
[WHAT ACTUALLY HAPPENS]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Using my pytest + requests framework, please generate:
1. A test case that reproduces the bug
2. The assertions that should pass once fixed
3. Any test data needed
4. Comments explaining the bug scenario

This test should fail with the current API and pass once the bug is fixed.
```

---

## 🎯 How to Use These Templates

1. **Copy the relevant template** from above
2. **Fill in your specific details** (marked in [BRACKETS])
3. **Paste into Claude AI chat**
4. **Get back production-ready code** that fits your project structure
5. **Copy-paste directly into your project files**

---

## ⚡ Quick Tips for Best Results

✅ **Be Specific**: The more details you provide, the better code Claude generates
✅ **Include Context**: Mention your existing project structure and patterns
✅ **Show Examples**: Provide sample payloads and expected responses
✅ **Request Format**: Ask for "complete Python code" with "docstrings and comments"
✅ **Follow Patterns**: Tell Claude to follow your existing code style
✅ **Error Handling**: Ask for "comprehensive error handling"
✅ **Logging**: Request "detailed logging at each step"

---

## 🔄 Example: Using Template 1

### Input (Your Question to Claude):
```
You are a senior QA automation engineer. I have an existing Python pytest API test automation project.

Project structure with APIClient and AssertionHelper classes as mentioned above.

Now, I need you to:
1. Create a test case for the GET /booking/{id} endpoint
2. Add test data if needed
3. Follow existing code style

Test scenario: Retrieve a booking by ID that was previously created, validate all fields match

Please provide complete Python code with docstrings.
```

### Output (Claude's Response):
```python
def test_get_booking_by_id(self):
    """
    Test Case: Retrieve booking by ID
    
    Steps:
    1. Create a new booking
    2. Extract booking ID from response
    3. Call GET /booking/{id} endpoint
    4. Validate all fields match the created booking
    """
    # Create booking
    payload = get_valid_booking_payload()
    create_response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
    booking_id = create_response.json()["bookingid"]
    
    # Get booking by ID
    get_endpoint = f"{Config.BOOKING_ENDPOINT}/{booking_id}"
    response = self.api_client.get(get_endpoint)
    
    # Validate
    self.assertion_helper.assert_status_code(response)
    self.assertion_helper.assert_field_value(response, "firstname", payload["firstname"])
```

✅ **Ready to use! Just add to test_booking_api.py**

---

  ## 🧪 Concrete AI-Assisted Example (Short)

  ### Prompt (to Claude)
  ```
  You are a senior QA automation engineer. Given the existing pytest project (APIClient + AssertionHelper), generate a test case that:
  - Creates a booking with firstname "AIUser" and lastname "Assistant"
  - Verifies the POST response contains bookingid and booking fields
  - Retrieves the booking by id and verifies firstname/lastname match
  Return only the complete Python test function body compatible with pytest class-based tests used in this repo.
  ```

  ### Example Claude Output
  ```python
  def test_create_and_verify_booking_ai(self):
    payload = get_booking_payload_with_params(firstname="AIUser", lastname="Assistant")
    create_resp = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
    self.assertion_helper.assert_status_code(create_resp)
    booking_id = create_resp.json().get("bookingid")
    assert booking_id is not None

    get_resp = self.api_client.get(f"{Config.BOOKING_ENDPOINT}/{booking_id}")
    self.assertion_helper.assert_status_code(get_resp)
    self.assertion_helper.assert_field_value(get_resp, "firstname", "AIUser")
    self.assertion_helper.assert_field_value(get_resp, "lastname", "Assistant")
  ```

  Add this snippet to your tests to concretely show how Claude can generate executable test code that follows the repository patterns.

**Pro Tip:** Keep these templates handy and reuse them for all your test automation prompts! 🚀
