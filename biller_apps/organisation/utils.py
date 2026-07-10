import pandas
from biller_apps.common.common import Common


class OrganisationUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'owner_name': 'ownerName',
            'owner_mobile': 'ownerMobile',
            'created_date_time': 'createdDateTime',
            'shop_count': 'shopCount',
            'employee_count': 'employeeCount',
            'approval': 'approval',
            'plan': 'plan',
            'plan_expiry': 'planExpiry',
            'owner_alternate_mobile':'ownerAlternateMobile',
            'company_name':'companyName'
        }

    def mapper(self, data: list) -> str:
        if len(data) == 0:
            return '[]'

        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)

        if 'createdDateTime' in dataframe.columns:
            dataframe['createdDateTime'] = pandas.to_datetime(dataframe['createdDateTime'], errors='coerce')
            dataframe['createdDateTime'] = dataframe['createdDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        if 'planExpiry' in dataframe.columns:
            dataframe['planExpiry'] = pandas.to_datetime(dataframe['planExpiry'], errors='coerce')
            dataframe['planExpiry'] = dataframe['planExpiry'].dt.strftime('%Y-%m-%d %H:%M:%S')

        if len(self.columns_required) == 0:
            return dataframe.to_json(orient='records')
        missing_columns = [col for col in self.columns_required if col not in dataframe.columns]
        if missing_columns:
            return Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                             columns_required=self.columns_required)

        dataframe = dataframe.filter(items=self.columns_required, axis=1)
        return dataframe.to_json(orient='records')
