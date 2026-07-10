from behave import given, when, then, step

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints



class DeleteManyEmployeeWithValidJwtTokenAndValidEmployeeIds:
    response = None
    url = None

    @given('I have the API endpoint "/employees/delete_many/"')
    def step_api_endpoint(context):
        context.url = Endpoints.employees_delete_many

    @given("Create 2 employees by calling employee create and note its employee code")
    def step_create_employee(context):
        url = Endpoints.employees_create  # This line should be indented
        params1 = {
            "name": "Jesus Jiminez",
            "mobile_number": "7777755555",
            "alternate_mobile_number": "2222255555",
            "dob": "2024-11-10",
            "shop_access": ["admin"],
            "email_id": "jesusjiminze@gmail.com",
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

        params2 = {
            "name": "Harry Kane",
            "mobile_number": "1111100000",
            "alternate_mobile_number": "1121100000",
            "dob": "2024-11-10",
            "shop_access": ["admin"],
            "email_id": "harrykane@gmail.com",
            "state": "California",
            "country": "USA",
            "street": "123 Main St",
            "profile_photo_url": "http://example.com/photo.jpg",
            "employee_code": "T_20",
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
        Apis().post(url=url, data=params2)

    @when("I send a PATCH request with valid JWT Token and valid employee IDs")
    def step_send_invalid_jwt_token(context):
        params = {
            "employee_code": ["T_19", "T_20"]
        }
        DeleteManyEmployeeWithValidJwtTokenAndValidEmployeeIds.response = Apis().patch(url=context.url,data=params)



    @then("the delete many response status code with valid JWT Token should be 200")
    def step_validate_status_code(context):
        assert DeleteManyEmployeeWithValidJwtTokenAndValidEmployeeIds.response.status_code == 200

    @step("the delete many response with valid JWT Token should contain")
    def step_deleted_sucessfully(context):
        response = {
            "status": True,
            "message": "Employees deleted successfully",
        }
        response_data = DeleteManyEmployeeWithValidJwtTokenAndValidEmployeeIds.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data


class DeleteManyEmployeeWithInvalidJwtToken:
    response = None
    url = None
    wrong_token = None


    @given('I have an invalid JWT token "invalid.jwt.token" to delete many employee')
    def step_validate_jwt_token(context):
        context.wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcnkiOiIyMDI1LTAxLTE1IDEyOjQ1OjA0Ljg0NjQ4MCswMDAwIiwidXNlcl9zcGVjaWZpY19kYXRhIjp7Im9yZ2FuaXNhdGlvbk5hbWUiOiJUZWNoYXNvIiwibmFtZSI6ImFkbWluIiwiZW1wbG95ZWVDb2RlIjoiVF8xIiwiZW1haWxJZCI6ImFkbWluQHRlY2hhc28ub3JnIiwicHJvZmlsZVBob3RvVXJsIjoiIiwic2hvcEFjY2Vzc0xpc3QiOltdLCJhcHByb3ZhbCI6ZmFsc2V9LCJwZXJtaXNzaW9ucyI6eyJtYXN0ZXIiOnsiaXRlbSI6dHJ1ZSwic2hvcCI6dHJ1ZSwic3VwcGxpZXIiOnRydWUsImN1c3RvbWVyIjp0cnVlLCJjcmVhdGUiOnRydWUsImVtcGxveWVlIjp0cnVlfSwiaW52ZW50b3J5Ijp7ImludmVudG9yeSI6dHJ1ZX0sImJpbGxpbmciOnsicG9zIjp0cnVlLCJyZXR1cm5faXRlbSI6dHJ1ZSwiYmlsbF9oaXN0b3J5Ijp0cnVlfSwicmVwb3J0cyI6eyJnZW5lcmFsIjp0cnVlLCJvdmVydmlldyI6dHJ1ZSwiYWRtaW5pc3RyYXRpb24iOnRydWUsImRheV9ib29rIjp0cnVlLCJnc3QiOnRydWV9LCJwcmludGVyX3RlbXBsYXRlcyI6eyJwcmludGVyX3RlbXBsYXRlcyI6dHJ1ZX0sImRhc2hib2FyZCI6eyJkYXNoYm9hcmQiOnRydWV9LCJzdG9jayI6eyJwdXJjaGFzZV9saXN0Ijp0cnVlLCJyZXR1cm5fcHVyY2hhc2UiOnRydWUsInN0b2NrIjp0cnVlfSwicXVvdGF0aW9ucyI6eyJxdW90YXRpb25zIjp0cnVlfX19.YoWHWwJRtMk-FIg1G41zYfNO6-NJBy0iAUE4-tKuMfY"

    @when("I send a PATCH request with invalid token with the following JSON body")
    def step_send_invalid_jwt_token(context):
        context.url = Endpoints.employees_delete_many
        headers = {"Authorization": f"Bearer {context.wrong_token}"}
        params = {
            "employee_code": "E_1",
        }
        DeleteManyEmployeeWithInvalidJwtToken.response = Apis().patch(url=context.url,data=params, headers=headers)

    @then("the delete many response status code with invalid token should be 401")
    def step_validate_status_code(context):
        assert DeleteManyEmployeeWithInvalidJwtToken.response.status_code == 401

    @step("the delete many response with invalid token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = DeleteManyEmployeeWithInvalidJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data


class DeleteManyEmployeeWithoutJwtToken:
    response = None

    @when("I send a PATCH request without an authorization token with the following JSON body")
    def step_send_without_jwt_token(context):
        url = Endpoints.employees_delete_many
        headers = {"Authorization": f"Bearer "}
        params = {
            "employee_code": ["E_1", "E_2"]
        }
        DeleteManyEmployeeWithoutJwtToken.response = Apis().patch(url=url, data=params, headers=headers)

    @then("the delete many response status code without an authorization token should be 401")
    def step_validate_status_code(context):
        assert DeleteManyEmployeeWithoutJwtToken.response.status_code == 401

    @step("the delete many response without an authorization token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = DeleteManyEmployeeWithoutJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data


class DeleteManyEmployeeWithValidJwtTokenAndMissingEmployeeId:
    response = None

    @given('I have a valid JWT token "valid.jwt.token" to delete many employees')
    def step_validate_token(context):
        url = Endpoints.employees_get_all
        response = Apis().get(url=url)
        assert response.status_code == 200

    @when("I send a PATCH request with missing employee IDs")
    def step_send_without_query_params(context):
        url = Endpoints.employees_delete_many
        params = {
        "employee_ids": []
        }
        DeleteManyEmployeeWithValidJwtTokenAndMissingEmployeeId.response = Apis().patch(url=url, data=params)

    @then("the delete many response status code with missing employee IDs should be 400")
    def step_validate_status_code(context):
        assert DeleteManyEmployeeWithValidJwtTokenAndMissingEmployeeId.response.status_code == 400

    @step("the delete many response response with missing employee IDs should contain")
    def step_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error",
        }
        response_data = DeleteManyEmployeeWithValidJwtTokenAndMissingEmployeeId.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]


class DeleteManyEmployeeWithValidJwtTokenAndInvalidEmployeeId:
    response = None

    @when("I send a PATCH request with invalid employee ID")
    def step_send_without_query_params(context):
        url = Endpoints.employees_delete_many
        params = {
            "employee_code":["T_11","T_7"]
        }
        DeleteManyEmployeeWithValidJwtTokenAndInvalidEmployeeId.response = Apis().patch(url=url, data=params)

    @then("the delete many response status code with invalid employee ID should be 400")
    def step_validate_status_code(context):
        assert DeleteManyEmployeeWithValidJwtTokenAndInvalidEmployeeId.response.status_code == 400

    @step("the delete many response with invalid employee ID should contain")
    def step_validation_error(context):
        response = {
            "status": False,
            "message": "Value Error No matching employee found",
            "error": ['No matching employee found']
        }
        response_data = DeleteManyEmployeeWithValidJwtTokenAndInvalidEmployeeId.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]
        assert response_data.get("error") == response["error"]

class DeleteManyEmployeeWithValidJwtTokenAndNoEmployeeId:
    response = None

    @when("I send a PATCH request without any JSON body")
    def step_send_without_query_params(context):
        url = Endpoints.employees_delete_many
        params = {
        }
        DeleteManyEmployeeWithValidJwtTokenAndNoEmployeeId.response = Apis().patch(url=url, data=params)

    @then("the delete many response status code with no employee IDs should be 400")
    def step_validate_status_code(context):
        print(DeleteManyEmployeeWithValidJwtTokenAndNoEmployeeId.response.json())
        assert DeleteManyEmployeeWithValidJwtTokenAndNoEmployeeId.response.status_code == 400

    @step("the delete many response with no employee IDs should contain")
    def step_validation_error(context):
        response = {
            "status": False,
            "message": "Validation Error",
            "error": [{'employee_code': ['This field is required.']}]
        }
        response_data = DeleteManyEmployeeWithValidJwtTokenAndNoEmployeeId.response.json()
        assert response_data.get("status") == response["status"]
        assert response_data.get("message") == response["message"]
        assert response_data.get("error") == response["error"]