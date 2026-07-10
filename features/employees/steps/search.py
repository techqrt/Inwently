
from behave import given, when, then, step

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


class SearchEmployeeWithValidJwtTokenAndValidSearchKey:
    url = None
    response = None

    @given('I have the API endpoint "/employees/search/"')
    def step_api_end_point(context):
        context.url = Endpoints.employees_search

    @given('I have a valid JWT token "valid.jwt.token" to search employees')
    def step_valid_jwt_token(context):
        params = {
            "key" : "admin"
        }
        response = Apis().get(url=context.url,data=params)
        assert response.status_code == 200


    @when("I send a GET request with query parameters with key admin")
    def step_get_request_with_key_admin(context):
        api_client = Apis()
        params = {
            "key": "admin",
            "limit": 20,
            "page_num": 1,
        }
        SearchEmployeeWithValidJwtTokenAndValidSearchKey.response = api_client.get(url=context.url, data=params)


    @then("the search response status code with valid search key should be 200")
    def step_response_status_200(context):
        assert SearchEmployeeWithValidJwtTokenAndValidSearchKey.response.status_code == 200

    @step("the search response with valid search key should contain data fetched successfully")
    def step_response_data_fetched_successfully(context):
        response = {
            "status": True,
            "message": "Data fetched successfully",
        }
        response_data = SearchEmployeeWithValidJwtTokenAndValidSearchKey.response.json()
        assert response_data["status"] == response["status"]
        assert response_data["message"] == response["message"]
        assert any(
            employee['name'] == 'admin' and
            employee['mobileNumber'] == '0342' and
            employee['isActive'] == True and
            employee['employeeCode'] == 'T_01' and
            employee['dob'] == '2020-01-01' and
            employee['profilePhotoUrl'] == ''
            for employee in response_data["data"]["data"]
        )

class SearchEmployeeWithValidJwtTokenAndNoSearchKey:
    response = None

    @when("I send a GET request with query parameters without key")
    def step_get_request_without_key(context):
        url = Endpoints.employees_search
        api_client = Apis()
        params = {
            "limit": 20,
            "page_num": 1,
        }
        SearchEmployeeWithValidJwtTokenAndNoSearchKey.response = api_client.get(url=url, data=params)

    @then("the search response status code with no search key should be 400")
    def step_response_status_400(context):
        assert SearchEmployeeWithValidJwtTokenAndNoSearchKey.response.status_code == 400

    @step("the search response with no search key should contain validation error")
    def step_response_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error"
        }
        response_data = SearchEmployeeWithValidJwtTokenAndNoSearchKey.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]


class SearchEmployeeWithInvalidJwtToken:
    wrong_token = None
    response = None

    @given('I have an invalid JWT token "invalid.jwt.token" to search employees')
    def step_create_wrong_jwt_token(context):
        context.wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcnkiOiIyMDI1LTAxLTE1IDEyOjQ1OjA0Ljg0NjQ4MCswMDAwIiwidXNlcl9zcGVjaWZpY19kYXRhIjp7Im9yZ2FuaXNhdGlvbk5hbWUiOiJUZWNoYXNvIiwibmFtZSI6ImFkbWluIiwiZW1wbG95ZWVDb2RlIjoiVF8xIiwiZW1haWxJZCI6ImFkbWluQHRlY2hhc28ub3JnIiwicHJvZmlsZVBob3RvVXJsIjoiIiwic2hvcEFjY2Vzc0xpc3QiOltdLCJhcHByb3ZhbCI6ZmFsc2V9LCJwZXJtaXNzaW9ucyI6eyJtYXN0ZXIiOnsiaXRlbSI6dHJ1ZSwic2hvcCI6dHJ1ZSwic3VwcGxpZXIiOnRydWUsImN1c3RvbWVyIjp0cnVlLCJjcmVhdGUiOnRydWUsImVtcGxveWVlIjp0cnVlfSwiaW52ZW50b3J5Ijp7ImludmVudG9yeSI6dHJ1ZX0sImJpbGxpbmciOnsicG9zIjp0cnVlLCJyZXR1cm5faXRlbSI6dHJ1ZSwiYmlsbF9oaXN0b3J5Ijp0cnVlfSwicmVwb3J0cyI6eyJnZW5lcmFsIjp0cnVlLCJvdmVydmlldyI6dHJ1ZSwiYWRtaW5pc3RyYXRpb24iOnRydWUsImRheV9ib29rIjp0cnVlLCJnc3QiOnRydWV9LCJwcmludGVyX3RlbXBsYXRlcyI6eyJwcmludGVyX3RlbXBsYXRlcyI6dHJ1ZX0sImRhc2hib2FyZCI6eyJkYXNoYm9hcmQiOnRydWV9LCJzdG9jayI6eyJwdXJjaGFzZV9saXN0Ijp0cnVlLCJyZXR1cm5fcHVyY2hhc2UiOnRydWUsInN0b2NrIjp0cnVlfSwicXVvdGF0aW9ucyI6eyJxdW90YXRpb25zIjp0cnVlfX19.YoWHWwJRtMk-FIg1G41zYfNO6-NJBy0iAUE4-tKuMfY"

    @when("I send a GET request with query parameters key john")
    def step_when_get_request(context):
        url = Endpoints.employees_search
        headers = {"Authorization": f"Bearer {context.wrong_token}"}
        params = {
            "key": "john",
            "limit": 20,
            "page_num": 1,
        }
        SearchEmployeeWithInvalidJwtToken.response = Apis().get(url=url,headers=headers, data=params)

    @then("the response status with invalid jwt token code should be 401")
    def step_response_status_401(context):
        assert SearchEmployeeWithInvalidJwtToken.response.status_code == 401

    @step("the search response with invalid jwt token should contain authentication error")
    def step_response_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = SearchEmployeeWithInvalidJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data


