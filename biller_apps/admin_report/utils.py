import pandas
from biller_apps.common.common import Common
from biller_apps.employees.models.employees import Employees


class AdminReportUtils:
    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        
        # Mapped column names for Employees model
        self.employee_mapped_columns = {
            'employee_id': 'EmployeeID',
            'name': 'EmployeeName',
            'mobile_number': 'EmployeeMobile',
            'alternate_mobile_number': 'EmployeeAlternateMobile',
            'dob': 'EmployeeDOB',
            'employee_code': 'EmployeeCode',
            'email_verified': 'EmployeeEmailVerified',
            'created_date_time': 'EmployeeCreatedTime',
            'is_active': 'EmployeeActiveStatus',
            'is_active_change_time': 'EmployeeStatusChangeTime',
            'profile_photo_url': 'EmployeeProfilePhotoURL',
            'address_id__street': 'EmployeeStreetAddress',
            'address_id__state': 'EmployeeState',
            'address_id__country': 'EmployeeCountry'
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'

        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.employee_mapped_columns, inplace=True)
        
        # Format date fields if applicable
        date_fields = ['EmployeeDOB', 'EmployeeCreatedTime', 'EmployeeStatusChangeTime']
        for field in date_fields:
            if field in dataframe.columns:
                dataframe[field] = pandas.to_datetime(dataframe[field])
                dataframe[field] = dataframe[field].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # If no specific columns are required, return full data
        if len(self.columns_required) == 0:
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.employee_mapped_columns,
                                      columns_required=self.columns_required)
        
        # Filter dataframe based on required columns
        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, organisation_name: str) -> None | dict:
        """
        The key can be 'employee_id'.
        The value is the associated data with respect to the key.
        """
        data = Employees.objects.filter(
            organisation_id__company_name=organisation_name, employee_id=value
        ).first()
        
        return data
