"""
API Test Cases - Test automation for booking API endpoint
"""
import pytest
import logging
from config.config import Config
from data.test_data import get_valid_booking_payload, get_booking_payload_with_params, TEST_DATA_SETS
from utils.api_client import APIClient, AssertionHelper

# Configure logging for tests
logger = logging.getLogger(__name__)


class TestBookingAPI:
    """Test suite for booking API"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.api_client = APIClient(Config.BASE_URL)
        self.assertion_helper = AssertionHelper()
        logger.info("\n" + "="*80)
        logger.info("TEST SETUP COMPLETED")
        logger.info("="*80)
    
    def test_create_booking_with_valid_payload(self):
        """
        Test Case 1: Create a booking with valid payload
        
        Steps:
        1. Prepare valid booking payload
        2. Send POST request to /booking endpoint
        3. Validate status code (200 or 201)
        4. Validate response structure
        5. Validate all required fields are present
        """
        logger.info("\n>>> Test: Create booking with valid payload")
        
        # Step 1: Prepare payload
        payload = get_valid_booking_payload()
        logger.info(f"Payload prepared: firstname={payload['firstname']}, lastname={payload['lastname']}")
        
        # Step 2: Send POST request
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        
        # Step 3: Validate status code
        self.assertion_helper.assert_status_code(response)
        
        # Step 4 & 5: Validate response structure
        self.assertion_helper.assert_booking_response_structure(response)
        
        logger.info("✓ Test passed: Booking created successfully")
    
    def test_response_contains_booking_id(self):
        """
        Test Case 2: Verify response contains bookingid
        
        Steps:
        1. Create a booking
        2. Verify bookingid is present in response
        3. Verify bookingid is not empty
        """
        logger.info("\n>>> Test: Response contains bookingid")
        
        # Step 1: Create booking
        payload = get_valid_booking_payload()
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        
        # Step 2 & 3: Verify bookingid
        response_json = response.json()
        assert "bookingid" in response_json, "bookingid not found in response"
        assert isinstance(response_json["bookingid"], int), "bookingid should be an integer"
        assert response_json["bookingid"] > 0, "bookingid should be a positive integer"
        
        logger.info(f"✓ Booking ID received: {response_json['bookingid']}")
    
    def test_booking_details_match_request(self):
        """
        Test Case 3: Verify booking details in response match the request
        
        Steps:
        1. Create booking with specific firstname and lastname
        2. Verify response contains the same firstname
        3. Verify response contains the same lastname
        4. Verify response contains the same totalprice
        """
        logger.info("\n>>> Test: Booking details match request")
        
        # Step 1: Create booking with known values
        expected_firstname = "TestUser"
        expected_lastname = "AutoTest"
        expected_price = 1999
        
        payload = get_booking_payload_with_params(
            firstname=expected_firstname,
            lastname=expected_lastname,
            totalprice=expected_price
        )
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        
        # Step 2-4: Verify details match
        self.assertion_helper.assert_field_value(response, "booking.firstname", expected_firstname)
        self.assertion_helper.assert_field_value(response, "booking.lastname", expected_lastname)
        self.assertion_helper.assert_field_value(response, "booking.totalprice", expected_price)
        
        logger.info("✓ Test passed: All booking details match request")
    
    def test_booking_dates_validation(self):
        """
        Test Case 4: Verify booking dates are properly set
        
        Steps:
        1. Create booking with specific check-in and check-out dates
        2. Verify checkin date is present and correct
        3. Verify checkout date is present and correct
        """
        logger.info("\n>>> Test: Booking dates validation")
        
        # Step 1: Create booking
        payload = get_valid_booking_payload()
        expected_checkin = payload["bookingdates"]["checkin"]
        expected_checkout = payload["bookingdates"]["checkout"]
        
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        
        # Step 2 & 3: Verify dates
        response_json = response.json()
        booking_dates = response_json["booking"]["bookingdates"]
        
        assert booking_dates["checkin"] == expected_checkin, \
            f"Check-in date mismatch. Expected: {expected_checkin}, Got: {booking_dates['checkin']}"
        assert booking_dates["checkout"] == expected_checkout, \
            f"Check-out date mismatch. Expected: {expected_checkout}, Got: {booking_dates['checkout']}"
        
        logger.info(f"✓ Check-in date: {booking_dates['checkin']}")
        logger.info(f"✓ Check-out date: {booking_dates['checkout']}")
    
    def test_deposit_paid_field(self):
        """
        Test Case 5: Verify depositpaid field is correctly reflected
        
        Steps:
        1. Create booking with depositpaid=True
        2. Verify response shows depositpaid=True
        3. Create another booking with depositpaid=False
        4. Verify response shows depositpaid=False
        """
        logger.info("\n>>> Test: Deposit paid field validation")
        
        # Step 1-2: Test with deposit paid = True
        payload_with_deposit = get_booking_payload_with_params(depositpaid=True)
        response_with_deposit = self.api_client.post(Config.BOOKING_ENDPOINT, payload_with_deposit)
        self.assertion_helper.assert_field_value(response_with_deposit, "booking.depositpaid", True)
        
        # Step 3-4: Test with deposit paid = False
        payload_without_deposit = get_booking_payload_with_params(depositpaid=False)
        response_without_deposit = self.api_client.post(Config.BOOKING_ENDPOINT, payload_without_deposit)
        self.assertion_helper.assert_field_value(response_without_deposit, "booking.depositpaid", False)
        
        logger.info("✓ Test passed: Deposit paid field validated correctly")
    
    @pytest.mark.parametrize("test_data", TEST_DATA_SETS)
    def test_create_multiple_bookings(self, test_data):
        """
        Test Case 6: Parameterized test - Create multiple bookings with different data
        
        Args:
            test_data (dict): Test data containing firstname, lastname, totalprice, depositpaid
        """
        logger.info(f"\n>>> Test: Create booking with data: {test_data}")
        
        # Create payload with test data
        payload = get_booking_payload_with_params(
            firstname=test_data["firstname"],
            lastname=test_data["lastname"],
            totalprice=test_data["totalprice"],
            depositpaid=test_data["depositpaid"]
        )
        
        # Send request
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        
        # Validate
        self.assertion_helper.assert_status_code(response)
        self.assertion_helper.assert_field_value(response, "booking.firstname", test_data["firstname"])
        self.assertion_helper.assert_field_value(response, "booking.lastname", test_data["lastname"])
        
        logger.info(f"✓ Booking created for {test_data['firstname']} {test_data['lastname']}")


class TestBookingAPIEdgeCases:
    """Test suite for edge cases and error handling"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.api_client = APIClient(Config.BASE_URL)
        self.assertion_helper = AssertionHelper()
    
    def test_booking_with_special_characters(self):
        """
        Test Case 7: Create booking with special characters in name
        """
        logger.info("\n>>> Test: Booking with special characters in name")
        
        payload = get_booking_payload_with_params(
            firstname="José",
            lastname="García-Smith"
        )
        
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        self.assertion_helper.assert_status_code(response)
        self.assertion_helper.assert_field_value(response, "booking.firstname", "José")
        
        logger.info("✓ Test passed: Special characters handled correctly")
    
    def test_booking_with_zero_price(self):
        """
        Test Case 8: Create booking with zero price
        """
        logger.info("\n>>> Test: Booking with zero price")
        
        payload = get_booking_payload_with_params(totalprice=0)
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        
        self.assertion_helper.assert_status_code(response)
        self.assertion_helper.assert_field_value(response, "booking.totalprice", 0)
        
        logger.info("✓ Test passed: Zero price booking created successfully")
    
    def test_booking_with_high_price(self):
        """
        Test Case 9: Create booking with high price value
        """
        logger.info("\n>>> Test: Booking with high price")
        
        high_price = 999999
        payload = get_booking_payload_with_params(totalprice=high_price)
        response = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        
        self.assertion_helper.assert_status_code(response)
        self.assertion_helper.assert_field_value(response, "booking.totalprice", high_price)
        
        logger.info(f"✓ Test passed: High price ({high_price}) booking created successfully")
