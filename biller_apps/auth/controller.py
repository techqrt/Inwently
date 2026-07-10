from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.auth.serializers.request.email_verify import EmailVerifyRequestSerializer
from biller_apps.auth.serializers.request.register import RegisterRequestSerializer
from biller_apps.auth.serializers.request.auth import LoginRequestSerializer
from biller_apps.auth.serializers.request.forgot_password import ForgotPasswordRequestSerializer
from biller_apps.auth.serializers.request.password_change import PasswordChangeRequestSerializer
from biller_apps.auth.serializers.response.get_token import GetTokenResponseSerializer
from biller_apps.auth.serializers.response.login_extract import LoginResponseSerializer
from biller_apps.auth.view import AuthView
from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage


# noinspection PyMethodParameters
class AuthController:
    @extend_schema(
        description="Creates new access token with refresh-token. Bearer token must be refresh-token for"
                    " this call",
        responses=SwaggerPage.response(response=GetTokenResponseSerializer, auth=True)

    )
    @api_view(['GET'])
    def get_token(request: Request) -> Response:
        return AuthView().get_token_extract(request)

    @extend_schema(
        description="Retrieves access token for the given credentials",
        request=LoginRequestSerializer,
        responses=SwaggerPage.response(response=LoginResponseSerializer),
        auth=[]
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=LoginRequestSerializer).validate
    def login(request: Request) -> Response:
        return AuthView().login_extract(params=request.params)

    @extend_schema(
        description="Register a particular user after adding a new user in the system",
        request=RegisterRequestSerializer,
        responses=SwaggerPage.response(description=AuthView().activate_successfully),
        auth=[]
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=RegisterRequestSerializer).validate
    def register(request: Request) -> Response:
        return AuthView().register_extract(request,params=request.params)


    @extend_schema(
        description="Change the password",
        request=PasswordChangeRequestSerializer,
        responses=SwaggerPage.response(description=AuthView().password_changed)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=PasswordChangeRequestSerializer).validate
    def password_change(request: Request) -> Response:
        return AuthView().password_change_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Forgot password",
        request=ForgotPasswordRequestSerializer,
        responses=SwaggerPage.response(description=AuthView().password_changed),
        auth=[]
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=ForgotPasswordRequestSerializer).validate
    def forgot_password(request: Request) -> Response:
        return AuthView().forgot_password_extract(params=request.params, present_url=request.build_absolute_uri())

    @extend_schema(
        description="Send an otp to Email for verification of email",
        request=EmailVerifyRequestSerializer,
        responses=SwaggerPage.response(description=AuthView().forgot_password),
        auth=[]
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=EmailVerifyRequestSerializer).validate
    def email_verify(request: Request) -> Response:
        return AuthView().email_verify_extract(params=request.params)