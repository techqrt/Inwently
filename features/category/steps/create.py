from behave import when, then
from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


# Scenario 1: Create a Category with a valid JWT token and valid data
@when('scenario 1 category I send a POST request with a valid JWT token and the following JSON body')
def create_category_with_valid_token(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    response = api.post_api(Endpoints.category_create, data={"name": "Electronics"}, headers=headers)
    context.response = response


@then('scenario 1 category the response status code should be 201')
def verify_status_code_201(context):
    assert context.response.status_code == 201, f"Expected 201 but got {context.response.status_code}"


@then('scenario 1 category response should contain:')
def verify_successful_category_creation(context):
    actual_response = context.response.json()
    expected_values = {"status": True, "message": "Category added successfully"}
    assert actual_response == expected_values


# Scenario 2: Create a Category with invalid or missing authentication

@when('scenario 2 category I send a POST request with an invalid JWT token and the proper JSON body')
def create_category_with_invalid_token(context):
    api = Apis()
    response = api.post_api(Endpoints.category_create, data={"name": "Electronics"},
                            headers={"Authorization": "Bearer invalid.token"})
    context.response = response


@then('scenario 2 category the response status code should be 401')
def verify_status_code_401(context):
    assert context.response.status_code == 401, f"Expected 401 but got {context.response.status_code}"


@then('scenario 2 category response should contain:')
def verify_authentication_failure(context):
    actual_response = context.response.json()
    assert actual_response["status"] is False
    assert isinstance(actual_response, dict)


# Scenario 3: Create a Category with invalid or missing name

@when('scenario 3 category I send a POST request with the following JSON body:')
def create_category_with_invalid_name(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    response = api.post_api(Endpoints.category_create, data={"name": None}, headers=headers)
    context.response = response


@then('scenario 3 category the response status code should be 400')
def verify_status_code_400(context):
    assert context.response.status_code == 400, f"Expected 400 but got {context.response.status_code}"


@then('scenario 3 response should contain:')
def verify_validation_error(context):
    actual_response = context.response.json()
    assert actual_response["status"] is False
    assert isinstance(actual_response, dict)
    assert 'error' in actual_response.keys()
