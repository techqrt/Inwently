from behave import given, when, then, step
from requests import Response

from features.steps.common.apis import Apis
from features.steps.common.constants import Constants
from features.steps.common.endpoints import Endpoints


class LoginWithValidCredentials:
    username = None
    password = None
    response: Response = None

    @staticmethod
    @given("Prepare the username and password for login api")
    def step_impl(context):
        LoginWithValidCredentials.username = Constants.global_username
        LoginWithValidCredentials.password = Constants.global_password
        assert isinstance(LoginWithValidCredentials.username, str)
        assert isinstance(LoginWithValidCredentials.password, str)

    @staticmethod
    @when("Call the login api endpoint with given username and password")
    def step_impl(context):
        url = Endpoints.login
        payload = {"email_id": LoginWithValidCredentials.username, "password": LoginWithValidCredentials.password}
        LoginWithValidCredentials.response = Apis().post_api(url=url, data=payload)

    @staticmethod
    @then("Check the response status is 200")
    def step_impl(context):
        assert LoginWithValidCredentials.response.status_code == 200

    @staticmethod
    @step("the response content type should be dict")
    def step_impl(context):
        assert isinstance(LoginWithValidCredentials.response.json(), dict)

    @staticmethod
    @step('the response body should contain the keys "access_token" and "refresh_token"')
    def step_impl(context):
        response_data = LoginWithValidCredentials.response.json().get("data", {})
        assert "access_token" in response_data
        assert "refresh_token" in response_data


class LoginWithInvalidCredentials:
    wrong_username = None
    wrong_password = None
    wrong_response: Response = None

    @given("Prepare an incorrect username and password for login api")
    def step_impl(context):
        LoginWithInvalidCredentials.wrong_username = "admi@techaso.org"
        LoginWithInvalidCredentials.wrong_password = "12345678"
        assert isinstance(LoginWithInvalidCredentials.wrong_username, str)
        assert isinstance(LoginWithInvalidCredentials.wrong_password, str)

    @when("Call the login api endpoint with given incorrect username and password")
    def step_impl(context):
        url = Endpoints.login
        payload = {"email_id": LoginWithInvalidCredentials.wrong_username,
                   "password": LoginWithInvalidCredentials.wrong_password}
        LoginWithInvalidCredentials.wrong_response = Apis().post_api(url=url, data=payload)

    @then("Check the response status is 400")
    def step_impl(context):
        assert LoginWithInvalidCredentials.wrong_response.status_code == 400

    @step("the response body should contain an error message")
    def step_impl(context):
        error_resp = {
            "status": False,
            "message": "Validation Error",
            "error": [
                "Email or Password is incorrect"
            ]
        }
        assert LoginWithInvalidCredentials.wrong_response.json() == error_resp


class LoginWithInvalidUsername:
    wrong_username = None
    wrong_password = None
    wrong_response: Response = None

    @given("Prepare an incorrect username  for login api")
    def step_impl(context):
        LoginWithInvalidUsername.wrong_username = "adm@techaso.org"
        LoginWithInvalidUsername.wrong_password = "123456780"
        assert isinstance(LoginWithInvalidUsername.wrong_username, str)
        assert isinstance(LoginWithInvalidUsername.wrong_password, str)

    @when("Call the login api endpoint with given incorrect username")
    def step_impl(context):
        url = Endpoints.login
        payload = {
            "email_id": LoginWithInvalidUsername.wrong_username,
        }
        LoginWithInvalidUsername.wrong_response = Apis().post_api(url=url, data=payload)

    @then("Check the response status is 400 for incorrect username alone")
    def step_impl(context):
        assert LoginWithInvalidUsername.wrong_response.status_code == 400

    @step("the response body should contain an error message with status false and with mesage key")
    def step_impl(context):
        error_resp = {
            "status": False,
            "message": "Validation Error",
            "error": [
                {
                    "password": [
                        "This field is required."
                    ]
                }
            ]
        }
        assert LoginWithInvalidUsername.wrong_response.json() == error_resp
