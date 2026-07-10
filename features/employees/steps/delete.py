from behave import given, when, then, step

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


class DeleteEmployeeWithValidJwtTokenAndValidEmployeeId:
    response = None
    url = None

    @given('I have a valid JWT token "valid.jwt.token" to delete employee')
    def step_valid_jwt_token(context):
        context.url = Endpoints.employees_get_all
        response = Apis().get(url=context.url)
        assert response.status_code == 200

    @given('Create an employee by calling employee create api')
    def step_create_employee(context):
        url = Endpoints.employees_create  # This line should be indented
        params1 = {
            "name": "Peepe Boss",
            "mobile_number": "9090123414",
            "alternate_mobile_number": "9435367241",
            "dob": "2024-11-10",
            "shop_access": ["admin"],
            "email_id": "peeepeboss@gmail.com",
            "state": "California",
            "country": "USA",
            "street": "123 Main St",
            "profile_photo_url": "http://example.com/photo.jpg",
            "employee_code": "T_19",
            "permissions": {
                "master": {
                    "item": True,
                    "shop": True,
                    "supplier": True,
                    "customer": True,
                    "create": True,
                    "employee": True
                },
                "inventory": {
                    "inventory": True
                },
                "billing": {
                    "bill_history": True,
                    "pos": True,
                    "return_item": True
                },
                "reports": {
                    "overview": True,
                    "general": True,
                    "administration": True,
                    "day_book": True,
                    "gst": True
                },
                "printer_templates": {
                    "printer_templates": True
                },
                "dashboard": {
                    "dashboard": True
                },
                "stock": {
                    "stock": True,
                    "purchase_list": True,
                    "return_purchase": True
                },
                "quotations": {
                    "quotations": True
                }
            }
        }
        Apis().post(url=url, data=params1)

    @when("I send a DELETE request with valid Jwt Token with query parameters")
    def step_send_invalid_jwt_token(context):
        params = {
            "employee_code": "T_4",
        }
        DeleteEmployeeWithValidJwtTokenAndValidEmployeeId.response = Apis().delete(url=context.url,data=params)

    @then("the delete response status code with valid Jwt Token should be 200")
    def step_validate_status_code(context):
        assert DeleteEmployeeWithValidJwtTokenAndValidEmployeeId.response.status_code == 200

    @step("the delete response with valid Jwt Token should contain")
    def step_deleted_sucessfully(context):
        response = {
            "status": True,
            "message": "Employee deleted successfully",
        }
        response_data = DeleteEmployeeWithValidJwtTokenAndValidEmployeeId.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data

