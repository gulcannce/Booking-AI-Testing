"""
API Client module - Contains reusable API client and assertion utilities
"""
import requests
import json
import logging
from config.config import Config
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIClient:
    """Reusable API Client for making HTTP requests"""
    
    def __init__(self, base_url: str = Config.BASE_URL):
        """
        Initialize API Client
        
        Args:
            base_url (str): Base URL for API calls
        """
        self.base_url = base_url
        self.timeout = Config.REQUEST_TIMEOUT
        self.headers = {
            "Content-Type": Config.CONTENT_TYPE,
            "Accept": Config.CONTENT_TYPE
        }
        logger.info(f"APIClient initialized with base URL: {self.base_url}")
    
    def post(self, endpoint: str, payload: Dict[str, Any]) -> requests.Response:
        """
        Make a POST request to the API
        
        Args:
            endpoint (str): API endpoint
            payload (dict): Request payload
            
        Returns:
            requests.Response: API response object
        """
        url = f"{self.base_url}{endpoint}"
        
        logger.info(f"Making POST request to: {url}")
        logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            logger.info(f"Response status code: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    def get(self, endpoint: str) -> requests.Response:
        """
        Make a GET request to the API
        
        Args:
            endpoint (str): API endpoint
            
        Returns:
            requests.Response: API response object
        """
        url = f"{self.base_url}{endpoint}"
        
        logger.info(f"Making GET request to: {url}")
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            logger.info(f"Response status code: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise


class AssertionHelper:
    """Helper class for API response assertions"""
    
    @staticmethod
    def assert_status_code(response: requests.Response, expected_codes: List[int] = None):
        """
        Assert response status code
        
        Args:
            response (requests.Response): API response
            expected_codes (list): List of acceptable status codes
        """
        if expected_codes is None:
            expected_codes = Config.EXPECTED_STATUS_CODES
        
        assert response.status_code in expected_codes, \
            f"Expected status code {expected_codes}, but got {response.status_code}"
        
        logger.info(f"✓ Status code assertion passed: {response.status_code}")
    
    @staticmethod
    def assert_response_contains_keys(response: requests.Response, required_keys: List[str]):
        """
        Assert that response JSON contains required keys
        
        Args:
            response (requests.Response): API response
            required_keys (list): List of required keys in response
        """
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise AssertionError(f"Response is not valid JSON: {response.text}")
        
        for key in required_keys:
            assert key in response_json, \
                f"Expected key '{key}' not found in response. Available keys: {response_json.keys()}"
            
            logger.info(f"✓ Key '{key}' found in response with value: {response_json[key]}")
    
    @staticmethod
    def assert_booking_response_structure(response: requests.Response):
        """
        Assert that response contains expected booking structure
        
        Args:
            response (requests.Response): API response
        """
        required_top_level_keys = ["bookingid", "booking"]
        required_booking_keys = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
        required_dates_keys = ["checkin", "checkout"]
        
        # Check top-level keys
        AssertionHelper.assert_response_contains_keys(response, required_top_level_keys)
        
        # Check booking object keys
        response_json = response.json()
        booking = response_json.get("booking", {})
        
        for key in required_booking_keys:
            assert key in booking, \
                f"Expected key '{key}' not found in booking object. Available keys: {booking.keys()}"
            logger.info(f"✓ Booking key '{key}' present with value: {booking[key]}")
        
        # Check bookingdates structure
        booking_dates = booking.get("bookingdates", {})
        for key in required_dates_keys:
            assert key in booking_dates, \
                f"Expected date key '{key}' not found in bookingdates. Available keys: {booking_dates.keys()}"
            logger.info(f"✓ Booking date '{key}' present: {booking_dates[key]}")
    
    @staticmethod
    def assert_field_value(response: requests.Response, field_path: str, expected_value: Any):
        """
        Assert that a specific field in response has expected value
        
        Args:
            response (requests.Response): API response
            field_path (str): Path to field (e.g., "booking.firstname")
            expected_value: Expected value
        """
        response_json = response.json()
        keys = field_path.split(".")
        
        current_value = response_json
        for key in keys:
            assert key in current_value, \
                f"Key '{key}' not found in path '{field_path}'"
            current_value = current_value[key]
        
        assert current_value == expected_value, \
            f"Expected {field_path}={expected_value}, but got {current_value}"
        
        logger.info(f"✓ Field assertion passed: {field_path}={expected_value}")
