import datetime
import json
import urllib
import uuid

import pandas
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.auth.utils import AuthUtils
from biller_apps.auth.view import AuthView
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.exceptions.validation_errors import ValidationErrors
from biller_apps.common.models.adress import Address
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.employees.dataclasses.request.bulk_status_change import EmployeeBulkStatusChangeRequest
from biller_apps.employees.dataclasses.request.create import Permissions, EmployeesRequest, PermissionsDashboard, \
    PermissionsInventory, PermissionsMaster, PermissionsReports, PrinterTemplatesPermission, SalesPermission, \
    PurchasePermission, QuotationsPermission, DispatchPermission
from biller_apps.employees.dataclasses.request.delete import EmployeeDelete
from biller_apps.employees.dataclasses.request.delete_many import EmployeeDeleteManyRequest
from biller_apps.employees.dataclasses.request.get import EmployeeGet
from biller_apps.employees.dataclasses.request.update import EmployeesUpdateRequest
from biller_apps.employees.es_query import EmployeeEsQuery
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees
from biller_apps.employees.models.permission import SalesPermission, PrinterTemplatesPermission, ReportsPermission, \
    PurchasePermission, DashboardPermission, InventoryPermission, MasterDataPermission, QuotationsPermission, \
    DispatchPermission
from biller_apps.employees.serializers.response.get import EmployeesGetResponseSerializer
from biller_apps.employees.serializers.response.get_all import EmployeesGetAllResponseSerializer
from biller_apps.employees.utils import EmployeeUtils
from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops


