from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_incidents_returns_incidents():
    response = client.get("/api/incidents")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0