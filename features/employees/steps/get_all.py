import json

from behave import given, when, then, step

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


class EmployeesGetAllWithoutParameters:
    sample_response = None
    response = None

    @given("A sample response is present in folder steps/common/sample_response/employees_get_all json")
    def step_impl(context):
        with open('features\steps\common\sample_response\employees_get_all.json', 'r') as file:
            data = json.load(file)
        EmployeesGetAllWithoutParameters.sample_response = data

    @when("Call the employees get_all api")
    def step_impl(context):
        url = Endpoints.employees_get_all
        EmployeesGetAllWithoutParameters.response = Apis().get(url=url)

    @then("Check the response of employees get_all status is 200")
    def step_impl(context):
        assert EmployeesGetAllWithoutParameters.response.status_code == 200

    @step("the response content type should be dict for employees get_all")
    def step_impl(context):
        assert isinstance(EmployeesGetAllWithoutParameters.response.json(), dict)

    @step("the response body should contain the keys mentioned in employees_get_all json file without next page url")
    def step_impl(context):
        response_data = EmployeesGetAllWithoutParameters.response.json()
        if "next_page_url" in response_data:
            del response_data["next_page_url"]
        assert set(response_data.keys()) == set(EmployeesGetAllWithoutParameters.sample_response.keys())


class EmployeesGetAllWithoutParametersWithWrongToken:
    response = None
    wrong_token = None

    @given("create jwt token manualy for employees get all api")
    def step_create_wrong_jwt_token(context):
        context.wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcnkiOiIyMDI1LTAxLTE1IDEyOjQ1OjA0Ljg0NjQ4MCswMDAwIiwidXNlcl9zcGVjaWZpY19kYXRhIjp7Im9yZ2FuaXNhdGlvbk5hbWUiOiJUZWNoYXNvIiwibmFtZSI6ImFkbWluIiwiZW1wbG95ZWVDb2RlIjoiVF8xIiwiZW1haWxJZCI6ImFkbWluQHRlY2hhc28ub3JnIiwicHJvZmlsZVBob3RvVXJsIjoiIiwic2hvcEFjY2Vzc0xpc3QiOltdLCJhcHByb3ZhbCI6ZmFsc2V9LCJwZXJtaXNzaW9ucyI6eyJtYXN0ZXIiOnsiaXRlbSI6dHJ1ZSwic2hvcCI6dHJ1ZSwic3VwcGxpZXIiOnRydWUsImN1c3RvbWVyIjp0cnVlLCJjcmVhdGUiOnRydWUsImVtcGxveWVlIjp0cnVlfSwiaW52ZW50b3J5Ijp7ImludmVudG9yeSI6dHJ1ZX0sImJpbGxpbmciOnsicG9zIjp0cnVlLCJyZXR1cm5faXRlbSI6dHJ1ZSwiYmlsbF9oaXN0b3J5Ijp0cnVlfSwicmVwb3J0cyI6eyJnZW5lcmFsIjp0cnVlLCJvdmVydmlldyI6dHJ1ZSwiYWRtaW5pc3RyYXRpb24iOnRydWUsImRheV9ib29rIjp0cnVlLCJnc3QiOnRydWV9LCJwcmludGVyX3RlbXBsYXRlcyI6eyJwcmludGVyX3RlbXBsYXRlcyI6dHJ1ZX0sImRhc2hib2FyZCI6eyJkYXNoYm9hcmQiOnRydWV9LCJzdG9jayI6eyJwdXJjaGFzZV9saXN0Ijp0cnVlLCJyZXR1cm5fcHVyY2hhc2UiOnRydWUsInN0b2NrIjp0cnVlfSwicXVvdGF0aW9ucyI6eyJxdW90YXRpb25zIjp0cnVlfX19.YoWHWwJRtMk-FIg1G41zYfNO6-NJBy0iAUE4-tKuMfY"

    @when("Call the employees get_all api with wrong jwt token")
    def step_api_call_wrong_token(context):
        url = Endpoints.employees_get_all
        headers = {"Authorization": f"Bearer {context.wrong_token}"}
        EmployeesGetAllWithoutParametersWithWrongToken.response = Apis().get(url=url, headers=headers)

    @then("Check the response of employees get_all status is 401 and should be a dict type")
    def step_response_status_and_type(context):
        assert EmployeesGetAllWithoutParametersWithWrongToken.response.status_code == 401
        assert isinstance(EmployeesGetAllWithoutParameters.response.json(), dict)

    @step("the response content should contain Authentication Error message")
    def step_authentication_error(context):
        response_data = EmployeesGetAllWithoutParametersWithWrongToken.response.json()
        assert "error" in response_data

class EmployeesGetAllWithInvalidQueryParametersScene1:
    response = None
    url = None

    @given('I have the API endpoint "/employees/get_all/"')
    def step_api_end_point(context):
        context.url = Endpoints.employees_get_all

    @when("I send a GET request with query parameters with scenario 1")
    def step_when_get_request(context):
        params = {
            "limit": -1,
            "page_num": 0,
            "sort_by": "name",
            # "sort_order": "unknown",
        }
        EmployeesGetAllWithInvalidQueryParametersScene1.response = Apis().get(url=context.url, data=params)


    @then("the get response status code should be 400")
    def response_status_code(context):
        assert EmployeesGetAllWithInvalidQueryParametersScene1.response.status_code == 400


    @step("the get response should contain value error")
    def step_response_value_error(context):
        response = {
            "status" : False,
            "message" : "Value Error The given page number is greater than maximum available limit"
        }
        response_data = EmployeesGetAllWithInvalidQueryParametersScene1.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]

class EmployeesGetAllWithInvalidQueryParametersScene2:
    response = None

    @when("I send a GET request with query parameters with scenario 2")
    def step_when_get_request(context):
        url = Endpoints.employees_get_all
        params = {
            "limit": 1,
            "page_num": 0,
            "sort_by": "name",
            # "sort_order": "unknown",
        }
        EmployeesGetAllWithInvalidQueryParametersScene2.response = Apis().get(url=url, data=params)

    @step("the get response should contain exception error")
    def step_response_exception_error(context):
        response = {
            "status" : False,
            "message" : "Exception Error That page number is less than 1"
        }
        response_data = EmployeesGetAllWithInvalidQueryParametersScene2.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]



class EmployeesGetAllWithUnsupportedSorting:
    response = None
    url = None

    @given('I have a valid JWT token "valid.jwt.token"')
    def step_valid_jwt_token(context):
        context.url = Endpoints.employees_get_all
        response = Apis().get(url=context.url)
        assert response.status_code == 200

    @when("I send a GET request with query parameters")
    def step_when_get_request(context):
        params = {
            "limit": 20,
            "page_num": 1,
            "sort_by": "name",
            "sort_order": "unsupported",
        }
        EmployeesGetAllWithInvalidQueryParametersScene2.response = Apis().get(url=context.url, data=params)

    @step("the get response should contain validation error")
    def step_response_validation_error(context):
        response = {
            "status" : False,
            "message" : "Validation Error"
        }
        response_data = EmployeesGetAllWithInvalidQueryParametersScene2.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]









