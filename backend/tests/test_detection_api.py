from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_detection_health():
    response = client.get("/api/detection/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "detection-engine",
    }