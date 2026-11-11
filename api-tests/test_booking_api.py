"""API checks for the public Restful Booker learning service."""

import csv
import os
from pathlib import Path
from types import MappingProxyType

import pytest
import requests

import json
from jsonschema import Draft202012Validator


@pytest.mark.api
@pytest.mark.regression
def test_existing_booking_matches_json_schema(
    api_session, api_config, booking_factory
):
    booking_id, _ = booking_factory()
    response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == 200

    booking = response.json()

    schema_path = (
        Path(__file__).parent
        / "schemas"
        / "booking_schema.json"
    )

    with schema_path.open(encoding="utf-8") as schema_file:
        schema = json.load(schema_file)

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(booking))

    assert not errors, (
        "Booking response does not match the schema:\n"
        + "\n".join(error.message for error in errors)
    )


pytestmark = pytest.mark.api


@pytest.fixture(scope="module")
def api_config():
    """Load stable API settings once; keep shared configuration read-only."""
    return MappingProxyType(
        {
            "base_url": os.getenv(
                "RESTFUL_BOOKER_BASE_URL",
                "https://restful-booker.herokuapp.com",
            ).rstrip("/"),
            "timeout_seconds": 15,
            "username": os.getenv("RESTFUL_BOOKER_USERNAME", "admin"),
            "password": os.getenv("RESTFUL_BOOKER_PASSWORD", "password123"),
        }
    )


@pytest.fixture
def api_session():
    """Provide a requests.Session with common headers and a bounded timeout per call."""
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


