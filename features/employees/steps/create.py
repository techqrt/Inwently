from behave import given, when, then, step

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints


class CreateEmployeeWithValidJwtTokenAndValidData:
    response = None
    url = None

    @given('I have the API endpoint "/employees/create/"')
    def step_api_endpoint(context):
        context.url = Endpoints.employees_create

    @given('I have a valid JWT token "valid.jwt.token" to create employee')
    def step_validate_jwt_token(context):
        response = Apis().get(url=Endpoints.employees_get_all)
        assert response.status_code == 200

    @when("I send a POST request to create employee with the following JSON body")
    def step_send_create_employee(context):
        params = {
        "name": "Alan Roy",
        "mobile_number": "9435060890",
        "alternate_mobile_number":"7435371001",
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Alanr.roy@example.com",
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
        CreateEmployeeWithValidJwtTokenAndValidData.response = Apis().post(url=context.url, data=params)

    @then("the response status code to create employee should be 201")
    def step_validate_status_code(context):
        print(CreateEmployeeWithValidJwtTokenAndValidData.response.status_code)
        assert CreateEmployeeWithValidJwtTokenAndValidData.response.status_code == 201

    @step("the response to create employee should contain")
    def step_response_create_employee(context):
        response = {
            "status": True,
            "message": "Employee created successfully",
        }
        response_data = CreateEmployeeWithValidJwtTokenAndValidData.response.json()
        assert response_data["status"] == response["status"]
        assert response_data["message"] == response["message"]

class CreateEmployeeWithValidJwtTokenAndMissingRequiredField:
    response = None

    @when("I send a POST request to create employee with missing required fields")
    def step_send_create_employee(context):
        url = Endpoints.employees_create
        params = {}
        CreateEmployeeWithValidJwtTokenAndMissingRequiredField.response = Apis().post(url=url, data=params)
    @then("the create response status code with missing required fields should be 400")
    def step_validate_status_code(context):
        assert CreateEmployeeWithValidJwtTokenAndMissingRequiredField.response.status_code == 400

    @step("the create response with missing required fields should contain")
    def step_response_create_employee(context):
        response = {
            "status": False,
            "message": "Validation Error",
        }
        response_data = CreateEmployeeWithValidJwtTokenAndValidData.response.json()
        assert response_data["status"] == response["status"]
        assert response_data["message"] == response["message"]

class CreateEmployeeWithInvalidMobileNumber:
    response = None

    @when("I send a POST request to create employee with invalid mobile number")
    def step_send_create_employee(context):
        url = Endpoints.employees_create
        params = {
        "name": "Alan Roy",
        "mobile_number": "1apo0osdsda",
        "alternate_mobile_number":"7435371001",
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Alanr.roy@example.com",
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
        CreateEmployeeWithInvalidMobileNumber.response = Apis().post(url=url, data=params)

    @then("the create response status code with invalid phone number should be 400")
    def step_validate_status_code(context):
        assert CreateEmployeeWithInvalidMobileNumber.response.status_code == 400

    @step("the create response with invalid phone number should contain")
    def step_response_create_employee(context):
        response = {
            "status": False,
            "message": "Validation Error",
        }
        response_data = CreateEmployeeWithValidJwtTokenAndValidData.response.json()
        assert response_data["status"] == response["status"]
        assert response_data["message"] == response["message"]

class CreateEmployeeWithoutJwtToken:
    response = None

    @when("I send a POST request to create employee without an authorization token with the following JSON body")
    def step_api_call_wrong_token(context):
        url = Endpoints.employees_create
        headers = {"Authorization": f"Bearer "}
        params = {
        "name": "Alan Roy",
        "mobile_number": "9435060890",
        "alternate_mobile_number":"7435371001",
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Alanr.roy@example.com",
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
        CreateEmployeeWithoutJwtToken.response = Apis().post(url=url,data=params, headers=headers)

    @then("the create response status code without an authorization token should be 401")
    def step_response_status_and_type(context):
        assert CreateEmployeeWithoutJwtToken.response.status_code == 401

    @step("the create response without an authorization token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = CreateEmployeeWithoutJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data

class CreateEmployeeWithInvalidJwtToken:
    response = None
    wrong_token = None

    @given('I have an invalid JWT token "invalid.jwt.token" to create employee')
    def step_create_wrong_jwt_token(context):
        context.wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcnkiOiIyMDI1LTAxLTE1IDEyOjQ1OjA0Ljg0NjQ4MCswMDAwIiwidXNlcl9zcGVjaWZpY19kYXRhIjp7Im9yZ2FuaXNhdGlvbk5hbWUiOiJUZWNoYXNvIiwibmFtZSI6ImFkbWluIiwiZW1wbG95ZWVDb2RlIjoiVF8xIiwiZW1haWxJZCI6ImFkbWluQHRlY2hhc28ub3JnIiwicHJvZmlsZVBob3RvVXJsIjoiIiwic2hvcEFjY2Vzc0xpc3QiOltdLCJhcHByb3ZhbCI6ZmFsc2V9LCJwZXJtaXNzaW9ucyI6eyJtYXN0ZXIiOnsiaXRlbSI6dHJ1ZSwic2hvcCI6dHJ1ZSwic3VwcGxpZXIiOnRydWUsImN1c3RvbWVyIjp0cnVlLCJjcmVhdGUiOnRydWUsImVtcGxveWVlIjp0cnVlfSwiaW52ZW50b3J5Ijp7ImludmVudG9yeSI6dHJ1ZX0sImJpbGxpbmciOnsicG9zIjp0cnVlLCJyZXR1cm5faXRlbSI6dHJ1ZSwiYmlsbF9oaXN0b3J5Ijp0cnVlfSwicmVwb3J0cyI6eyJnZW5lcmFsIjp0cnVlLCJvdmVydmlldyI6dHJ1ZSwiYWRtaW5pc3RyYXRpb24iOnRydWUsImRheV9ib29rIjp0cnVlLCJnc3QiOnRydWV9LCJwcmludGVyX3RlbXBsYXRlcyI6eyJwcmludGVyX3RlbXBsYXRlcyI6dHJ1ZX0sImRhc2hib2FyZCI6eyJkYXNoYm9hcmQiOnRydWV9LCJzdG9jayI6eyJwdXJjaGFzZV9saXN0Ijp0cnVlLCJyZXR1cm5fcHVyY2hhc2UiOnRydWUsInN0b2NrIjp0cnVlfSwicXVvdGF0aW9ucyI6eyJxdW90YXRpb25zIjp0cnVlfX19.YoWHWwJRtMk-FIg1G41zYfNO6-NJBy0iAUE4-tKuMfY"

    @when("I send a POST request to create employee with invalid token with the following JSON body")
    def step_api_call_wrong_token(context):
        url = Endpoints.employees_create
        headers = {"Authorization": f"Bearer {context.wrong_token}"}
        params = {
        "name": "Alan Roy",
        "mobile_number": "9435060890",
        "alternate_mobile_number":"7435371001",
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Alanr.roy@example.com",
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
        CreateEmployeeWithInvalidJwtToken.response = Apis().post(url=url, data=params, headers=headers)

    @then("the create response status code with invalid token should be 401")
    def step_response_status_and_type(context):
        assert CreateEmployeeWithInvalidJwtToken.response.status_code == 401

    @step("the create response with invalid token should contain")
    def step_authentication_error(context):
        response = {
            "status": False,
            "message": "error",
        }
        response_data = CreateEmployeeWithInvalidJwtToken.response.json()
        assert response_data.get("status") == response["status"]
        assert response["message"] in response_data


class CreateEmployeeWithValidJwtTokenAndInvalidEmailFormat:
    response = None
    url = None

    @when("I send a POST request to create employee with invalid email id with the following JSON body")
    def step_send_put_request(context):
        url = Endpoints.employees_create
        params = {
        "name": "Alan Roy",
        "mobile_number": "9435060890",
        "alternate_mobile_number":"7435371001",
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Alanr.roy///.com",
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
        CreateEmployeeWithValidJwtTokenAndInvalidEmailFormat.response = Apis().post(url=url, data=params)

        @then(u"the create response status code with invalid email id should be 400")
        def step_response_status_400(context):
            assert CreateEmployeeWithValidJwtTokenAndInvalidEmailFormat.response.status_code == 400

        @step(u"the create response with invalid email should contain")
        def step_response_should_contain_employee_updated(context):
            response = {
                "status": False,
                "message": "Validation Error",
            }
            response_data = CreateEmployeeWithValidJwtTokenAndInvalidEmailFormat.response.json()
            assert response_data["status"] == response["status"]
            assert response_data["message"] == response["message"]


class CreateEmployeeWithValidJwtTokenAndWithoutPermissions:
    response = None

    @when("I send a POST request to create employee without permissions with the following JSON body")
    def step_send_put_request(context):
        url = Endpoints.employees_create
        params = {
        "name": "Alan Roy",
        "mobile_number": "9435060890",
        "alternate_mobile_number":"7435371001",
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Alanr.roy@example.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        }
        CreateEmployeeWithValidJwtTokenAndWithoutPermissions.response = Apis().post(url=url, data=params)

        @then("the create response status code without permissions should be 400")
        def step_response_status_400(context):
            assert CreateEmployeeWithValidJwtTokenAndWithoutPermissions.response.status_code == 400

        @step("the create response without permissions should contain")
        def step_response_should_contain_employee_updated(context):
            response = {
                "status": False,
                "message": "Validation Error",
            }
            response_data = CreateEmployeeWithValidJwtTokenAndWithoutPermissions.response.json()
            assert response_data["status"] == response["status"]
            assert response_data["message"] == response["message"]