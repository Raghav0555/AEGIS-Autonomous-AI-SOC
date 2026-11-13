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


def test_get_events_filters_by_source():
    response = client.get("/api/events?source=http")

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    assert all(event["source"] == "HTTP" for event in data)


def test_post_event_requires_core_fields():
    response = client.post("/api/events", json={"event_id": "evt_999"})

    assert response.status_code == 422


def test_post_event_returns_event():
    payload = {
        "event_id": "evt_999",
        "timestamp": "2026-09-25T10:00:00",
        "event_type": "LOGIN_SUCCESS",
        "source": "AUTH",
    }

    response = client.post("/api/events", json=payload)

    assert response.status_code == 200
    assert response.json()["event_id"] == "evt_999"
    assert response.json()["severity"] == "low"
