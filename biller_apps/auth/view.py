import datetime
import secrets
from dataclasses import asdict

import jwt
from argon2 import PasswordHasher
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.auth_activate import  RegisterRequest
from biller_apps.auth.dataclasses.request.auth_login import LoginRequest
from biller_apps.auth.dataclasses.request.email_verify import EmailVerify
from biller_apps.auth.dataclasses.request.forgot_password import ForgotPassword
from biller_apps.auth.dataclasses.request.password_change import PasswordChange
from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.auth.dataclasses.request.user_specific import UserSpecificData
from biller_apps.auth.utils import AuthUtils
from biller_apps.common.common import Common
from biller_apps.common.email import EmailService
from biller_apps.common.email_template import EmailTemplate
from biller_apps.common.exceptions.token_errors import TokenErrors
from biller_apps.common.exceptions.validation_errors import ValidationErrors
from biller_apps.common.utils import Utils
from biller_apps.employees.dataclasses.request.create import Permissions
from biller_apps.employees.models.employees import EmployeeCredentials, Employees


# noinspection PyMethodParameters
class AuthView:
    def __init__(self):
        self.invalid_cred = "Email or Password is incorrect"
        self.not_active = "Not an active user"
        self.activation_failed = "Failed to activate the user"
        self.expired_url = "The activation url has been expired"
        self.activate_successfully = "The user has been successfully activated"
        self.password_changed = "Password changed successfully"
        self.forgot_password = "The instruction are shared to your email. Please check your mail box"
        self.access_token_expiry_min = 30
        self.refresh_token_expiry_day = 1
        self.user_not_found = "User not found"
        self.otp_shared = "The otp has been shared successfully to your email"

    def generate_new_token(self, payload: dict, user_data: dict, token_key: str, user_specific_data: dict):
        user_specific = AuthUtils.mapper(user_specific_data)
        permissions_data = AuthUtils.permission_mapper(user_specific_data)

        access_token = self.generate_token(token_key=token_key, user_specific_data=user_specific,
                                           permissions=permissions_data,

                                           expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                                               minutes=self.access_token_expiry_min))
        Employees.update_access_token(employee_id=user_data['employee_id'], access_token=access_token)
        data = {'access_token': access_token}
        response_data = Utils.success_response_data(message=Constants.auth_success, data=data)
        return Response(response_data, status.HTTP_200_OK)

    @staticmethod
    def get_user_from_refresh_token(auth_headers: str):
        refresh_token = auth_headers.split()[1]
        payload = jwt.decode(refresh_token, options={"verify_signature": False})
        AuthUtils.token_key_validations(payload=payload)
        user_info = AuthUtils.get_user_info_from_db(email_id=payload['user_specific_data']['emailId'],
                                                    organisation_name=payload['user_specific_data']['organisationName'])
        payload = jwt.decode(refresh_token, user_info['token_key'], algorithms='HS256')
        user_data = EmployeeCredentials.get_with_email(email_id=payload['user_specific_data']['emailId'])
        return user_data, payload, refresh_token, user_info['token_key']

    @staticmethod
    def generate_random_key(length=32):
        return secrets.token_hex(length)

    @staticmethod
    def check_expiry_of_access_token(employee_credentials_id: int, token_key: str) -> tuple:
        user_data = Employees.get_by_id(employee_credentials_id=employee_credentials_id)
        if user_data['access_token']:
            access_token_saved = jwt.decode(user_data['access_token'], token_key, algorithms='HS256')
            expiry_time = datetime.datetime.strptime(access_token_saved['expiry'], '%Y-%m-%d %H:%M:%S.%f%z')
            return user_data, expiry_time
        if user_data['refresh_token']:
            access_token_saved = jwt.decode(user_data['refresh_token'], token_key, algorithms='HS256')
            expiry_time = datetime.datetime.strptime(access_token_saved['expiry'], '%Y-%m-%d %H:%M:%S.%f%z')
            return user_data, expiry_time

    @Common().exception_handler
    def get_token_extract(self, request: Request) -> Response:
        auth_headers = request.headers.get('Authorization')
        if auth_headers is None:
            raise TokenErrors(errors=[Constants.invalid_header])

            # it's in the format 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI....'
        user_data, payload, refresh_token, token_key = self.get_user_from_refresh_token(auth_headers=auth_headers)
        cred_id = user_data['employee_credentials_id']

        user_data, expiry_time = self.check_expiry_of_access_token(
            employee_credentials_id=user_data['employee_credentials_id'], token_key=token_key)

        if user_data['access_token']:
            # return the existing access token - 30 mins
            present_time = datetime.datetime.now(datetime.timezone.utc)
            if expiry_time > present_time and user_data['refresh_token'] == refresh_token:
                return Response(status=status.HTTP_200_OK,
                                data=Utils.success_response_data(message=Constants.auth_success,
                                                                 data={'access_token': user_data['access_token']}))

        # return a new access token
        if user_data['refresh_token'] == refresh_token:
            user_specific_data = Employees.get_login_auth(employee_credentials_id=cred_id)
            if user_specific_data is None:
                raise ValidationErrors(errors=[self.not_active])
            return self.generate_new_token(payload=payload, user_data=user_data, token_key=token_key,
                                           user_specific_data=user_specific_data)
        raise TokenErrors(errors=[Constants.refresh_token_invalid])

    def password_verify(self, user_data: dict, db_password: str, param_password: str):
        hasher = PasswordHasher()
        if user_data is None:
            raise ValidationErrors(errors=[self.invalid_cred])
        try:
            verify = hasher.verify(db_password, param_password)
        except Exception:
            raise ValidationErrors(errors=[self.invalid_cred])

    @Common().exception_handler
    def login_extract(self, params: LoginRequest):
        user_data = EmployeeCredentials.get_with_email(email_id=params.email_id)
        if user_data is None:
            raise ValidationErrors(errors=[self.invalid_cred])
        self.password_verify(user_data=user_data, db_password=user_data['password'], param_password=params.password)

        user_data = Employees.get_login_auth(employee_credentials_id=user_data['employee_credentials_id'])

        if user_data is None:
            raise ValidationErrors(errors=[self.not_active])
        payload = dict()
        token_key = self.generate_random_key()
        user_specific_data = AuthUtils.mapper(user_data)

        permissions_data = AuthUtils.permission_mapper(user_data)

        access_token = self.generate_token(token_key=token_key, user_specific_data=user_specific_data,
                                           permissions=permissions_data,
                                           expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                                               minutes=self.access_token_expiry_min))

        refresh_token = self.generate_token(token_key=token_key, user_specific_data=user_specific_data,
                                            permissions=permissions_data,
                                            expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                                                days=self.refresh_token_expiry_day))

        payload['access_token'] = access_token
        payload['refresh_token'] = refresh_token
        Employees.update_tokens(employee_id=user_data['employee_id'], access_token=access_token,
                                refresh_token=refresh_token, token_key=token_key)

        return Response(data=Utils.success_response_data(message=Constants.auth_success, data=payload),
                        status=status.HTTP_200_OK)

    @Common().exception_handler
    def register_extract(self, request, params: RegisterRequest):
        employee_data = Employees.get_for_register(email_id=params.email_id,otp=params.email_otp)
        if employee_data is None:
            raise ValidationErrors(errors=[self.not_active])
        with transaction.atomic():
            Employees.update_activation(employee_id=employee_data['employee_id'], is_active=True, email_verified=True)
            EmployeeCredentials.update(new_password=params.password,
                                   employee_credentials_id=employee_data['employee_credentials_id_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.activate_successfully))

    @Common().exception_handler
    def password_change_extract(self, params: PasswordChange, token_payload: Payload):
        user_data = EmployeeCredentials.get_with_email(email_id=token_payload.email_id)
        self.password_verify(user_data=user_data, db_password=user_data['password'], param_password=params.old_password)
        EmployeeCredentials.update(new_password=params.new_password,
                                   employee_credentials_id=user_data['employee_credentials_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.password_changed))

    @staticmethod
    def generate_token(token_key: str, expiry: datetime.datetime, user_specific_data: UserSpecificData = None,
                       permissions: Permissions = None) -> str:
        expiry = expiry.strftime('%Y-%m-%d %H:%M:%S.%f%z')
        payload = asdict(TokenPayload(expiry=expiry, user_specific_data=user_specific_data, permissions=permissions))
        token = jwt.encode(payload=payload, key=token_key, algorithm='HS256')
        return token

    @Common().exception_handler
    def forgot_password_extract(self, params: ForgotPassword, present_url: str):
        user_data = Employees.get_by_email_and_otp(email_id=params.email_id, otp=params.email_otp)
        if user_data is None:
            raise ValidationErrors(errors=[self.user_not_found])
        email_temp = EmailTemplate()

        email_temp.set_forgot_password_email(name=user_data['name'],)
        EmployeeCredentials.update(new_password=params.new_password, employee_credentials_id=user_data['employee_credentials_id_id'])
        EmailService(subject=email_temp.subject, body=email_temp.body, to=[params.email_id]).send_email()
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.password_changed))

    @Common().exception_handler
    def email_verify_extract(self, params: EmailVerify):
        user_data = Employees.get_with_email(email_id=params.email)
        if user_data is None:
            raise ValidationErrors(errors=[self.invalid_cred])
        email_template = EmailTemplate()
        otp = Utils.generate_otp()
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
        expiry = expiry.strftime('%Y-%m-%d %H:%M:%S.%f%z')
        Employees.update_otp(employee_id=user_data['employee_id'], otp=otp, expiry=expiry)
        email_template.set_email_verify(name=user_data['name'],otp=otp,expiry_time=expiry)
        EmailService(subject=email_template.subject, body=email_template.body, to=[params.email]).send_email()
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.otp_shared))
