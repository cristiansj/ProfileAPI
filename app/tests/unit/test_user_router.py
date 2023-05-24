from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_user():
    response = client.get("/users/123")
    assert response.status_code == 401

def test_update_user():
    response = client.put(
        "/users/123",
        json={"nombre": "John", "apellido": "Doe", "correo": "john.doe@example.com"}
    )
    assert response.status_code == 401

def test_delete_user():
    response = client.delete("/users/123")
    assert response.status_code == 401
