"""Offline examples for pytest fixtures, parametrization, marks, and cleanup."""

import json
import tempfile
from pathlib import Path
from types import MappingProxyType

import pytest


@pytest.fixture(scope="session")
def qe_context():
    """Stable, read-only project context shared for this pytest process."""
    return MappingProxyType({"service": "sample booking", "mode": "offline exercise"})


@pytest.fixture(scope="module")
def valid_booking_case():
    """Module-level sample input; callers should treat this template as read-only."""
    return MappingProxyType({
        "firstname": "Sam",
        "lastname": "Example",
        "totalprice": 120,
        "depositpaid": True,
    })


@pytest.fixture
def case_file(valid_booking_case):
    """Set up a temporary JSON case and remove it during fixture teardown."""
    with tempfile.TemporaryDirectory(
        prefix=".pytest-booking-",
        dir=Path(__file__).parent,
    ) as temp_dir:
        path = Path(temp_dir) / "booking.json"
        path.write_text(json.dumps(dict(valid_booking_case)), encoding="utf-8")
        yield path


def classify_status(status_code):
    """Return a simple HTTP status family for these local pytest examples."""
    if not isinstance(status_code, int) or isinstance(status_code, bool):
        raise TypeError("status_code must be an integer")
    if not 100 <= status_code <= 599:
        raise ValueError("status_code must be between 100 and 599")
    if status_code < 300:
        return "success"
    if status_code < 400:
        return "redirect"
    if status_code < 500:
        return "client_error"
    return "server_error"


@pytest.mark.smoke
def test_session_fixture_provides_project_context(qe_context):
    assert qe_context["service"] == "sample booking"
    assert qe_context["mode"] == "offline exercise"


@pytest.mark.data_driven
@pytest.mark.parametrize(
    ("status_code", "expected_family"),
    [
        pytest.param(200, "success", id="ok"),
        pytest.param(201, "success", id="created"),
        pytest.param(302, "redirect", id="redirect"),
        pytest.param(400, "client_error", id="bad-request"),
        pytest.param(404, "client_error", id="not-found"),
        pytest.param(500, "server_error", id="server-error"),
    ],
)
def test_status_code_is_classified(status_code, expected_family):
    assert classify_status(status_code) == expected_family


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_status",
    [pytest.param(99, id="below-http-range"), pytest.param(600, id="above-http-range")],
)
def test_status_code_outside_http_range_is_rejected(invalid_status):
    with pytest.raises(ValueError, match="between 100 and 599"):
        classify_status(invalid_status)


@pytest.mark.negative
def test_non_integer_status_code_is_rejected():
    with pytest.raises(TypeError, match="must be an integer"):
        classify_status("200")


def test_function_fixture_sets_up_json_case(case_file):
    case = json.loads(case_file.read_text(encoding="utf-8"))
    assert case["totalprice"] == 120
    assert case["depositpaid"] is True
# End of the offline pytest behavior examples.

