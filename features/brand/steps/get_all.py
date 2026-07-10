from behave import when, then

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


# Scenario 1: Create a Brand with a valid JWT token and valid data
@when('Scenario 1 call the get all api with a GET request with query parameters:')
def step_imp(context):
    api = Apis()
    headers = {"Authorization": f"Bearer {api.access_token}"}
    api.post_api(Endpoints.brand_create, data={"name": "cafe"}, headers=headers)
    api.post_api(Endpoints.brand_create, data={"name": "cafe2"}, headers=headers)
    response = api.get_api(url=Endpoints.brand_get_all, param={}, headers=headers)
    context.response = response


@then('scenario 1 the response status code should be 200')
def step_imp(context):
    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}"


@then('Scenario 1 the response should contain following pattern:')
def step_imp(context):
    actual_response = context.response.json()
    assert actual_response["status"] == True
    data =  actual_response["data"]
    print(data)
    assert len(data["data"]) > 1
    assert isinstance(data["presentPage"] ,int)
    assert isinstance(data["totalCount"], int)
    assert isinstance(data["totalPage"], int)