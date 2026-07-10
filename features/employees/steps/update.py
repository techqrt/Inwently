
from behave import given, when, then, step

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


class UpdateEmployeeWithValidJwtTokenAndValidData:
    response  = None
    url = None

    @given('I have the API endpoint "/employees/update/"')
    def step_api_end_point(context):
        context.url = Endpoints.employees_update

    @given('I have a valid JWT token "valid\.jwt\.token" to update employees')
    def step_valid_jwt_token(context):
        response = Apis().get(url=Endpoints.employees_get_all)
        assert response.status_code == 200

    @when("I send a PUT request with the following JSON body")
    def step_send_put_request(context):
        params = {
        "name": "Amxson Sminage",
        "mobile_number": 9435071907,
        "alternate_mobile_number":7901253210,
        "dob": "2024-11-10",
        "shop_access":["admin"],
        "email_id": "Amxsoan@gmail.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        "employee_code": "T_7",
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
        UpdateEmployeeWithValidJwtTokenAndValidData.response = Apis().put(url=context.url, data=params)

    @then("the update response status code for valid data should be 200")
    def step_response_status_200(context):
        print(UpdateEmployeeWithValidJwtTokenAndValidData.response.json())
        assert UpdateEmployeeWithValidJwtTokenAndValidData.response.status_code == 200

    @step("the update response should contain employee updated successfully")
    def step_response_should_contain_employee_updated(context):
        response = {
            "status": True,
            "message": "Employee updated successfully",
        }
        response_data = UpdateEmployeeWithValidJwtTokenAndValidData.response.json()
        assert response_data["status"] == response["status"]
        assert response_data["message"] == response["message"]

class UpdateEmployeeWithValidJwtTokenAndMissingEmployeeId:
    response = None

    @when("I send a PUT request with the following JSON body with employee_code missing")
    def step_send_put_request(context):
        url = Endpoints.employees_update
        params = {
        "name": "Amxson Sminage",
        "mobile_number": 943,
        "alternate_mobile_number":7901253200,
        "dob": "2024-11-10",
        "shop_access": ["admin"],
        "email_id": "Amxson@gmail.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
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
        UpdateEmployeeWithValidJwtTokenAndMissingEmployeeId.response = Apis().put(url=url, data=params)

    @then("the update response status code for missing employee_code should be 400")
    def step_response_status_400(context):
        assert UpdateEmployeeWithValidJwtTokenAndMissingEmployeeId.response.status_code == 400

    @step("the update response for missing employee_code should contain Validation error")
    def step_response_should_contain_employee_updated(context):
        response = {
            "status": False,
            "message": "Validation Error",
        }
        response_data = UpdateEmployeeWithValidJwtTokenAndMissingEmployeeId.response.json()
        assert response_data["status"] == response["status"]
        assert response_data["message"] == response["message"]


class UpdateEmployeeWithValidJwtTokenAndInvalidEmailFormat:
    response = None
    url = None

    @when("I send a PUT request with the following JSON body with invalid email ID format")
    def step_send_put_request(context):
        url = Endpoints.employees_update
        params = {
        "name": "Amxson Sminage",
        "mobile_number": 9435071987,
        "alternate_mobile_number":7901253200,
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Amxson//gmail.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        "employee_code": "T_11",
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
        UpdateEmployeeWithValidJwtTokenAndInvalidEmailFormat.response = Apis().put(url=url, data=params)

    @then("the update response status code for invalid email ID format should be 400")
    def step_response_status_400(context):
        assert UpdateEmployeeWithValidJwtTokenAndInvalidEmailFormat.response.status_code == 400

    @step("the update response for invalid email ID format should contain")
    def step_response_should_contain_employee_updated(context):
        response = {
            "status": False,
            "message": "Validation Error",
        }
        response_data = UpdateEmployeeWithValidJwtTokenAndInvalidEmailFormat.response.json()
        assert response_data["status"] == response["status"]
        assert response_data["message"] == response["message"]




class UpdateEmployeeWithoutJwtToken:
    response = None

    @when("I send a PUT request with the following JSON body with valid data but without Jwt Token")
    def step_api_call_wrong_token(context):
        url = Endpoints.employees_update
        headers = {"Authorization": f"Bearer "}
        params = {
        "name": "Amxson Sminage",
        "mobile_number": 9435071987,
        "alternate_mobile_number":7901253200,
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Amxson@gmail.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        "employee_code": "T_11",
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
        UpdateEmployeeWithoutJwtToken.response = Apis().put(url=url,data=params, headers=headers)

    @then("the update response status code without jwt token should be 401")
    def step_response_status_and_type(context):
        assert UpdateEmployeeWithoutJwtToken.response.status_code == 401

    @step("the update response without jwt token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = UpdateEmployeeWithoutJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data

class UpdateEmployeeWithInvalidJwtToken:
    response = None
    wrong_token = None

    @given('I have an invalid JWT token "invalid.jwt.token"')
    def step_create_wrong_jwt_token(context):
        context.wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcnkiOiIyMDI1LTAxLTE1IDEyOjQ1OjA0Ljg0NjQ4MCswMDAwIiwidXNlcl9zcGVjaWZpY19kYXRhIjp7Im9yZ2FuaXNhdGlvbk5hbWUiOiJUZWNoYXNvIiwibmFtZSI6ImFkbWluIiwiZW1wbG95ZWVDb2RlIjoiVF8xIiwiZW1haWxJZCI6ImFkbWluQHRlY2hhc28ub3JnIiwicHJvZmlsZVBob3RvVXJsIjoiIiwic2hvcEFjY2Vzc0xpc3QiOltdLCJhcHByb3ZhbCI6ZmFsc2V9LCJwZXJtaXNzaW9ucyI6eyJtYXN0ZXIiOnsiaXRlbSI6dHJ1ZSwic2hvcCI6dHJ1ZSwic3VwcGxpZXIiOnRydWUsImN1c3RvbWVyIjp0cnVlLCJjcmVhdGUiOnRydWUsImVtcGxveWVlIjp0cnVlfSwiaW52ZW50b3J5Ijp7ImludmVudG9yeSI6dHJ1ZX0sImJpbGxpbmciOnsicG9zIjp0cnVlLCJyZXR1cm5faXRlbSI6dHJ1ZSwiYmlsbF9oaXN0b3J5Ijp0cnVlfSwicmVwb3J0cyI6eyJnZW5lcmFsIjp0cnVlLCJvdmVydmlldyI6dHJ1ZSwiYWRtaW5pc3RyYXRpb24iOnRydWUsImRheV9ib29rIjp0cnVlLCJnc3QiOnRydWV9LCJwcmludGVyX3RlbXBsYXRlcyI6eyJwcmludGVyX3RlbXBsYXRlcyI6dHJ1ZX0sImRhc2hib2FyZCI6eyJkYXNoYm9hcmQiOnRydWV9LCJzdG9jayI6eyJwdXJjaGFzZV9saXN0Ijp0cnVlLCJyZXR1cm5fcHVyY2hhc2UiOnRydWUsInN0b2NrIjp0cnVlfSwicXVvdGF0aW9ucyI6eyJxdW90YXRpb25zIjp0cnVlfX19.YoWHWwJRtMk-FIg1G41zYfNO6-NJBy0iAUE4-tKuMfY"

    @when("I send a PUT request with the following JSON body with valid data but invalid token")
    def step_api_call_wrong_token(context):
        url = Endpoints.employees_update
        headers = {"Authorization": f"Bearer {context.wrong_token}"}
        params = {
        "name": "Amxson Sminage",
        "mobile_number": 9435071987,
        "alternate_mobile_number":7901253200,
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Amxson@gmail.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        "employee_code": "T_11",
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
        UpdateEmployeeWithInvalidJwtToken.response = Apis().post(url=url, data=params, headers=headers)

    @then("the update response status code for invalid JWT Token should be 401")
    def step_response_status_and_type(context):
        assert UpdateEmployeeWithInvalidJwtToken.response.status_code == 401

    @step("the update response for invalid JWT Token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = UpdateEmployeeWithInvalidJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data