class DeleteEmployeeWithInvalidJwtToken:
    response = None
    url = None
    wrong_token = None

    @given('I have the API endpoint "/employees/delete/"')
    def step_api_endpoint(context):
        DeleteEmployeeWithInvalidJwtToken.url = Endpoints.employee_delete

    @given('I have an invalid JWT token "invalid.jwt.token" to delete employee')
    def step_validate_jwt_token(context):
        context.wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcnkiOiIyMDI1LTAxLTE1IDEyOjQ1OjA0Ljg0NjQ4MCswMDAwIiwidXNlcl9zcGVjaWZpY19kYXRhIjp7Im9yZ2FuaXNhdGlvbk5hbWUiOiJUZWNoYXNvIiwibmFtZSI6ImFkbWluIiwiZW1wbG95ZWVDb2RlIjoiVF8xIiwiZW1haWxJZCI6ImFkbWluQHRlY2hhc28ub3JnIiwicHJvZmlsZVBob3RvVXJsIjoiIiwic2hvcEFjY2Vzc0xpc3QiOltdLCJhcHByb3ZhbCI6ZmFsc2V9LCJwZXJtaXNzaW9ucyI6eyJtYXN0ZXIiOnsiaXRlbSI6dHJ1ZSwic2hvcCI6dHJ1ZSwic3VwcGxpZXIiOnRydWUsImN1c3RvbWVyIjp0cnVlLCJjcmVhdGUiOnRydWUsImVtcGxveWVlIjp0cnVlfSwiaW52ZW50b3J5Ijp7ImludmVudG9yeSI6dHJ1ZX0sImJpbGxpbmciOnsicG9zIjp0cnVlLCJyZXR1cm5faXRlbSI6dHJ1ZSwiYmlsbF9oaXN0b3J5Ijp0cnVlfSwicmVwb3J0cyI6eyJnZW5lcmFsIjp0cnVlLCJvdmVydmlldyI6dHJ1ZSwiYWRtaW5pc3RyYXRpb24iOnRydWUsImRheV9ib29rIjp0cnVlLCJnc3QiOnRydWV9LCJwcmludGVyX3RlbXBsYXRlcyI6eyJwcmludGVyX3RlbXBsYXRlcyI6dHJ1ZX0sImRhc2hib2FyZCI6eyJkYXNoYm9hcmQiOnRydWV9LCJzdG9jayI6eyJwdXJjaGFzZV9saXN0Ijp0cnVlLCJyZXR1cm5fcHVyY2hhc2UiOnRydWUsInN0b2NrIjp0cnVlfSwicXVvdGF0aW9ucyI6eyJxdW90YXRpb25zIjp0cnVlfX19.YoWHWwJRtMk-FIg1G41zYfNO6-NJBy0iAUE4-tKuMfY"

    @when("I send a DELETE request with invalid Jwt Token with query parameters")
    def step_send_invalid_jwt_token(context):
        headers = {"Authorization": f"Bearer {context.wrong_token}"}
        params = {
            "employee_code" : "T_3",
        }
        DeleteEmployeeWithInvalidJwtToken.response = Apis().delete(url=DeleteEmployeeWithInvalidJwtToken.url, data=params, headers=headers)

    @then("the delete response status code with invalid Jwt token should be 401")
    def step_validate_status_code(context):
        assert DeleteEmployeeWithInvalidJwtToken.response.status_code == 401

    @step("the delete response with invalid Jwt Token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = DeleteEmployeeWithInvalidJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data

class DeleteEmployeeWithoutJwtToken:
    response = None

    @when("I send a DELETE request without an authorization token with query parameters")
    def step_send_without_jwt_token(context):
        url = Endpoints.employee_delete
        headers = {"Authorization": f"Bearer "}
        params = {
            "employee_code" : "E_1",
        }
        DeleteEmployeeWithoutJwtToken.response = Apis().delete(url=url, data=params, headers=headers)

    @then("the delete response status code without authorization Token should be 401")
    def step_validate_status_code(context):
        assert DeleteEmployeeWithoutJwtToken.response.status_code == 401

    @step("the delete response without authorization Token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = DeleteEmployeeWithoutJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data

class DeleteEmployeeWithValidJwtTokenAndMissingEmployeeId:
    response = None

    @when("I send a DELETE request without query parameters")
    def step_send_without_query_params(context):
        url = Endpoints.employee_delete
        params = {

        }
        DeleteEmployeeWithValidJwtTokenAndMissingEmployeeId.response = Apis().delete(url=url, data=params)

    @then("the delete response status code without query parameters should be 400")
    def step_validate_status_code(context):
        assert DeleteEmployeeWithValidJwtTokenAndMissingEmployeeId.response.status_code == 400

    @step("the delete response without query parameters should contain")
    def step_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error",
            "error" : [{'employee_code': ['This field is required.']}],
        }
        response_data = DeleteEmployeeWithValidJwtTokenAndMissingEmployeeId.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]
        assert response_data.get("error") == response["error"]


class DeleteEmployeeWithValidJwtTokenAndInvalidEmployeeId:
    response = None

    @when("I send a DELETE request with invalid employee id")
    def step_send_without_query_params(context):
        url = Endpoints.employee_delete
        params = {
            "employee_code": "Ea11",
        }
        DeleteEmployeeWithValidJwtTokenAndInvalidEmployeeId.response = Apis().delete(url=url, data=params)

    @then("the delete response status code with invalid employee id should be 400")
    def step_validate_status_code(context):
        assert DeleteEmployeeWithValidJwtTokenAndInvalidEmployeeId.response.status_code == 400

    @step("the delete response with invalid employee id should contain")
    def step_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error",
        }
        response_data = DeleteEmployeeWithValidJwtTokenAndInvalidEmployeeId.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]