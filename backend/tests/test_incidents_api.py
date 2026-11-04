from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_incidents_returns_incidents():
    response = client.get("/api/incidents")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    incident = data[0]

    assert "incident_id" in incident
    assert "severity" in incident
    assert "confidence" in incident
    assert "events" in incident


def test_incidents_include_event_references():
    response = client.get("/api/incidents")

    assert response.status_code == 200

    for incident in response.json():
        assert isinstance(incident["events"], list)


def test_incidents_filter_by_severity():
    response = client.get("/api/incidents?severity=critical")

    assert response.status_code == 200
    assert all(
        incident["severity"] == "critical"
        for incident in response.json()
    )


def test_incidents_reject_unknown_severity():
    response = client.get("/api/incidents?severity=bad")

    assert response.status_code == 422
