
from behave import given, when, then, step

from features.steps.common.apis import Apis
from features.steps.common.endpoints import Endpoints



class GetEmployeeWithSpecificFields:
    response = None
    url = None
    value = None
    response_data = None

    @given('I have the API endpoint "/employees/get/"')
    def step_api_endpoint(context):
        context.url = Endpoints.employees_get

    @given('I have the employee code "employee_code"')
    def step_employee_code(context):
        context.employee_code = "T_7"

    @given('I specify the expected response fields as "value"')
    def step_value(context):
        context.value = {
        "name": "Amxson Sminage",
        "mobileNumber": "9435071907",
        "alternate_mobile_number": "7901253210",
        "dob": "2024-11-10",
        "state": "California",
        "country": "USA",
        "organisationName": "Techaso",
        "shopAccess": [
            {
                "name": "admin",
                "shopCode": "T_1"
            }
        ],
        "street": "123 Main St",
        "isActive": False,
        "emailId": "James.paul@example.com",
        "emailVerified": False,
        "employeeCode": "T_7",
        "profilePhotoUrl": "http://example.com/photo.jpg",
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
                "billHistory": True,
                "pos": True,
                "returnItem": True
            },
            "reports": {
                "overview": True,
                "general": True,
                "administration": True,
                "dayBook": True,
                "gst": True
            },
            "dashboard": {
                "dashboard": True
            },
            "stock": {
                "stock": True,
                "purchaseList": True,
                "returnPurchase": True
            },
            "quotations": {
                "quotations": True
            },
            "printerTemplates": {
                "printerTemplates": True
            }
        }
    }

    @when("I send a GET request to retrieve employees with specified fields to the endpoint")
    def step_api_get_request(context):
        params = {
            "employee_code" : context.employee_code
        }
        GetEmployeeWithSpecificFields.response = Apis().get(url=context.url,data=params)

    @then("the get response with specified field status should be 200")
    def step_validate_response_status(context):
        assert GetEmployeeWithSpecificFields.response.status_code == 200

    @step('the get response with specified field should contain the field "status" with the value true')
    def step_validate_response(context):
        print(GetEmployeeWithSpecificFields.response)
        context.response_data = GetEmployeeWithSpecificFields.response.json()
        assert context.response_data.get("status") == True

    @step('the get response with specified field should contain the field "message" with a string')
    def step_validate_reponse(context):
        assert context.response_data.get("message") == "Data fetched successfully"

    @step('the get response with specified field should contain the "data" object with specified fields')
    def  step_validate_reponse(context):
        assert context.response_data.get("data") == context.value

    @step('the get response with specified field "data" object should contain the "permissions" structure with appropriate permissions')
    def step_validate_reponse(context):
        required_permissions_keys = [
            'master', 'inventory', 'billing', 'reports', 'printerTemplates',
            'dashboard', 'stock', 'quotations'
        ]

        for key in required_permissions_keys:
            assert key in context.response_data['data']['permissions'], f"Missing key in 'permissions': {key}"


class GetEmployeesWithAllAvailableFields:
    response = None
    url = None
    response_data = None

    @given('I have the employee code "xxxx"')
    def step_employee_code(context):
        context.employee_code = "T_7"

    @given('I specify the expected response fields as empty so all fields should be returned')
    def step_expected_response(context):
        expected_response = {}

    @when('I send a GET request to the endpoint')
    def step_api_get_request(context):
        params = {
            "employee_code": context.employee_code
        }
        GetEmployeesWithAllAvailableFields.response = Apis().get(url=context.url, data=params)

    @then("the get response with all available fields status code should be 200")
    def step_validate_response_status(context):
        assert GetEmployeesWithAllAvailableFields.response.status_code == 200

    @step('the get response with all available fields should contain the field "status" with the value true')
    def step_validate_response(context):
        context.response_data = GetEmployeesWithAllAvailableFields.response.json()
        assert context.response_data.get("status") == True

    @step('the get response with all available fields should contain the field "message" with a string')
    def step_validate_reponse(context):
        assert context.response_data.get("message") == "Data fetched successfully"

    @step('the get response with all available fields should contain all fields in the "data" object including')
    def step_validate_reponse(context):
        required_data_keys = [
            'name', 'mobileNumber', 'dob', 'state', 'country', 'street',
            'organisationName', 'isActive', 'emailId', 'emailVerified',
            'profilePhotoUrl', 'employeeCode'
        ]

        for key in required_data_keys:
            assert key in context.response_data['data'], f"Missing key in 'data': {key}"


    @step('the get response with all available fields "permissions" structure should include')
    def step_validate_response(context):
        required_permissions_keys = [
            'master', 'inventory', 'billing', 'reports', 'printerTemplates',
            'dashboard', 'stock', 'quotations'
        ]

        for key in required_permissions_keys:
            assert key in context.response_data['data']['permissions'], f"Missing key in 'permissions': {key}"


