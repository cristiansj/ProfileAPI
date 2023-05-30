from behave import given, when, then
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@given('the API is running')
def step_given_api_running(context):
    # No se requiere ninguna acción ya que se asume que la API está en funcionamiento
    pass

@when('I send a POST request to "/login" with the following data:')
def step_when_send_post_request_with_data(context):
    data = {}
    for row in context.table:
        key = row["username"]
        value = row["password"]
        data[key] = value

    context.response = client.post("/login", json=data)

@then('the response status code should be 200')
def step_then_check_status_code_200(context):
    assert context.response.status_code == 200

@then('the response body should contain a "token" field')
def step_then_check_response_body_token_field(context):
    response_data = context.response.json()
    assert "token" in response_data

