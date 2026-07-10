from behave import when, then

from biller_apps.employees.models.employees import Employees
from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


# Scenario 1: Create a Brand with a valid JWT token and valid data
@when('scenario 1 I send a POST request with a valid JWT token and the following JSON body')
def create_brand_with_valid_token(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    response = api.post_api(Endpoints.brand_create, data={"name": "cafe"}, headers=headers)
    context.response = response


@then('scenario 1 the response status code should be 201')
def verify_status_code_201(context):
    assert context.response.status_code == 201, f"Expected 201 but got {context.response.status_code}"


@then('scenario 1 response should contain:')
def verify_successful_brand_creation(context):
    actual_response = context.response.json()
    expected_values = {"status": True, "message": "Brand added successfully"}
    assert actual_response == expected_values


# Scenario 2: Create a Brand with invalid or missing authentication

@when('scenario 2 I send a POST request with an invalid JWT token and the proper JSON body')
def create_brand_with_invalid_token(context):
    api = Apis()
    response = api.post_api(Endpoints.brand_create, data={"name": "cafe"},
                            headers={"Authorization": "Bearer asdkasdkak.jsladlkjfjdf.asdasjflakfj"})
    context.response = response


@then('scenario 2 the response status code should be 401')
def verify_status_code_401(context):
    assert context.response.status_code == 401, f"Expected 401 but got {context.response.status_code}"


@then('scenario 2 response should contain:')
def verify_authentication_failure(context):
    actual_response = context.response.json()
    assert actual_response["status"] == False
    assert isinstance(actual_response, dict)


# Scenario 3: Create a Brand with a valid name
@when('scenario 3 I send a POST request with the following JSON body:')
def create_brand_with_valid_name(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    resp = Employees.objects.all()
    payload = {
        "name": "cloud cafe"
    }
    response = api.post_api(Endpoints.brand_create, data=payload, headers=headers)
    context.response = response


@then('scenario 3 the response status code should be 201')
def verify_status_code_201_scenario_3(context):
    assert context.response.status_code == 201, f"Expected 201 but got {context.response.status_code}"


@then('scenario 3 response should contain:')
def verify_successful_brand_creation_scenario_3(context):
    actual_response = context.response.json()
    expected_values = {"status": True, "message": "Brand added successfully"}
    assert actual_response == expected_values


# Scenario 4: Create a Brand with invalid or missing name

@when('scenario 4 I send a POST request with the following JSON body:')
def create_brand_with_invalid_name(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    response = api.post_api(Endpoints.brand_create, data={"name": None}, headers=headers)
    context.response = response


@then('scenario 4 the response status code should be 400')
def verify_status_code_400(context):
    assert context.response.status_code == 400, f"Expected 400 but got {context.response.status_code}"


@then('scenario 4 response should contain:')
def verify_validation_error(context):
    actual_response = context.response.json()
    assert actual_response["status"] == False
    assert isinstance(actual_response, dict)
    assert 'error' in actual_response.keys()
