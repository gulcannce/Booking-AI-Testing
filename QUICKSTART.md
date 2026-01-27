# Quick Start Guide for Booking API Test Automation

## 🚀 Installation & Setup

### 1️⃣ Clone or Navigate to Project
```bash
cd /Users/gulcan/Desktop/booking
```

### 2️⃣ Activate Virtual Environment (One-time Setup)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Optional: Add to ~/.zshrc for Auto-Activation
Add this to your `~/.zshrc` file:

```zsh
# Booking API Test Automation
alias booking='cd /Users/gulcan/Desktop/booking && source .venv/bin/activate'
```

Then reload your shell:
```bash
source ~/.zshrc
```

Now you can simply type `booking` to jump into the project with venv activated!

---

## ✅ Running Tests

### Once Virtual Environment is Activated:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_booking_api.py::TestBookingAPI::test_create_booking_with_valid_payload -v

# Run tests matching pattern
pytest -k "test_deposit" -v

# Generate coverage report
pytest --cov=. --cov-report=html

# Show test collection without running
pytest --collect-only
```

### Or Use the Test Runner Script:
```bash
./run_tests.sh                # Run all tests
./run_tests.sh -v             # Verbose mode
./run_tests.sh -k test_name   # Match test pattern
./run_tests.sh --cov          # Coverage report
./run_tests.sh --cov-html     # HTML coverage report
```

---

## 📊 Coverage Report

After running tests with coverage, open the HTML report:
```bash
open htmlcov/index.html
```

Current Coverage: **92%** ✅

---

## 📁 Project Structure
```
booking/
├── config/config.py           ← API configuration
├── data/test_data.py          ← Test payloads
├── utils/api_client.py        ← API client & assertions
├── tests/test_booking_api.py  ← 11 test cases
├── run_tests.sh              ← Test runner script
├── requirements.txt          ← Dependencies
├── pytest.ini                ← Pytest config
└── README.md                 ← Full documentation
```

---

## 🎯 Test Cases Overview

### Main Suite (6 tests)
- ✅ Valid booking creation
- ✅ Booking ID validation
- ✅ Details match request
- ✅ Dates validation
- ✅ Deposit paid field
- ✅ Parameterized testing (3 data sets)

### Edge Cases (3 tests)
- ✅ Special characters
- ✅ Zero price
- ✅ High price

---

## 🔗 Adding New Tests

1. Add test data to `data/test_data.py`
2. Write test function in `tests/test_booking_api.py`
3. Run tests: `pytest -v`

Example:
```python
def test_new_scenario(self):
    """Test description"""
    payload = get_valid_booking_payload()
    response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
    self.assertion_helper.assert_status_code(response)
    # Add your assertions
```

---

## 💡 Tips & Tricks

- Use `source .venv/bin/activate` before running pytest
- Use `pytest -s` to see print statements
- Use `pytest -x` to stop on first failure
- Use `pytest -vv` for extra verbose output
- Check `pytest.ini` for all available options

---

**Ready to test! 🚀**
