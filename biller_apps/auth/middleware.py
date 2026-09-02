import datetime

import jwt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from biller.config import Configurations
from biller.constants import Constants
from biller.settings import URLS_ALLOW_ANONYMOUS
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.auth.utils import AuthUtils
from biller_apps.common.app_logger import Logger
from biller_apps.common.utils import Utils
from biller_apps.employees.dataclasses.request.create import Permissions, PermissionsDashboard, PermissionsInventory, \
    PermissionsMaster, PermissionsReports, PrinterTemplatesPermission, SalesPermission, PurchasePermission, \
    QuotationsPermission, DispatchPermission


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def response_handler(self, request: Request):
        response = self.get_response(request)
        Logger.log.info('stop -> host:' + request.get_host() + ' path:' + request.path)
        if response.status_code == 500 and Configurations.debug is False:
            return error_response(status_code=response.status_code, data=Constants.server_error)
        else:
            return response

    def __call__(self, request: Request) -> Response:
        try:
            Logger.log.info('start -> host:'+request.META.get('REMOTE_ADDR')+' path:'+request.path)
            if request.path in URLS_ALLOW_ANONYMOUS:
                return self.response_handler(request=request)

            auth_headers = request.headers.get('Authorization')
            if auth_headers is None:
                return error_response(status_code=status.HTTP_401_UNAUTHORIZED, data=Constants.invalid_header)

            # it's in the format 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI....'
            access_token = (auth_headers.split())[1]
            payload = jwt.decode(access_token, options={"verify_signature": False})
            AuthUtils.token_key_validations(payload=payload)
            expiry_time = datetime.datetime.strptime(payload['expiry'], '%Y-%m-%d %H:%M:%S.%f%z')
            if expiry_time < datetime.datetime.now(datetime.timezone.utc):
                return error_response(status_code=status.HTTP_401_UNAUTHORIZED, data=Constants.access_token_expired)

            user_info = AuthUtils.get_user_info_from_db(email_id=payload['user_specific_data']['emailId'],
                                                        organisation_name=payload['user_specific_data'][
                                                            'organisationName'])

            payload = jwt.decode(access_token, user_info['token_key'], algorithms='HS256')

            payload['organisation_id'] = user_info['organisation_id_id']

            if access_token != user_info['access_token']:
                return error_response(status_code=status.HTTP_401_UNAUTHORIZED, data=Constants.invalid_access_token)

            # Validate user permissions for module access
            if not self.validate_permissions(request=request, payload=payload):
                return error_response(status_code=status.HTTP_403_FORBIDDEN, data=Constants.forbidden_access)

            permissions = map_permissions_from_payload(payload['permissions'])

            request.payload = Payload(email_id=payload['user_specific_data']['emailId'],
                                      expiry=datetime.datetime.strptime(payload['expiry'],
                                                                        "%Y-%m-%d %H:%M:%S.%f%z"),
                                      organisationName=payload['user_specific_data']['organisationName'],
                                      organisation_id=payload['organisation_id'],
                                      present_url=request.build_absolute_uri(),
                                      access_token=access_token, method=request.method, path=request.path,
                                      approval=payload['user_specific_data']['approval'],
                                      permissions=permissions,
                                      role=payload.get('role', 'EMPLOYEE'))

            return self.response_handler(request=request)

        except Exception as e:
            print("auth error -> " + str(e))
            return error_response(status_code=status.HTTP_401_UNAUTHORIZED,
                                  data=Utils.env_exception_handler(message=str(e)))

    def validate_permissions(self, request: Request, payload: Payload) -> bool:
        path = request.path.lower()
        permissions = payload['permissions']

        # Dictionary mapping URL paths to permissions fields
        permissions_mapping = {
            'master': permissions['master'],
            'inventory': permissions['inventory'],
            'billing': permissions['billing'],
            'reports': permissions['reports'],
            'dashboard': permissions['dashboard'],
            'stock': permissions['stock'],
            'quotations': permissions['stock'],
            'dispatch': permissions['dispatch']
        }

        # Iterate over the dictionary to check if the user has the required permissions
        for key, permission_group in permissions_mapping.items():
            if key in path:
                # Dynamically check all fields in the permission group
                for field, value in permission_group.items():
                    if not value:  # If any field is False, deny access
                        return False

        return True


def map_permissions_from_payload(payload_permissions):
    return Permissions(
        master=PermissionsMaster(
            item=payload_permissions['master']['item'],
            shop=payload_permissions['master']['shop'],
            supplier=payload_permissions['master']['supplier'],
            customer=payload_permissions['master']['customer'],
            create=payload_permissions['master']['create'],
            employee=payload_permissions['master']['employee']
        ),
        inventory=PermissionsInventory(
            inventory=payload_permissions['inventory']['inventory']
        ),
        billing=SalesPermission(
            pos=payload_permissions['billing']['pos'],
            return_item=payload_permissions['billing']['return_item'],
            bill_history=payload_permissions['billing']['bill_history']
        ),
        reports=PermissionsReports(
            general=payload_permissions['reports']['general'],
            overview=payload_permissions['reports']['overview'],
            administration=payload_permissions['reports']['administration'],
            day_book=payload_permissions['reports']['day_book'],
            gst=payload_permissions['reports']['gst']
        ),
        printer_templates=PrinterTemplatesPermission(
            printer_templates=payload_permissions['printer_templates']['printer_templates']
        ),
        dashboard=PermissionsDashboard(
            dashboard=payload_permissions['dashboard']['dashboard']
        ),
        stock=PurchasePermission(
            purchase_list=payload_permissions['stock']['purchase_list'],
            return_purchase=payload_permissions['stock']['return_purchase'],
            stock=payload_permissions['stock']['stock']
        ),
        quotations=QuotationsPermission(
            quotations=payload_permissions['quotations']['quotations']
        ),
        dispatch=DispatchPermission(
            dispatch=payload_permissions['dispatch']['dispatch']
        )
    )


def error_response(status_code=status.HTTP_401_UNAUTHORIZED, data=Constants.auth_error) -> Response:
    response_data = Utils.error_response_data(message=data, error=[data])
    response = Response(status=status_code, data=response_data)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response
