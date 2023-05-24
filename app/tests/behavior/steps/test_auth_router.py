from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login():
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "password"}
    )
    assert response.status_code == 200
    assert "token" in response.json()
