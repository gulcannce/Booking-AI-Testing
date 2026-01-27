"""
Test data module - Contains reusable booking payload and test data
"""
from datetime import datetime, timedelta


def get_valid_booking_payload():
    """
    Returns a valid booking payload for POST request
    
    Returns:
        dict: Booking request payload
    """
    # Calculate check-in and check-out dates
    checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    checkout_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin_date,
            "checkout": checkout_date
        },
        "additionalneeds": "Breakfast included"
    }
    
    return payload


def get_booking_payload_with_params(firstname="Jane", lastname="Smith", 
                                    totalprice=2000, depositpaid=False,
                                    days_from_now=2, nights=5):
    """
    Returns a customized booking payload for parameterized testing
    
    Args:
        firstname (str): First name of the guest
        lastname (str): Last name of the guest
        totalprice (int): Total price for booking
        depositpaid (bool): Whether deposit is paid
        days_from_now (int): Check-in date offset from today
        nights (int): Number of nights to stay
        
    Returns:
        dict: Customized booking payload
    """
    checkin_date = (datetime.now() + timedelta(days=days_from_now)).strftime("%Y-%m-%d")
    checkout_date = (datetime.now() + timedelta(days=days_from_now + nights)).strftime("%Y-%m-%d")
    
    payload = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin_date,
            "checkout": checkout_date
        }
    }
    
    return payload


# Test data sets for parameterized testing
TEST_DATA_SETS = [
    {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 1500,
        "depositpaid": True,
    },
    {
        "firstname": "Alice",
        "lastname": "Smith",
        "totalprice": 2500,
        "depositpaid": False,
    },
    {
        "firstname": "Bob",
        "lastname": "Johnson",
        "totalprice": 3000,
        "depositpaid": True,
    },
]
