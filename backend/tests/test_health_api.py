from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "AEGIS",
    }


def test_root_returns_service_info():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "AEGIS"
    assert "version" in response.json()
