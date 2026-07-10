import pandas

from biller_apps.common.common import Common
from biller_apps.inventory.models import Inventory


class InventoryUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'item_id__name': 'itemName',
            'shop_id__name': 'shopName',
            'expiry_date': 'expiryDate',
            'price': 'price',
            'balance_qty': 'balanceQty',
            'organisation_id__company_name': 'organisationName',
            'created_time': 'createdTime'
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        
        if 'createdTime' in self.columns_required:
            dataframe['createdTime'] = pandas.to_datetime(dataframe['createdTime'])
            dataframe['createdTime'] = dataframe['createdTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        if 'expiryDate' in self.columns_required:
            dataframe['expiryDate'] = pandas.to_datetime(dataframe['expiryDate'])
            dataframe['expiryDate'] = dataframe['expiryDate'].dt.strftime('%Y-%m-%d')

        if len(self.columns_required) == 0:
            dataframe['createdTime'] = pandas.to_datetime(dataframe['createdTime'])
            dataframe['createdTime'] = dataframe['createdTime'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)

        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, organisation_name: str) -> None | dict:
        """
        The key can be either 'sku' or 'item_name'.
        The value is the associated data with respect to the key.
        """
        data = None
        if key == 'item_name':
            # Assuming you have a method to get an inventory item by name
            data = Inventory.objects.filter(item_id__name=value, organisation_id__company_name=organisation_name).first()
        elif key == 'sku':
            # Assuming SKU is associated with items or an additional model that you could reference here
            data = Inventory.objects.filter(item_id__sku=value, organisation_id__company_name=organisation_name).first()

        return data
