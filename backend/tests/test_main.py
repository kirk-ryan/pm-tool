from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_api_test_returns_json():
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "API is working", "status": "success"}
