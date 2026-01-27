# Booking API Test Automation

A comprehensive Python-based API test automation framework for the Restful Booker API using pytest and requests library.

## 📋 Project Overview

This project demonstrates QA automation best practices for testing the Booking API endpoint:
- **Endpoint**: `POST https://restful-booker.herokuapp.com/booking`
- **Framework**: pytest
- **HTTP Client**: requests
- **Python Version**: 3.8+

## 🏗️ Project Structure

```
booking/
├── config/
│   ├── __init__.py
│   └── config.py              # Configuration settings and constants
├── data/
│   ├── __init__.py
│   └── test_data.py           # Reusable test payloads and data sets
├── utils/
│   ├── __init__.py
│   └── api_client.py          # API client and assertion helpers
├── tests/
│   ├── __init__.py
│   └── test_booking_api.py    # Test cases
├── pytest.ini                  # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /Users/gulcan/Desktop/booking
pip install -r requirements.txt
```

### 2. Run All Tests

```bash
pytest
```

### 3. Run Tests with Detailed Output

```bash
pytest -v
```

### 4. Run Specific Test File

```bash
pytest tests/test_booking_api.py -v
```

### 5. Run Specific Test Case

```bash
pytest tests/test_booking_api.py::TestBookingAPI::test_create_booking_with_valid_payload -v
```

### 6. Run Tests with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

### 7. Run Only Parameterized Tests

```bash
pytest -k "test_create_multiple_bookings" -v
```

## 📊 Test Coverage

The test suite includes **9 comprehensive test cases**:

### Main Test Suite (TestBookingAPI)
1. **test_create_booking_with_valid_payload** - Create booking and validate full response structure
2. **test_response_contains_booking_id** - Verify bookingid is present and valid
3. **test_booking_details_match_request** - Validate firstname, lastname, and price match request
4. **test_booking_dates_validation** - Verify check-in and check-out dates are correct
5. **test_deposit_paid_field** - Verify depositpaid field works correctly
6. **test_create_multiple_bookings** - Parameterized test with multiple data sets

### Edge Cases Suite (TestBookingAPIEdgeCases)
7. **test_booking_with_special_characters** - Test special characters in guest names
8. **test_booking_with_zero_price** - Test zero price bookings
9. **test_booking_with_high_price** - Test high price values

## 📝 Example Request Payload

```json
{
  "firstname": "John",
  "lastname": "Doe",
  "totalprice": 1500,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2024-01-28",
    "checkout": "2024-02-04"
  },
  "additionalneeds": "Breakfast included"
}
```

## ✅ Expected Response Structure

```json
{
  "bookingid": 1,
  "booking": {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 1500,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2024-01-28",
      "checkout": "2024-02-04"
    },
    "additionalneeds": "Breakfast included"
  }
}
```

## 🛠️ Key Components

### Config Module (`config/config.py`)
- Centralized configuration management
- API endpoints and URLs
- Request timeouts and headers
- Response validation rules

### Test Data Module (`data/test_data.py`)
- `get_valid_booking_payload()` - Returns standard booking payload
- `get_booking_payload_with_params()` - Returns customized payload
- `TEST_DATA_SETS` - Pre-defined test data for parameterized tests

### API Client (`utils/api_client.py`)

**APIClient Class**
- `post()` - Make POST requests with logging
- `get()` - Make GET requests with logging

**AssertionHelper Class**
- `assert_status_code()` - Validate response status code
- `assert_response_contains_keys()` - Verify required keys exist
- `assert_booking_response_structure()` - Validate full response structure
- `assert_field_value()` - Assert specific field values

## 📈 Best Practices Implemented

✅ **Clean Code Structure**
- Organized folder layout (config, data, utils, tests)
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)

✅ **Reusable Components**
- Generic API client for any endpoint
- Test data functions for easy payload generation
- Assertion helpers for common validations

✅ **Comprehensive Logging**
- Request/response logging
- Test execution flow visibility
- Debug information for troubleshooting

✅ **Maintainability**
- Clear function names and docstrings
- Parameterized tests for data-driven testing
- Configuration management for easy updates

✅ **Best Practices**
- PEP 8 code style
- Type hints where applicable
- Proper exception handling
- Pytest fixtures for setup/teardown

## 🔧 Customization

### Modify Base URL

Edit `config/config.py`:
```python
BASE_URL = "https://your-api-url.com"
```

### Add New Test Data

Edit `data/test_data.py`:
```python
def get_custom_payload():
    return {
        "firstname": "Custom",
        "lastname": "User",
        "totalprice": 5000,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-03-01",
            "checkout": "2024-03-05"
        }
    }
```

### Add New Test Case

In `tests/test_booking_api.py`:
```python
def test_new_scenario(self):
    """Test description"""
    payload = get_valid_booking_payload()
    response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
    self.assertion_helper.assert_status_code(response)
    # Add your assertions
```

## 📚 CLI Commands Reference

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Run tests with verbose output |
| `pytest -k test_name` | Run specific test by pattern |
| `pytest -x` | Stop on first failure |
| `pytest -s` | Show print statements and logging |
| `pytest --collect-only` | Show tests without running |
| `pytest --markers` | Show available markers |

## 🐛 Troubleshooting

### Tests Fail with Connection Error
- Verify internet connection
- Check if API endpoint is accessible
- Verify firewall settings

### Import Errors
- Ensure you're running tests from project root
- Verify all __init__.py files exist in each package
- Run `pip install -r requirements.txt` again

### Logging Not Showing
- Check pytest.ini log_cli_level setting
- Use `pytest -s` to show logging

## 📞 Support

For questions or issues:
1. Check test logs in console output
2. Review API response in assertion error messages
3. Verify payload structure in test_data.py
4. Check API documentation for endpoint changes

---

**Happy Testing! 🚀**
