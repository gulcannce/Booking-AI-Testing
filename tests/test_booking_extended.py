import os
import json
import pytest
import logging
from jsonschema import validate, ValidationError
from config.config import Config
from utils.api_client import APIClient, AssertionHelper
from data.test_data import get_valid_booking_payload, get_booking_payload_with_params

logger = logging.getLogger(__name__)


class TestBookingExtended:
    """Extended tests: GET, invalid ID, and auth-protected update/delete (skipped if no creds)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.api_client = APIClient(Config.BASE_URL)
        self.assertion_helper = AssertionHelper()

    def test_get_all_bookings(self):
        """GET /booking returns a list of bookings (ids)."""
        response = self.api_client.get(Config.BOOKING_ENDPOINT)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list), "Expected list of bookings"
        logger.info(f"Found {len(data)} booking entries")

    def test_get_booking_by_id(self):
        """Create a booking then retrieve it by id and compare fields."""
        payload = get_valid_booking_payload()
        post_resp = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        self.assertion_helper.assert_status_code(post_resp)
        booking_id = post_resp.json().get("bookingid")
        assert booking_id, "bookingid not returned"

        get_resp = self.api_client.get(f"{Config.BOOKING_ENDPOINT}/{booking_id}")
        assert get_resp.status_code == 200
        booking = get_resp.json()
        # API returns booking object directly for GET by id
        assert booking.get("firstname") == payload["firstname"]
        assert booking.get("lastname") == payload["lastname"]

    def test_get_invalid_booking_id(self):
        """Requesting a non-existent booking id should return 404."""
        invalid_id = 99999999
        resp = self.api_client.get(f"{Config.BOOKING_ENDPOINT}/{invalid_id}")
        assert resp.status_code == 404, f"Expected 404 for invalid id, got {resp.status_code}"

    def _load_booking_schema(self):
        here = os.path.dirname(__file__)
        schema_path = os.path.join(here, "..", "schemas", "booking_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_client_side_rejects_missing_fields(self):
        """Deterministic test: validate invalid payload against local JSON Schema (no network call)."""
        payload = get_valid_booking_payload()
        payload.pop("firstname", None)
        schema = self._load_booking_schema()
        with pytest.raises(ValidationError):
            validate(instance=payload, schema=schema)

    @pytest.mark.xfail(reason="API may return 500 for invalid payload; not deterministic", strict=False)
    def test_api_handles_missing_fields(self):
        """API-level negative test: POST invalid payload and expect 4xx (xfail if server returns 5xx)."""
        payload = get_valid_booking_payload()
        payload.pop("firstname", None)
        resp = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        assert resp.status_code in (400, 422)

    def _get_auth_token(self):
        """Helper: obtain auth token using ADMIN_USERNAME/ADMIN_PASSWORD env vars. Skips test if not set."""
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")
        if not username or not password:
            pytest.skip("Admin credentials not provided via env vars; skipping auth tests")
        resp = self.api_client.post("/auth", {"username": username, "password": password})
        assert resp.status_code == 200, "Failed to obtain auth token"
        return resp.json().get("token")

    def test_update_and_delete_booking_with_auth(self):
        """Create booking, update it with auth token, then delete it. Requires ADMIN_USERNAME/ADMIN_PASSWORD env vars."""
        token = self._get_auth_token()

        payload = get_valid_booking_payload()
        post_resp = self.api_client.post(Config.BOOKING_ENDPOINT, payload)
        self.assertion_helper.assert_status_code(post_resp)
        booking_id = post_resp.json().get("bookingid")

        # Update booking
        updated_payload = get_booking_payload_with_params(firstname="UpdatedName")
        headers = {"Cookie": f"token={token}", "Content-Type": "application/json"}
        put_resp = self.api_client.put(f"{Config.BOOKING_ENDPOINT}/{booking_id}", updated_payload, headers=headers)
        assert put_resp.status_code in (200, 201, 204), f"Unexpected status for PUT: {put_resp.status_code}"

        # Verify update
        get_resp = self.api_client.get(f"{Config.BOOKING_ENDPOINT}/{booking_id}")
        assert get_resp.status_code == 200
        assert get_resp.json().get("firstname") == "UpdatedName"

        # Delete booking
        del_headers = {"Cookie": f"token={token}"}
        del_resp = self.api_client.delete(f"{Config.BOOKING_ENDPOINT}/{booking_id}", headers=del_headers)
        assert del_resp.status_code in (200, 201, 204)

        # Verify deletion
        after_del = self.api_client.get(f"{Config.BOOKING_ENDPOINT}/{booking_id}")
        assert after_del.status_code == 404