class GetEmployeesWithoutNonExistingEmployeeCode:
    response = None
    expected_response = None

    @given('I use a non-existing employee code "E0000"')
    def step_set_employee_code(context):
        context.params = {
            "employee_code": "E0000"
        }
    @given("I specify no expected response fields")
    def step_response_field(context):
        context.expected_response = None

    @when("I send a GET request to the endpoint with non-existing employee code")
    def step_send_request(context):
        url = Endpoints.employees_get
        GetEmployeesWithoutNonExistingEmployeeCode.response = Apis().get(url=url, data=context.params)

    @then("the get response status with non-existing employee code should be 400")
    def step_validate_response_status(context):
        assert GetEmployeesWithoutNonExistingEmployeeCode.response.status_code == 400

    @step('the get response with non-existing employee code should contain the field "status" with the value false')
    def step_validate_response(context):
        response_data = GetEmployeesWithoutNonExistingEmployeeCode.response.json()
        assert response_data.get("status") == False

    @step('the get response with non-existing employee code should contain the field "message" with the value "Value Error No matching employee found"')
    def step_validate_response(context):
        response_data = GetEmployeesWithoutNonExistingEmployeeCode.response.json()
        assert response_data.get("message") == "Value Error No matching employee found"

    @step('the get response with non-existing employee code should contain an "error" field with the message')
    def step_validate_response(context):
        response = {
            "No matching employee found"
        }
        response_data = GetEmployeesWithoutNonExistingEmployeeCode.response.json()
        assert response_data.get("error") == response

class GetEmployeesWithoutEmployeeCode:
    response = None
    params = None

    @given("I do not provide an employee code")
    def step_set_employee_code(context):
        context.params = {
        }
    @when("I send a GET request to the endpoint without employee code")
    def step_send_request(context):
        url = Endpoints.employees_get
        GetEmployeesWithoutEmployeeCode.response = Apis().get(url=url, data=context.params)

    @then("the get response without employee code status should be 400")
    def step_validate_response_status(context):
        assert GetEmployeesWithoutEmployeeCode.response.status_code == 400

    @step('the get response without employee code should contain the field "status" with the value false')
    def step_validate_response(context):
        response_data = GetEmployeesWithoutEmployeeCode.response.json()
        assert response_data.get("status") == False

    @step('the get response without employee code should contain the field "message" with the value "Validation Error"')
    def step_validate_response(context):
        response_data = GetEmployeesWithoutEmployeeCode.response.json()
        assert response_data.get("message") == "Validation Error"

    @step('the get response without employee code should contain an "error" field with the following structure')
    def step_validate_response(context):
        response = [{
            "employee_code": ["This field is required."]
        }]
        response_data = GetEmployeesWithoutEmployeeCode.response.json()
        assert response_data.get("error") == response


class GetEmployeesWithInvalidEmployeeCode:
    response = None
    response_data = None

    @given('I use an invalid employee code "!@#123"')
    def step_set_employee_code(context):
        context.employee_code = "!@123"

    @when('I send a GET request to the endpoint with invalid employee code format')
    def step_send_get_request(context):
        params = {
            "employee_code": context.employee_code,
        }
        url = Endpoints.employees_get
        GetEmployeesWithInvalidEmployeeCode.response = Apis().get(url=url, data=params)

    @then("the get response with invalid employee code status should be 400")
    def step_validate_response_status(context):
        assert GetEmployeesWithInvalidEmployeeCode.response.status_code == 400

    @step('the get response with invalid employee code should contain the field "status" with the value false')
    def step_validate_response(context):
        context.response_data = GetEmployeesWithInvalidEmployeeCode.response.json()
        assert context.response_data.get("status") == False

    @step('the get response with invalid employee code should contain the field "message" with the value "Validation Error"')
    def step_validate_response(context):
        assert context.response_data.get("message") == "Validation Error"

    @step('the get response with invalid employee code should contain an "error" field with the following structure')
    def step_validate_response(context):
        assert context.response_data.get("error") == "No matching employee found"

class GetEmployeesWithEmptyEmployeeCode:
    response = None
    params = None

    @given("I set the employee code as an empty string")
    def step_set_employee_code(context):
        context.params = {
            "employee_code": ""
        }

    @when("I send a GET request to the endpoint with empty employee code")
    def step_send_request(context):
        url = Endpoints.employees_get
        GetEmployeesWithEmptyEmployeeCode.response = Apis().get(url=url, data=context.params)

    @then("the response status with empty employee code should be 400")
    def step_validate_response_status(context):
        assert GetEmployeesWithEmptyEmployeeCode.response.status_code == 400

    @step('the get response with empty employee code should contain the field "status" with the value false')
    def step_validate_response(context):
        response_data = GetEmployeesWithEmptyEmployeeCode.response.json()
        assert response_data.get("status") == False

    @step('the get response with empty employee code should contain the field "message" with the value "Validation Error"')
    def step_validate_response(context):
        response_data = GetEmployeesWithEmptyEmployeeCode.response.json()
        assert response_data.get("message") == "Validation Error"

    @step('the get response with empty employee code should contain an "error" field with the following structure')
    def step_validate_response(context):
        response = [{
            "employee_code": ["This field may not be blank."]
        }]
        response_data = GetEmployeesWithEmptyEmployeeCode.response.json()
        assert response_data.get("error") == response


