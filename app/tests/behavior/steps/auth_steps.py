from behave import given, when, then
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@given('a user with username "{username}" and password "{password}"')
def step_given_user_credentials(context, username, password):
    context.username = username
    context.password = password

@when("the user logs in with username and password")
def step_when_user_logs_in(context):
    response = client.post(
        "/login",
        data={"username": context.username, "password": context.password}
    )
    context.response = response

@then("a token should be returned")
def step_then_token_returned(context):
    assert context.response.status_code == 200
    assert "access_token" in context.response.json()

@then("an error message should be returned")
def step_then_error_message_returned(context):
    assert context.response.status_code == 401
    assert "detail" in context.response.json()
