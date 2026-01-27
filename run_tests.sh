#!/bin/bash

# Booking API Test Automation - Test Runner Script

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Booking API Test Automation${NC}"
echo -e "${BLUE}========================================${NC}"

# Activate virtual environment
source .venv/bin/activate

# Check if argument is provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./run_tests.sh                    # Run all tests"
    echo "  ./run_tests.sh -v                 # Run tests with verbose output"
    echo "  ./run_tests.sh -k test_name       # Run specific test by pattern"
    echo "  ./run_tests.sh --cov              # Run tests with coverage report"
    echo "  ./run_tests.sh --cov-html         # Generate HTML coverage report"
    echo ""
    echo -e "${YELLOW}Running all tests by default...${NC}"
    pytest tests/test_booking_api.py -v
else
    case "$1" in
        -v)
            echo -e "${GREEN}Running tests with verbose output...${NC}"
            pytest tests/test_booking_api.py -v
            ;;
        -k)
            echo -e "${GREEN}Running tests matching: $2${NC}"
            pytest tests/test_booking_api.py -k "$2" -v
            ;;
        --cov)
            echo -e "${GREEN}Running tests with coverage report...${NC}"
            pytest tests/test_booking_api.py --cov=. --cov-report=term
            ;;
        --cov-html)
            echo -e "${GREEN}Generating HTML coverage report...${NC}"
            pytest tests/test_booking_api.py --cov=. --cov-report=html --cov-report=term
            echo -e "${GREEN}Coverage report generated in: htmlcov/index.html${NC}"
            ;;
        *)
            echo -e "${YELLOW}Unknown option: $1${NC}"
            pytest tests/test_booking_api.py "$@"
            ;;
    esac
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Test run completed!${NC}"
echo -e "${BLUE}========================================${NC}"
