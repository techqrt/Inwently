from behave import when, then

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


# Scenario 1: Create a Brand with a valid JWT token and valid data
@when('scenario 1 I send a PATCH request with valid jwt token and the following JSON body')
def step_imp(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    api.post_api(Endpoints.brand_create, data={"name": "cafe"}, headers=headers)
    api.post_api(Endpoints.brand_create, data={"name": "cafe2"}, headers=headers)
    brands = api.get_api(url=Endpoints.brand_get_all, param={}, headers=headers)
    brand_code1 = brands.json()["data"]["data"][0]["brandCode"]
    brand_code2 = brands.json()["data"]["data"][1]["brandCode"]
    response = api.patch_api(url=Endpoints.brand_delete_many, data={'brand_code': [brand_code1,brand_code2]}, headers=headers)
    context.response = response


@then('scenario 1 delete many the response status code should be 200')
def step_imp(context):
    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}"


@then('scenario 1 delete many the response should contain:')
def step_imp(context):
    actual_response = context.response.json()
    assert actual_response["status"] == True
    assert actual_response["message"] == "Brand delete successfully"