class EmployeesView:
    def __init__(self) -> None:
        super().__init__()
        self.data_create = "Employee added successfully"
        self.data_update = "Employee updated successfully"
        self.data_delete = "Employee deleted successfully"
        self.data_no_match = "No matching employee found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"
        self.employees_limit_exceeded = 'Employees limit exceeded'
        self.bulk_status_update = 'Status has been changed for all given employees'

    @staticmethod
    def get_shop_ids(shop_ids_list: list) -> list:
        seen = set()
        unique_ids = []
        for row in shop_ids_list:
            if row['shop_id'] not in seen:
                seen.add(row['shop_id'])
                unique_ids.append(row['shop_id'])
        return unique_ids

    @staticmethod
    def check_constrains(params: EmployeesRequest | EmployeesUpdateRequest, token_payload: Payload,
                         present_employee_id=None):
        mob_unique = EmployeeUtils.check_uniqueness(key='mobile_number', value=params.mobile_number,
                                                    organisation_name=token_payload.organisationName,
                                                    present_employee_id=present_employee_id)
        email_unique = EmployeeUtils.check_uniqueness(key='email_id', value=params.email_id,
                                                      organisation_name=token_payload.organisationName,
                                                      present_employee_id=present_employee_id)

        errors = []
        if mob_unique is not None:
            errors.append(Constants.mobile_number_not_unique)
        if email_unique is not None:
            errors.append(Constants.email_id_not_unique)
        if len(errors) > 0:
            raise ValidationErrors(errors=errors)

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: EmployeesRequest, token_payload: Payload,host:str, password: str = None):
        passw = password if password else str(uuid.uuid4())
        self.check_constrains(params=params, token_payload=token_payload)

        with transaction.atomic():
            organisation_data = Organisation.get(company_name=token_payload.organisationName, single=True)
            employee_count = Employees.get_count(organisation_name=token_payload.organisationName)
            if employee_count > organisation_data['employee_count']:
                raise ValueError(self.employees_limit_exceeded)
            address_id = Address().create(street=params.street, state=params.state, country=params.country)
            permissions = Permissions(**params.permissions)
            master_permissions = PermissionsMaster(**permissions.master)
            inventory_permissions = PermissionsInventory(**permissions.inventory)

            billing_permissions = SalesPermission(**permissions.billing)
            reports_permissions = PermissionsReports(**permissions.reports)
            dashboard_permissions = PermissionsDashboard(**permissions.dashboard)
            stock_permissions = PurchasePermission(**permissions.stock)
            printer_templates_permissions = PrinterTemplatesPermission(**permissions.printer_templates)
            quotation_permissions = QuotationsPermission(**permissions.quotations)
            dispatch_permissions = DispatchPermission(**permissions.dispatch)

            dashboard_permission_id = DashboardPermission().create(dashboard=dashboard_permissions.dashboard)
            master_data_permission_id = MasterDataPermission().create(
                item=master_permissions.item,
                supplier=master_permissions.supplier,
                shop=master_permissions.shop,
                customer=master_permissions.customer,
                employee=master_permissions.employee,
                create=master_permissions.create
            )
            inventory_permission_id = InventoryPermission().create(inventory=inventory_permissions.inventory)
            sales_permission_id = SalesPermission().create(
                pos=billing_permissions.pos,
                return_item=billing_permissions.return_item,
                bill_history=billing_permissions.bill_history
            )
            quotations_permission_id = QuotationsPermission().create(quotations=quotation_permissions.quotations)
            purchase_permission_id = PurchasePermission().create(
                purchase_list=stock_permissions.purchase_list,
                return_purchase=stock_permissions.return_purchase,
                stock=stock_permissions.stock
            )
            reports_permission_id = ReportsPermission().create(
                general=reports_permissions.general,
                overview=reports_permissions.overview,
                administration=reports_permissions.administration,
                day_book=reports_permissions.day_book,
                gst=reports_permissions.gst
            )
            printer_templates_permission_id = PrinterTemplatesPermission().create(
                printer_templates=printer_templates_permissions.printer_templates
            )
            dispatch_permission_id = DispatchPermission().create(dispatch=dispatch_permissions.dispatch)

            credential_id = EmployeeCredentials().create(email_id=params.email_id, password=passw)

            shop_access = self.get_shop_ids(shop_ids_list=Shops.get_with_code_list(shop_code=params.shop_access,
                                                                                   organisation_name=token_payload.organisationName))
            Employees().create(name=params.name, mobile_number=params.mobile_number,alternate_mobile_number=params.alternate_mobile_number,dob=params.dob,
                               shop_access=shop_access, address_id=address_id, credentials_id=credential_id,
                               organisation_id=organisation_data['organisation_id'],
                               organisation_name=token_payload.organisationName,
                               profile_photo_url=params.profile_photo_url,
                               dashboard_permission_id=dashboard_permission_id,
                               master_data_permission_id=master_data_permission_id,
                               inventory_permission_id=inventory_permission_id,
                               sales_permission_id=sales_permission_id,
                               quotations_permission_id=quotations_permission_id,
                               purchase_permission_id=purchase_permission_id,
                               reports_permission_id=reports_permission_id,
                               printer_templates_permission_id=printer_templates_permission_id,
                               dispatch_permission_id=dispatch_permission_id,
                               is_active=True)

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(
            message=self.data_create, data={'email_id': params.email_id, 'password': passw}))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: EmployeesUpdateRequest, token_payload: Payload):
        params.permissions = EmployeesUpdateRequest.dict_to_dataclass(Permissions, params.permissions)
        with transaction.atomic():
            employees_data = Employees.get_connections(employee_code=params.employee_code,
                                                       organisation_name=token_payload.organisationName)
            Address().update(street=params.street, state=params.state, country=params.country,
                             address_id=employees_data['address_id_id'])

            shop_access = self.get_shop_ids(shop_ids_list=Shops.get_with_code_list(shop_code=params.shop_access,
                                                                                 organisation_name=token_payload.organisationName))

            DashboardPermission().update(permission_id=employees_data['dashboard_permission_id'],
                                         dashboard=params.permissions.dashboard.dashboard)
            MasterDataPermission().update(permission_id=employees_data['master_data_permission_id'],
                                          item=params.permissions.master.item,
                                          supplier=params.permissions.master.supplier,
                                          shop=params.permissions.master.shop,
                                          customer=params.permissions.master.customer,
                                          employee=params.permissions.master.employee,
                                          create=params.permissions.master.create)
            InventoryPermission().update(permission_id=employees_data['inventory_permission_id'],
                                         inventory=params.permissions.inventory.inventory)
            SalesPermission().update(permission_id=employees_data['sales_permission_id'],
                                     pos=params.permissions.billing.pos,
                                     return_item=params.permissions.billing.return_item,
                                     bill_history=params.permissions.billing.bill_history)
            QuotationsPermission().update(permission_id=employees_data['quotations_permission_id'],
                                          quotations=params.permissions.quotations.quotations)
            PrinterTemplatesPermission().update(permission_id=employees_data['printer_templates_permission_id'],
                                                printer_templates=params.permissions.printer_templates.printer_templates)
            PurchasePermission().update(permission_id=employees_data['purchase_permission_id'],
                                        purchase_list=params.permissions.stock.purchase_list,
                                        return_purchase=params.permissions.stock.return_purchase,
                                        stock=params.permissions.stock.stock)
            ReportsPermission().update(permission_id=employees_data['reports_permission_id'],
                                       general=params.permissions.reports.general,
                                       overview=params.permissions.reports.overview,
                                       administration=params.permissions.reports.administration,
                                       day_book=params.permissions.reports.day_book,
                                       gst=params.permissions.reports.gst)
            DispatchPermission().update(permission_id=employees_data['dispatch_permission_id'],
                                        dispatch=params.permissions.dispatch.dispatch)

            Employees().update(name=params.name, mobile_number=params.mobile_number,alternate_mobile_number=params.alternate_mobile_number, dob=params.dob,
                               shop_access=shop_access, employee_id=employees_data['employee_id'],
                               profile_photo_url=params.profile_photo_url)
            self.check_constrains(params=params, token_payload=token_payload,
                                  present_employee_id=employees_data['employee_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: EmployeeDelete, token_payload: Payload):
        employees = Employees.objects.filter(employee_code=params.employee_code,
                                             organisation_id__company_name=urllib.parse.unquote(
                                                 token_payload.organisationName)).values(
            'address_id', 'employee_credentials_id', 'employee_id','dashboard_permission_id',
            'master_data_permission_id','inventory_permission_id','printer_templates_permission_id',
            'purchase_permission_id','quotations_permission_id','reports_permission_id','sales_permission_id',
            'dispatch_permission_id').first()

        if employees is None:
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            Address().remove(address_id=employees['address_id'])
            DashboardPermission.remove(permission_id=employees['dashboard_permission_id'])
            MasterDataPermission.remove(permission_id=employees['master_data_permission_id'])
            InventoryPermission.remove(permission_id=employees['inventory_permission_id'])
            SalesPermission.remove(permission_id=employees['sales_permission_id'])
            QuotationsPermission.remove(permission_id=employees['quotations_permission_id'])
            PrinterTemplatesPermission.remove(permission_id=employees['printer_templates_permission_id'])
            PurchasePermission.remove(permission_id=employees['purchase_permission_id'])
            ReportsPermission.remove(permission_id=employees['reports_permission_id'])
            DispatchPermission.remove(permission_id=employees['dispatch_permission_id'])
            EmployeeCredentials().remove(employee_credentials_id=employees['employee_credentials_id'])
            Employees().remove(employee_id=employees['employee_id'])

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common(response_handler=EmployeesGetResponseSerializer).exception_handler
    def get_extract(self, params: EmployeeGet, token_payload: Payload):
        employee_data = Employees.get(employee_code=params.employee_code,
                                      organisation_name=token_payload.organisationName)
        if employee_data is None:
            raise ValueError(self.data_no_match)
        employee_data['shop_access'] = str(AuthUtils.get_shop_list_for_user(shop_ids=employee_data['shop_access']))
        employee_utils = EmployeeUtils(columns_required=params.values_list)
        employee_data = [employee_data]
        data = json.loads(employee_utils.mapper(data=employee_data))[0]
        if data.get('shopAccess', None) is not None:
            data['shopAccess'] = json.loads(data['shopAccess'].replace("'", '"'))
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=EmployeesGetAllResponseSerializer).exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(Employees.get_all(organisation_name=token_payload.organisationName,params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        employees_utils = EmployeeUtils(columns_required=params.values_list)
        data = json.loads(employees_utils.mapper(data=data))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url,
                                        total_page=pages.num_pages, total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: EmployeeDeleteManyRequest, token_payload: Payload):
        if not params.employee_code:
            raise ValueError("Employee list is empty. Please give at least one employee code")
            
        employee = Employees.get_with_code_list(employee_code=params.employee_code,
                                                organisation_name=token_payload.organisationName)
        if len(employee) != len(params.employee_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(employee)
        employee_ids = dataframe['employee_id'].tolist()
        address_ids = dataframe['address_id'].tolist()

        employee_credentials_ids = dataframe['employee_credentials_id'].tolist()
        with transaction.atomic():
            Employees.remove_from_list(employee_id=employee_ids)
            Address.remove_from_list(address_id=address_ids)
            EmployeeCredentials.remove_from_list(employee_credentials_id=employee_credentials_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def bulk_status_change_extract(self, params: EmployeeBulkStatusChangeRequest, token_payload: Payload):
        employee = Employees.get_with_code_list(employee_code=params.employee_code,
                                                organisation_name=token_payload.organisationName)
        if len(employee) != len(params.employee_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(employee)
        employee_ids = dataframe['employee_id'].tolist()
        Employees.status_change_from_list(employee_id=employee_ids, status=params.status)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.bulk_status_update))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = EmployeeEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
