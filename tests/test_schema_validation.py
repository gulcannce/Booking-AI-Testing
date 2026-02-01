import json
import os
import pytest
from jsonschema import validate, ValidationError
from config.config import Config
from utils.api_client import APIClient
from data.test_data import get_valid_booking_payload


@pytest.fixture(autouse=True)
def api_client():
    return APIClient(Config.BASE_URL)


def load_schema():
    here = os.path.dirname(__file__)
    schema_path = os.path.join(here, "..", "schemas", "booking_schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_post_response_matches_booking_schema(api_client):
    """Create a booking and validate the returned `booking` object against JSON Schema."""
    payload = get_valid_booking_payload()
    resp = api_client.post(Config.BOOKING_ENDPOINT, payload)
    assert resp.status_code == 200
    resp_json = resp.json()
    # POST returns { bookingid: int, booking: { ... } }
    assert "booking" in resp_json
    booking_obj = resp_json["booking"]

    schema = load_schema()
    try:
        validate(instance=booking_obj, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Booking object did not match schema: {e.message}")


def test_get_by_id_matches_booking_schema(api_client):
    """Create a booking, GET it by id and validate the returned object against JSON Schema."""
    payload = get_valid_booking_payload()
    post_resp = api_client.post(Config.BOOKING_ENDPOINT, payload)
    assert post_resp.status_code == 200
    booking_id = post_resp.json().get("bookingid")
    assert booking_id is not None

    get_resp = api_client.get(f"{Config.BOOKING_ENDPOINT}/{booking_id}")
    assert get_resp.status_code == 200
    booking_obj = get_resp.json()

    schema = load_schema()
    try:
        validate(instance=booking_obj, schema=schema)
    except ValidationError as e:
        pytest.fail(f"GET booking object did not match schema: {e.message}")
