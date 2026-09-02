import pandas

from biller_apps.common.common import Common
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees


class EmployeeUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'name': 'name',
            'mobile_number': 'mobileNumber',
            'alternate_mobile_number':'alternate_mobile_number',
            'dob': 'dob',
            'shop_access':'shopAccess',
            'address_id_id__state': 'state',
            'address_id_id__country': 'country',
            'address_id_id__street': 'street',
            'is_active': 'isActive',
            'employee_credentials_id__email_id': 'emailId',
            'email_verified': 'emailVerified',
            'employee_code': 'employeeCode',
            'profile_photo_url':'profilePhotoUrl',
            'dashboard_permission__dashboard': 'permissions.dashboard.dashboard',
            'master_data_permission__item': 'permissions.master.item',
            'master_data_permission__supplier': 'permissions.master.supplier',
            'master_data_permission__shop': 'permissions.master.shop',
            'master_data_permission__customer': 'permissions.master.customer',
            'master_data_permission__employee': 'permissions.master.employee',
            'master_data_permission__creating': 'permissions.master.create',
            'inventory_permission__inventory': 'permissions.inventory.inventory',
            'sales_permission__pos': 'permissions.billing.pos',
            'sales_permission__return_item': 'permissions.billing.return_item',
            'sales_permission__bill_history': 'permissions.billing.bill_history',
            'quotations_permission__quotations': 'permissions.quotations.quotations',
            'printer_templates_permission__printer_templates': 'permissions.printer_templates.printer_templates',
            'purchase_permission__purchase_list': 'permissions.stock.purchase_list',
            'purchase_permission__return_purchase': 'permissions.stock.return_purchase',
            'purchase_permission__stock': 'permissions.stock.stock',
            'reports_permission__general': 'permissions.reports.general',
            'reports_permission__overview': 'permissions.reports.overview',
            'reports_permission__administration': 'permissions.reports.administration',
            'reports_permission__day_book': 'permissions.reports.day_book',
            'reports_permission__gst': 'permissions.reports.gst',
            'dispatch_permission__dispatch': 'permissions.dispatch.dispatch',
            'organisation_id__company_name':'organisationName'
        }

    def consolidate_permissions(self, row):
        return {
        'master': {
            'item': row['permissions.master.item'],
            'shop': row['permissions.master.shop'],
            'supplier': row['permissions.master.supplier'],
            'customer': row['permissions.master.customer'],
            'create': row['permissions.master.create'],
            'employee': row['permissions.master.employee']
        },
        'inventory': {
            'inventory': row['permissions.inventory.inventory']
        },
        'billing': {
            'billHistory': row['permissions.billing.bill_history'],
            'pos': row['permissions.billing.pos'],
            'returnItem': row['permissions.billing.return_item']
        },
        'reports': {
            'overview': row['permissions.reports.overview'],
            'general': row['permissions.reports.general'],
            'administration': row['permissions.reports.administration'],
            'dayBook': row['permissions.reports.day_book'],
            'gst': row['permissions.reports.gst']
        },
        'dashboard': {
            'dashboard': row['permissions.dashboard.dashboard']
        },
        'stock': {
            'stock': row['permissions.stock.stock'],
            'purchaseList': row['permissions.stock.purchase_list'],
            'returnPurchase': row['permissions.stock.return_purchase']
        },
        'quotations': {
            'quotations': row['permissions.quotations.quotations']
        },
        'printerTemplates': {
            'printerTemplates': row['permissions.printer_templates.printer_templates']
        },
        'dispatch': {
            'dispatch': row['permissions.dispatch.dispatch']
        }
    }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        dataframe['permissions'] = dataframe.apply(lambda row: self.consolidate_permissions(row), axis=1)
        dataframe.drop(columns=['permissions.master.item','permissions.master.shop',
                                'permissions.master.supplier','permissions.master.customer',
                                'permissions.master.create','permissions.master.employee',
                                'permissions.inventory.inventory','permissions.billing.bill_history',
                                'permissions.billing.pos','permissions.billing.return_item',
                                'permissions.reports.overview','permissions.reports.general',
                                'permissions.reports.administration','permissions.reports.day_book',
                                'permissions.reports.gst','permissions.dashboard.dashboard',
                                'permissions.stock.stock','permissions.stock.purchase_list',
                                'permissions.stock.return_purchase','permissions.quotations.quotations',
                                'permissions.printer_templates.printer_templates',
                                'permissions.dispatch.dispatch'],
                       inplace=True)
        if 'dob' in self.columns_required:
            dataframe['dob'] = pandas.to_datetime(dataframe['dob'])
            dataframe['dob'] = dataframe['dob'].dt.strftime('%Y-%m-%d')
        if len(self.columns_required) == 0:
            dataframe['dob'] = pandas.to_datetime(dataframe['dob'])
            dataframe['dob'] = dataframe['dob'].dt.strftime('%Y-%m-%d')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)

        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, organisation_name: str,present_employee_id:int=None) -> None | dict:
        """
        The key can be any of the one given that: 'mobile_number','email_id'\n
        The value is the associated data wit respect to key.
        """
        data = None
        if key == 'email_id':
            if present_employee_id is not None:
                data = Employees.get_by_id_except_one(employee_id=present_employee_id,email_id=value)
            else:
                data = EmployeeCredentials.get_with_email(email_id=value)
        elif key == 'mobile_number':
            data = Employees.get_by_mobile(organisation_name=organisation_name, mobile_number=value,exclude_employee_id=present_employee_id)
        return data