class SearchEmployeeWithoutJwtToken:
    response = None

    @when("I send a GET request without an authorization token")
    def step_when_get_request(context):
        url = Endpoints.employees_search
        headers = {"Authorization": f"Bearer "}
        SearchEmployeeWithoutJwtToken.response = Apis().get(url=url, headers=headers)

    @then("the response status code without jwt token should be 401")
    def step_response_status_401(context):
        assert SearchEmployeeWithoutJwtToken.response.status_code == 401

    @step("the search response without jwt token should contain authentication error")
    def step_response_authentication_error(context):
        response_data = SearchEmployeeWithoutJwtToken.response.json()
        assert "error" in response_data

class SearchEmployeeWithInvalidLimitValue:
    response = None

    @when("I send a GET request with query parameters limit invalid_value")
    def step_when_get_request(context):
        url = Endpoints.employees_search
        params = {
            "key": "john",
            "limit": "invalid_value",
            "page_num": 1,
        }
        SearchEmployeeWithInvalidLimitValue.response = Apis().get(url=url, data=params)

    @then("the search response status code for invalid limit value should be 400")
    def step_response_status_400(context):
        assert SearchEmployeeWithInvalidLimitValue.response.status_code == 400

    @step("the search response for invalid limit value should contain validation error")
    def step_response_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error"
        }
        response_data = SearchEmployeeWithInvalidLimitValue.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]

class SearchEmployeeWithNegativePageNumber:
    response = None

    @when("I send a GET request with query parameters page_num -1")
    def step_when_get_request(context):
        url = Endpoints.employees_search
        params = {
            "key": "admin",
            "limit": "20",
            "page_num": "a1",
        }
        SearchEmployeeWithNegativePageNumber.response = Apis().get(url=url, data=params)

    @then("the search response status for negative page number code should be 400")
    def step_response_status_400(context):
        assert SearchEmployeeWithNegativePageNumber.response.status_code == 400

    @step("the search response for negative page number should contain validation error")
    def step_response_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error"
        }
        response_data = SearchEmployeeWithNegativePageNumber.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]

class SearchEmployeeWithUnsupportedSortingOrder:
    response = None

    @when("I send a GET request with query parameters sort_order unsupported")
    def step_when_get_request(context):
        url = Endpoints.employees_search
        params = {
            "key": "admin",
            "limit": "20",
            "page_num": 1,
            "sort_order": "unsupported",
            "sort_key" : "unsupported",
        }
        SearchEmployeeWithUnsupportedSortingOrder.response = Apis().get(url=url, data=params)

    @then("the search response status code for unsupported sorting order should be 400")
    def step_response_status_400(context):
        assert SearchEmployeeWithUnsupportedSortingOrder.response.status_code == 400

    @step("the search response for unsupported sorting order should contain validation error")
    def step_response_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error"
        }
        response_data = SearchEmployeeWithUnsupportedSortingOrder.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]

