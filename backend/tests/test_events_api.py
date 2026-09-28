from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_events_returns_events():
    response = client.get("/api/events")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 4


def test_get_events_returns_expected_event_fields():
    response = client.get("/api/events")

    assert response.status_code == 200

    data = response.json()
    event = data[0]

    assert event["event_id"] == "evt_001"
    assert event["source"] == "AUTH"
    assert event["user"] == "rahul"
    assert event["severity"] == "low"


def test_get_events_contains_security_scenarios():
    response = client.get("/api/events")

    assert response.status_code == 200

    data = response.json()

    event_types = {event["event_type"] for event in data}

    assert "LOGIN_FAILURE" in event_types
    assert "AUTH_SUCCESS" in event_types
    assert "DATA_ACCESS" in event_types
    