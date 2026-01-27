"""
Configuration module for API test automation
Contains environment-specific settings and constants
"""

class Config:
    """Base configuration class"""
    
    # API Configuration
    BASE_URL = "https://restful-booker.herokuapp.com"
    BOOKING_ENDPOINT = "/booking"
    FULL_URL = f"{BASE_URL}{BOOKING_ENDPOINT}"
    
    # Request Configuration
    REQUEST_TIMEOUT = 10  # seconds
    CONTENT_TYPE = "application/json"
    
    # Response Validation
    EXPECTED_STATUS_CODES = [200, 201]
    
    # Logging
    LOG_LEVEL = "INFO"
