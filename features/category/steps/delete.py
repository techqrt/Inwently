from behave import when, then
from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


# Scenario 1: Delete a Category with a valid JWT token and valid data
@when('scenario 1 category I send a DELETE request with a valid JWT token and the following JSON body:')
def delete_category_with_valid_token(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}

    # First, create a category to delete
    api.post_api(Endpoints.category_create, data={"name": "Electronics"}, headers=headers)

    # Fetch the category code
    categories = api.get_api(url=Endpoints.category_get_all, param={}, headers=headers)
    category_code = categories.json()["data"]["data"][0]["categoryCode"]

    # Send DELETE request
    response = api.delete_api(url=Endpoints.category_delete, data={"category_code": category_code}, headers=headers)
    context.response = response


@then('scenario 1 category delete the response status code should be 200')
def verify_status_code_200(context):
    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}"


@then('scenario 1 category delete the response should contain:')
def verify_successful_category_deletion(context):
    actual_response = context.response.json()
    expected_values = {"status": True, "message": "Category delete successfully"}
    assert actual_response == expected_values



