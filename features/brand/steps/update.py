from behave import when, then

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


# Scenario 1: Create a Brand with a valid JWT token and valid data
@when('scenario 1 I send a PUT request with a valid jwt token and the following JSON body:')
def step_imp(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    api.post_api(Endpoints.brand_create, data={"name": "cafe"}, headers=headers)
    brands = api.get_api(url=Endpoints.brand_get_all, param={}, headers=headers)
    brand_code1 = brands.json()["data"]["data"][0]["brandCode"]
    response = api.put_api(url=Endpoints.brand_update, data={'brand_code': brand_code1, "name": "cloud cocktails"}, headers=headers)
    context.response = response


@then('scenario 1 update the response status code should be 200')
def step_imp(context):
    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}"


@then('scenario 1 update the response should contain:')
def step_imp(context):
    actual_response = context.response.json()
    assert actual_response["status"] == True
    assert actual_response["message"] == "Brand updated successfully"