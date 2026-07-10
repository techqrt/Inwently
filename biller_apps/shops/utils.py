import pandas

from biller_apps.common.common import Common


class ShopsUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'is_active': 'isActive',
            'organisation_id_id__name': 'organisationName',
            'created_date_time': 'createdDateTime',
            'address_id_id__state': 'state',
            'address_id_id__street': 'street',
            'address_id_id__country': 'country',
            'is_active_change_time': 'isActiveChangeTime',
            'shop_code': 'shopCode',
            'website': 'website',
            'email_id': 'emailId',
            'mobile_number': 'mobileNumber',
            'alt_mobile_number': 'altMobileNumber'
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        if 'createdDateTime' in self.columns_required:
            dataframe['createdDateTime'] = dataframe['createdDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'isActiveChangeTime' in self.columns_required:
            dataframe['isActiveChangeTime'] = dataframe['isActiveChangeTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        if len(self.columns_required) == 0:
            dataframe['createdDateTime'] = dataframe['createdDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            dataframe['isActiveChangeTime'] = dataframe['isActiveChangeTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)
        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')