@pytest.fixture
def auth_token(api_session, api_config):
    """Authenticate once for a test and return its token."""
    response = api_session.post(
        f"{api_config['base_url']}/auth",
        json={
            "username": api_config["username"],
            "password": api_config["password"],
        },
        timeout=api_config["timeout_seconds"],
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
def booking_factory(api_session, auth_token, booking_payload, api_config):
    """Create test-owned bookings and remove any that remain after the test."""
    created_ids = []
    auth_headers = {"Cookie": f"token={auth_token}"}

    def create_booking(overrides=None):
        payload = {**booking_payload, **(overrides or {})}
        response = api_session.post(
            f"{api_config['base_url']}/booking",
            json=payload,
            timeout=api_config["timeout_seconds"],
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
            f"{api_config['base_url']}/booking/{booking_id}",
            timeout=api_config["timeout_seconds"],
        )
        if get_response.status_code == 200:
            delete_response = api_session.delete(
                f"{api_config['base_url']}/booking/{booking_id}",
                headers=auth_headers,
                timeout=api_config["timeout_seconds"],
            )
            assert delete_response.status_code == 201
        else:
            assert get_response.status_code == 404


@pytest.mark.smoke
def test_get_bookings(api_session, api_config):
    response = api_session.get(
        f"{api_config['base_url']}/booking",
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == 200
    assert "json" in response.headers.get("Content-Type", "").lower()
    bookings = response.json()
    assert isinstance(bookings, list)
    assert all(isinstance(item.get("bookingid"), int) for item in bookings)


@pytest.mark.smoke
def test_get_existing_booking(api_session, booking_factory, api_config):
    booking_id, _ = booking_factory()

    response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == 200
    booking = response.json()
    assert booking["firstname"] == "QA Day 6"
    assert isinstance(booking["lastname"], str)
    assert isinstance(booking["bookingdates"], dict)
    assert isinstance(booking["bookingdates"]["checkin"], str)
    assert isinstance(booking["bookingdates"]["checkout"], str)


@pytest.mark.negative
@pytest.mark.regression
def test_get_nonexistent_booking(api_session, api_config):
    response = api_session.get(
        f"{api_config['base_url']}/booking/999999999",
        timeout=api_config["timeout_seconds"],
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
@pytest.mark.negative
@pytest.mark.data_driven
@pytest.mark.regression
def test_booking_id_boundaries(api_session, booking_id, api_config):
    """Exercise representative invalid ID values around the positive ID domain."""
    response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == 404


@pytest.mark.negative
@pytest.mark.regression
def test_booking_id_with_text(api_session, api_config):
    response = api_session.get(
        f"{api_config['base_url']}/booking/abc",
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == 404


@pytest.mark.regression
def test_booking_response_is_json(api_session, booking_factory, api_config):
    booking_id, _ = booking_factory()
    response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
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
@pytest.mark.data_driven
@pytest.mark.regression
def test_totalprice_numeric_boundary_values(booking_factory, totalprice):
    """Check numeric values around zero; the API contract sets no minimum price."""
    _, response_body = booking_factory({"totalprice": totalprice})

    assert isinstance(response_body["booking"].get("totalprice"), (int, float))
    assert response_body["booking"]["totalprice"] == totalprice


@pytest.mark.negative
@pytest.mark.regression
def test_invalid_auth_credentials_return_reason(api_session, api_config):
    response = api_session.post(
        f"{api_config['base_url']}/auth",
        json={"username": "invalid-user", "password": "invalid-password"},
        timeout=api_config["timeout_seconds"],
    )

    # Restful Booker returns HTTP 200 with a reason body for bad login details.
    assert response.status_code == 200
    assert isinstance(response.json().get("reason"), str)
    assert response.json()["reason"]


@pytest.mark.negative
@pytest.mark.regression
def test_update_without_authentication_is_forbidden(
    api_session, booking_factory, booking_payload, api_config
):
    booking_id, _ = booking_factory()
    response = api_session.put(
        f"{api_config['base_url']}/booking/{booking_id}",
        json=booking_payload,
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == 403


@pytest.mark.negative
@pytest.mark.regression
def test_update_with_missing_required_fields_returns_bad_request(
    api_session, auth_token, booking_factory, api_config
):
    booking_id, _ = booking_factory()
    response = api_session.put(
        f"{api_config['base_url']}/booking/{booking_id}",
        json={"firstname": "Incomplete"},
        headers={"Cookie": f"token={auth_token}"},
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == 400


@pytest.mark.crud
@pytest.mark.regression
def test_booking_crud_lifecycle(
    api_session, booking_factory, booking_payload, auth_token, api_config
):
    booking_id, create_body = booking_factory()
    assert create_body["booking"]["firstname"] == booking_payload["firstname"]

    get_response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
    )
    assert get_response.status_code == 200
    assert get_response.json()["firstname"] == booking_payload["firstname"]

    updated_payload = {**booking_payload, "firstname": "QA Day 6 Updated"}
    update_response = api_session.put(
        f"{api_config['base_url']}/booking/{booking_id}",
        json=updated_payload,
        headers={"Cookie": f"token={auth_token}"},
        timeout=api_config["timeout_seconds"],
    )
    assert update_response.status_code == 200
    assert update_response.json()["firstname"] == updated_payload["firstname"]

    verify_response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
    )
    assert verify_response.status_code == 200
    assert verify_response.json()["firstname"] == updated_payload["firstname"]

    delete_response = api_session.delete(
        f"{api_config['base_url']}/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=api_config["timeout_seconds"],
    )
    assert delete_response.status_code == 201

    final_response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
    )
    assert final_response.status_code == 404

def load_booking_id_cases():
    csv_path = (
        Path(__file__).parent
        / "data"
        / "booking_id_cases.csv"
    )

    with csv_path.open(
        newline="",
        encoding="utf-8"
    ) as csvfile:
        return [
            (
                int(row["booking_id"]),
                int(row["expected_status"])
            )
            for row in csv.DictReader(csvfile)
        ]


@pytest.mark.parametrize(
    "booking_id, expected_status",
    load_booking_id_cases(),
)
@pytest.mark.data_driven
@pytest.mark.regression
def test_booking_ids_from_csv(
    api_session,
    booking_id,
    expected_status,
    api_config,
):
    response = api_session.get(
        f"{api_config['base_url']}/booking/{booking_id}",
        timeout=api_config["timeout_seconds"],
    )

    assert response.status_code == expected_status
