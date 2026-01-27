# 🚀 Booking API Test Automation - Quick Reference

## 📌 Project at a Glance

| Component | Location | Purpose |
|-----------|----------|---------|
| **Config** | `config/config.py` | API URLs, timeouts, constants |
| **Test Data** | `data/test_data.py` | Reusable payloads & datasets |
| **API Client** | `utils/api_client.py` | HTTP requests + assertions |
| **Tests** | `tests/test_booking_api.py` | 11 test cases |
| **Test Runner** | `run_tests.sh` | Easy test execution |

---

## ⚡ One-Liner Commands

```bash
# Activate venv & run tests
source .venv/bin/activate && pytest -v

# Or use the script
./run_tests.sh

# Generate coverage report
./run_tests.sh --cov-html

# Run specific test
pytest tests/test_booking_api.py::TestBookingAPI::test_create_booking_with_valid_payload -v

# Run tests matching pattern
pytest -k "test_booking" -v

# Show test output (print statements)
pytest -v -s
```

---

## 🔧 Key Classes & Methods

### APIClient
```python
from utils.api_client import APIClient
from config.config import Config

client = APIClient(Config.BASE_URL)

# Make POST request
response = client.post(Config.BOOKING_ENDPOINT, payload)

# Make GET request
response = client.get("/booking/1")
```

### AssertionHelper
```python
from utils.api_client import AssertionHelper

helper = AssertionHelper()

# Check status code
helper.assert_status_code(response)

# Check required keys
helper.assert_response_contains_keys(response, ["bookingid", "booking"])

# Check full structure
helper.assert_booking_response_structure(response)

# Check field value
helper.assert_field_value(response, "booking.firstname", "John")
```

### Test Data Functions
```python
from data.test_data import (
    get_valid_booking_payload,
    get_booking_payload_with_params,
    TEST_DATA_SETS
)

# Get standard payload
payload = get_valid_booking_payload()

# Get custom payload
payload = get_booking_payload_with_params(
    firstname="Jane",
    lastname="Doe",
    totalprice=2000
)

# Use predefined datasets
for data in TEST_DATA_SETS:
    print(data)
```

---

## 📊 Test Statistics

| Metric | Value |
|--------|-------|
| Total Tests | 11 |
| Pass Rate | 100% ✅ |
| Execution Time | ~7.5s |
| Code Coverage | 92% |
| Test Suites | 2 |
| Edge Cases | 3 |

---

## 📁 File Locations Quick Map

```
booking/
├── config/config.py              ← Change API URL here
├── data/test_data.py             ← Add test payloads here
├── utils/api_client.py           ← Add new assertion methods here
├── tests/test_booking_api.py     ← Add test cases here
├── CLAUDE_PROMPTS.md             ← Claude AI prompt templates
├── QUICKSTART.md                 ← Getting started guide
└── README.md                     ← Full documentation
```

---

## 🎯 Adding New Tests - Quick Checklist

- [ ] Create payload function in `data/test_data.py` (if needed)
- [ ] Write test function in `tests/test_booking_api.py`
- [ ] Use `self.api_client.post()` or `.get()`
- [ ] Use `self.assertion_helper.*()` for validations
- [ ] Add logging with `logger.info()`
- [ ] Run: `pytest tests/test_booking_api.py::TestYourClass::test_your_test -v`

---

## 🐛 Debugging Tips

| Issue | Solution |
|-------|----------|
| `pytest: command not found` | Run `source .venv/bin/activate` |
| Tests fail with connection error | Check internet & API endpoint |
| Import errors | Ensure all `__init__.py` files exist |
| Logging not showing | Use `pytest -v -s` |
| Want to see request/response | Check test logs automatically printed |

---

## 🎓 Common Pytest Flags

```bash
-v              # Verbose output
-vv             # Extra verbose
-s              # Show print statements
-x              # Stop on first failure
-k pattern      # Run tests matching pattern
--collect-only  # Show tests without running
--tb=short      # Short traceback format
--lf            # Run last failed tests
--ff            # Run failed tests first
```

---

## 📝 Payload Structure

```json
{
  "firstname": "John",
  "lastname": "Doe",
  "totalprice": 1500,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-01-28",
    "checkout": "2026-02-03"
  },
  "additionalneeds": "Breakfast"
}
```

---

## ✨ Environment Variables (Optional)

Create `.env` file to override settings:
```env
BASE_URL=https://your-api.com
BOOKING_ENDPOINT=/api/bookings
REQUEST_TIMEOUT=15
LOG_LEVEL=DEBUG
```

Then load in `config.py`:
```python
from dotenv import load_dotenv
import os
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
```

---

## 🚀 CI/CD Integration (GitHub Actions Example)

```yaml
name: Run API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## 💡 Pro Tips

✅ Use `@pytest.mark.parametrize` for data-driven tests
✅ Use fixtures for setup/teardown
✅ Keep assertions in helper methods
✅ Log every important step
✅ Use meaningful test names
✅ Group related tests in classes
✅ Document complex test scenarios
✅ Review coverage reports regularly

---

**Last Updated:** January 27, 2026
**Project Version:** 1.0.0
**Status:** Production Ready ✅
