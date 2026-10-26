"""API checks for the public Restful Booker learning service."""

import os

import pytest
import requests


BASE_URL = os.getenv(
    "RESTFUL_BOOKER_BASE_URL",
    "https://restful-booker.herokuapp.com",
).rstrip("/")
REQUEST_TIMEOUT_SECONDS = 15
DEMO_USERNAME = os.getenv("RESTFUL_BOOKER_USERNAME", "admin")
DEMO_PASSWORD = os.getenv("RESTFUL_BOOKER_PASSWORD", "password123")


@pytest.fixture
def api_session():
    """Provide a requests.Session with common headers and a bounded timeout per call."""
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


@pytest.fixture
def auth_token(api_session):
    """Authenticate once for a test and return its token."""
    response = api_session.post(
        f"{BASE_URL}/auth",
        json={"username": DEMO_USERNAME, "password": DEMO_PASSWORD},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert response.status_code == 200
    token = response.json().get("token")
    assert isinstance(token, str) and token
    return token


@pytest.fixture
def booking_payload():
    """Return fresh, fictional booking data for each test."""
    return {
        "firstname": "QA Day 6",
        "lastname": "Automation Sample",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {"checkin": "2027-01-10", "checkout": "2027-01-15"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def booking_factory(api_session, auth_token, booking_payload):
    """Create test-owned bookings and remove any that remain after the test."""
    created_ids = []
    auth_headers = {"Cookie": f"token={auth_token}"}

    def create_booking(overrides=None):
        payload = {**booking_payload, **(overrides or {})}
        response = api_session.post(
            f"{BASE_URL}/booking",
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        assert response.status_code == 200
        response_body = response.json()
        booking_id = response_body.get("bookingid")
        assert isinstance(booking_id, int)
        created_ids.append(booking_id)
        return booking_id, response_body

    yield create_booking

    # Clean up only IDs created by this fixture, including after assertion errors.
    for booking_id in created_ids:
        get_response = api_session.get(
            f"{BASE_URL}/booking/{booking_id}",
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        if get_response.status_code == 200:
            delete_response = api_session.delete(
                f"{BASE_URL}/booking/{booking_id}",
                headers=auth_headers,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            assert delete_response.status_code == 201
        else:
            assert get_response.status_code == 404


def test_get_bookings(api_session):
    response = api_session.get(
        f"{BASE_URL}/booking",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 200
    assert "json" in response.headers.get("Content-Type", "").lower()
    bookings = response.json()
    assert isinstance(bookings, list)
    assert all(isinstance(item.get("bookingid"), int) for item in bookings)


def test_get_existing_booking(api_session, booking_factory):
    booking_id, _ = booking_factory()

    response = api_session.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 200
    booking = response.json()
    assert booking["firstname"] == "QA Day 6"
    assert isinstance(booking["lastname"], str)
    assert isinstance(booking["bookingdates"], dict)
    assert isinstance(booking["bookingdates"]["checkin"], str)
    assert isinstance(booking["bookingdates"]["checkout"], str)


def test_get_nonexistent_booking(api_session):
    response = api_session.get(
        f"{BASE_URL}/booking/999999999",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "booking_id",
    [
        pytest.param(999999999, id="high-id"),
        pytest.param(-1, id="negative-id"),
        pytest.param(0, id="zero-id"),
    ],
)
def test_booking_id_boundaries(api_session, booking_id):
    """Exercise representative invalid ID values around the positive ID domain."""
    response = api_session.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 404


def test_booking_id_with_text(api_session):
    response = api_session.get(
        f"{BASE_URL}/booking/abc",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 404


def test_booking_response_is_json(api_session, booking_factory):
    booking_id, _ = booking_factory()
    response = api_session.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 200
    assert "json" in response.headers.get("Content-Type", "").lower()
    body = response.json()
    assert {"firstname", "lastname", "totalprice", "depositpaid", "bookingdates"} <= body.keys()


@pytest.mark.parametrize(
    "totalprice",
    [
        pytest.param(0, id="at-zero-boundary"),
        pytest.param(1, id="just-above-zero"),
        pytest.param(-1, id="just-below-zero"),
    ],
)
def test_totalprice_numeric_boundary_values(booking_factory, totalprice):
    """Check numeric values around zero; the API contract sets no minimum price."""
    _, response_body = booking_factory({"totalprice": totalprice})

    assert isinstance(response_body["booking"].get("totalprice"), (int, float))
    assert response_body["booking"]["totalprice"] == totalprice


def test_invalid_auth_credentials_return_reason(api_session):
    response = api_session.post(
        f"{BASE_URL}/auth",
        json={"username": "invalid-user", "password": "invalid-password"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    # Restful Booker returns HTTP 200 with a reason body for bad login details.
    assert response.status_code == 200
    assert isinstance(response.json().get("reason"), str)
    assert response.json()["reason"]


def test_update_without_authentication_is_forbidden(
    api_session, booking_factory, booking_payload
):
    booking_id, _ = booking_factory()
    response = api_session.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=booking_payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 403


def test_update_with_missing_required_fields_returns_bad_request(
    api_session, auth_token, booking_factory
):
    booking_id, _ = booking_factory()
    response = api_session.put(
        f"{BASE_URL}/booking/{booking_id}",
        json={"firstname": "Incomplete"},
        headers={"Cookie": f"token={auth_token}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 400


def test_booking_crud_lifecycle(api_session, booking_factory, booking_payload, auth_token):
    booking_id, create_body = booking_factory()
    assert create_body["booking"]["firstname"] == booking_payload["firstname"]

    get_response = api_session.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert get_response.status_code == 200
    assert get_response.json()["firstname"] == booking_payload["firstname"]

    updated_payload = {**booking_payload, "firstname": "QA Day 6 Updated"}
    update_response = api_session.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=updated_payload,
        headers={"Cookie": f"token={auth_token}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert update_response.status_code == 200
    assert update_response.json()["firstname"] == updated_payload["firstname"]

    verify_response = api_session.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert verify_response.status_code == 200
    assert verify_response.json()["firstname"] == updated_payload["firstname"]

    delete_response = api_session.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert delete_response.status_code == 201

    final_response = api_session.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert final_response.status_code == 404
