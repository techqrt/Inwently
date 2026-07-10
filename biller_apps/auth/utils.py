import json

import pandas

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.user_specific import UserSpecificData
from biller_apps.common.exceptions.token_errors import TokenErrors
from biller_apps.employees.dataclasses.request.create import Permissions, PermissionsDashboard, PermissionsInventory, \
    PermissionsMaster, PermissionsReports, PrinterTemplatesPermission, SalesPermission, PurchasePermission, \
    QuotationsPermission
from biller_apps.employees.models.employees import Employees
from biller_apps.shops.models import Shops


class AuthUtils:

    @staticmethod
    def get_shop_list_for_user(shop_ids:list):
        try:
            shops = list(Shops.get_by_ids(shop_ids=shop_ids))
            shop_dataframe = pandas.DataFrame.from_records(shops)
            shop_dataframe.rename(columns={'name': 'name', 'shop_code': 'shopCode'}, inplace=True)
            return json.loads(shop_dataframe.to_json(orient='records'))
        except Exception:
            return  []
    @staticmethod
    def mapper(user_data):
        shops = AuthUtils.get_shop_list_for_user(shop_ids=user_data['shop_access'])

        return UserSpecificData(
            organisationName=user_data['organisation_id__company_name'], name=user_data['name'],
            employeeCode=user_data['employee_code'], emailId=user_data['employee_credentials_id__email_id'],
            profilePhotoUrl=user_data['profile_photo_url'], shopAccessList=shops,
            approval=user_data['organisation_id__approval'])

    @staticmethod
    def permission_mapper(user_data):
        return Permissions(
            dashboard=PermissionsDashboard(dashboard=user_data['dashboard_permission__dashboard']),
            master=PermissionsMaster(
                item=user_data['master_data_permission__item'],
                shop=user_data['master_data_permission__shop'],
                supplier=user_data['master_data_permission__supplier'],
                customer=user_data['master_data_permission__customer'],
                create=user_data['master_data_permission__creating'],
                employee=user_data['master_data_permission__employee']
            ),
            inventory=PermissionsInventory(inventory=user_data['inventory_permission__inventory']),
            billing=SalesPermission(
                pos=user_data['sales_permission__pos'],
                return_item=user_data['sales_permission__return_item'],
                bill_history=user_data['sales_permission__bill_history']
            ),
            quotations=QuotationsPermission(quotations=user_data['quotations_permission__quotations']),
            printer_templates=PrinterTemplatesPermission(
                printer_templates=user_data['printer_templates_permission__printer_templates']
            ),
            stock=PurchasePermission(
                purchase_list=user_data['purchase_permission__purchase_list'],
                return_purchase=user_data['purchase_permission__return_purchase'],
                stock=user_data['purchase_permission__stock']
            ),
            reports=PermissionsReports(
                general=user_data['reports_permission__general'],
                overview=user_data['reports_permission__overview'],
                administration=user_data['reports_permission__administration'],
                day_book=user_data['reports_permission__day_book'],
                gst=user_data['reports_permission__gst']
            )
        )

    @staticmethod
    def token_key_validations(payload):
        if isinstance(payload, dict) is False:
            raise TokenErrors(errors=Constants.invalid_access_token)
        for key in ['expiry', 'user_specific_data', 'permissions']:
            if key not in payload.keys():
                raise TokenErrors(errors=Constants.invalid_access_token)

    @staticmethod
    def get_user_info_from_db(email_id: str, organisation_name: str) -> dict:
        return Employees.get_by_email(email=email_id, organisation_name=organisation_name)
