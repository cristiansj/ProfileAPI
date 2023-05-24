from behave import given, when, then
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
token = "valid_token"  # Token de prueba válido para realizar las operaciones

@given("an authenticated user")
def step_given_authenticated_user(context):
    context.token = token

@when("the user requests their own information")
def step_when_user_requests_information(context):
    response = client.get(
        "/user",
        headers={"Authorization": f"Bearer {context.token}"}
    )
    context.response = response

@when("the user updates their information")
def step_when_user_updates_information(context):
    response = client.put(
        "/user",
        json={"nombre": "Jane", "apellido": "Doe"},
        headers={"Authorization": f"Bearer {context.token}"}
    )
    context.response = response

@when("the user deletes their account")
def step_when_user_deletes_account(context):
    response = client.delete(
        "/user",
        headers={"Authorization": f"Bearer {context.token}"}
    )
    context.response = response

@then("the user details should be returned")
def step_then_user_details_returned(context):
    assert context.response.status_code == 200
    assert "id" in context.response.json()
    assert "nombre" in context.response.json()
    assert "apellido" in context.response.json()
    assert "correo" in context.response.json()

@then("the user details should be updated")
def step_then_user_details_updated(context):
    assert context.response.status_code == 200
    assert context.response.json().get("nombre") == "Jane"
    assert context.response.json().get("apellido") == "Doe"

@then("the user should be deleted")
def step_then_user_deleted(context):
    assert context.response.status_code == 200
    assert context.response.json().get("message") == "User deleted"