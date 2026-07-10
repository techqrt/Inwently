import pandas

from biller_apps.common.common import Common
from biller_apps.supplier.models import Supplier


class SupplierUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'organisation_id__company_name': 'organisationName',
            'address_id__country': 'country',
            'address_id__state': 'state',
            'address_id__street': 'street',
            'name': 'name',
            'is_active': 'isActive',
            'mobile_number': 'mobileNumber',
            'email_id': 'emailId',
            'created_date_time': 'createdDateTime',
            'alt_mobile_number': 'altMobileNumber',
            'supplier_code': 'supplierCode',
            'id_number': 'idNumber',
            'id_type': 'idType',
            'gst_number': 'gstNumber',
            'photo_url': 'photoUrl',
            'id_proof_url': 'idProofUrl'
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        if 'createdDateTime' in self.columns_required:
            dataframe['createdDateTime'] = pandas.to_datetime(dataframe['createdDateTime'])
            dataframe['createdDateTime'] = dataframe['createdDateTime'].dt.strftime('%Y-%m-%d')
        if len(self.columns_required) == 0:
            dataframe['createdDateTime'] = pandas.to_datetime(dataframe['createdDateTime'])
            dataframe['createdDateTime'] = dataframe['createdDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)

        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, organisation_name: str) -> None | dict:
        """
        The key can be any of the one given that: 'mobile_number','email_id'\n
        The value is the associated data wit respect to key.
        """
        data = None
        if key == 'mobile_number':
            data = Supplier.get_by_mobile(organisation_name=organisation_name, mobile_number=value)
        elif key == 'email_id':
            data = Supplier.get_by_email(organisation_name=organisation_name, email=value)

        return data
