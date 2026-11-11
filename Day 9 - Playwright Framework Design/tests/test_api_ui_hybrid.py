import pytest
from playwright.sync_api import expect


@pytest.mark.api
@pytest.mark.ui
def test_api_created_record_is_visible_in_ui(page, demo_api, demo_base_url):
    payload = {
        "title": "Day 9 API-created record",
        "description": "Created over the API and verified in the browser UI.",
    }

    response = demo_api.post("/api/records", data=payload)

    assert response.status == 201
    created_record = response.json()
    assert created_record["title"] == payload["title"]
    assert created_record["description"] == payload["description"]

    page.goto(f"{demo_base_url}/records/{created_record['id']}")

    expect(page.get_by_role("heading", name="Record details")).to_be_visible()
    expect(page.get_by_test_id("record-id")).to_have_text(created_record["id"])
    expect(page.get_by_test_id("record-title")).to_have_text(payload["title"])
    expect(page.get_by_test_id("record-description")).to_have_text(payload["description"])
