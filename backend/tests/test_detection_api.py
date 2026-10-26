from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_run_detection_returns_alert_summary():
    response = client.post("/api/detection/run")

    assert response.status_code == 200

    data = response.json()
    assert data["events_analyzed"] > 0
    assert data["alerts_generated"] == len(data["alerts"])


def test_run_detection_alerts_have_required_fields():
    response = client.post("/api/detection/run")

    assert response.status_code == 200

    for alert in response.json()["alerts"]:
        assert "event_id" in alert
        assert "rule" in alert
        assert "severity" in alert
        assert "reason" in alert
        
def test_run_detection_with_no_events():
    with patch("app.api.routes.detection.load_events", return_value=[]):
        response = client.post("/api/detection/run")

    assert response.status_code == 200
    assert response.json() == {
        "events_analyzed": 0,
        "alerts_generated": 0,
        "alerts": [],
    }
def test_run_detection_filters_by_severity():
    response = client.post(
        "/api/detection/run?severity=critical"
    )

    assert response.status_code == 200

    data = response.json()
    assert all(
        alert["severity"] == "critical"
        for alert in data["alerts"]
    )
    assert data["alerts_generated"] == len(data["alerts"])


def test_run_detection_rejects_invalid_severity():
    response = client.post(
        "/api/detection/run?severity=urgent"
    )

    assert response.status_code == 422

def test_run_detection_filters_by_high_severity():
    response = client.post(
        "/api/detection/run?severity=high"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["events_analyzed"] > 0
    assert all(
        alert["severity"] == "high"
        for alert in data["alerts"]
    )


def test_detection_health():
    response = client.get("/api/detection/health")

    assert response.status_code == 200
    assert response.json()["service"] == "detection-engine"