class GetEmployeesWithWrongJwtToken:
    response = None
    wrong_token = None

    @given("create jwt token manualy for employees get api")
    def step_create_wrong_jwt_token(context):
        context.wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcnkiOiIyMDI1LTAxLTE1IDEyOjQ1OjA0Ljg0NjQ4MCswMDAwIiwidXNlcl9zcGVjaWZpY19kYXRhIjp7Im9yZ2FuaXNhdGlvbk5hbWUiOiJUZWNoYXNvIiwibmFtZSI6ImFkbWluIiwiZW1wbG95ZWVDb2RlIjoiVF8xIiwiZW1haWxJZCI6ImFkbWluQHRlY2hhc28ub3JnIiwicHJvZmlsZVBob3RvVXJsIjoiIiwic2hvcEFjY2Vzc0xpc3QiOltdLCJhcHByb3ZhbCI6ZmFsc2V9LCJwZXJtaXNzaW9ucyI6eyJtYXN0ZXIiOnsiaXRlbSI6dHJ1ZSwic2hvcCI6dHJ1ZSwic3VwcGxpZXIiOnRydWUsImN1c3RvbWVyIjp0cnVlLCJjcmVhdGUiOnRydWUsImVtcGxveWVlIjp0cnVlfSwiaW52ZW50b3J5Ijp7ImludmVudG9yeSI6dHJ1ZX0sImJpbGxpbmciOnsicG9zIjp0cnVlLCJyZXR1cm5faXRlbSI6dHJ1ZSwiYmlsbF9oaXN0b3J5Ijp0cnVlfSwicmVwb3J0cyI6eyJnZW5lcmFsIjp0cnVlLCJvdmVydmlldyI6dHJ1ZSwiYWRtaW5pc3RyYXRpb24iOnRydWUsImRheV9ib29rIjp0cnVlLCJnc3QiOnRydWV9LCJwcmludGVyX3RlbXBsYXRlcyI6eyJwcmludGVyX3RlbXBsYXRlcyI6dHJ1ZX0sImRhc2hib2FyZCI6eyJkYXNoYm9hcmQiOnRydWV9LCJzdG9jayI6eyJwdXJjaGFzZV9saXN0Ijp0cnVlLCJyZXR1cm5fcHVyY2hhc2UiOnRydWUsInN0b2NrIjp0cnVlfSwicXVvdGF0aW9ucyI6eyJxdW90YXRpb25zIjp0cnVlfX19.YoWHWwJRtMk-FIg1G41zYfNO6-NJBy0iAUE4-tKuMfY"

    @when("Call the employees get api with wrong jwt token")
    def step_api_call_wrong_token(context):
        url = Endpoints.employees_get
        headers = {"Authorization": f"Bearer {context.wrong_token}"}
        GetEmployeesWithWrongJwtToken.response = Apis().get(url=url, headers=headers)

    @then("Check the response of employees get status with invalid jwt token is 401 and should be a dict type")
    def step_response_status_and_type(context):
        assert GetEmployeesWithWrongJwtToken.response.status_code == 401
        assert isinstance(GetEmployeesWithWrongJwtToken.response.json(), dict)

    @step("the get response content with wrong jwt token should contain Authentication Error message")
    def step_authentication_error(context):
        response_data = GetEmployeesWithWrongJwtToken.response.json()
        assert "error" in response_data


class GetEmployeesWithNoJwtToken:
    response = None
    params = None

    @given("Prepare a employee code 'T_1' to call get api")
    def step_create_wrong_jwt_token(context):
        context.params = {
            "employee_code" : "T_1"
        }

    @when("Call the employees get api with given employee code")
    def step_api_call_wrong_token(context):
        url = Endpoints.employees_get
        headers = {"Authorization": f"Bearer "}
        GetEmployeesWithNoJwtToken.response = Apis().get(url=url, headers=headers,data=context.params)

    @then("Check the response of employees get status with no jwt token is 401 and should be a dict type")
    def step_response_status_and_type(context):
        assert GetEmployeesWithNoJwtToken.response.status_code == 401
        assert isinstance(GetEmployeesWithNoJwtToken.response.json(), dict)

    @step("the get response content with no jwt token should contain Authentication Error message")
    def step_authentication_error(context):
        response_data = GetEmployeesWithNoJwtToken.response.json()
        assert "error" in response_data
