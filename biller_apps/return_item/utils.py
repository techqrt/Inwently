import pandas

from biller_apps.common.common import Common
from biller_apps.return_item.models import ReturnItem


class ReturnItemUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'return_id': 'returnId',
            'return_code': 'returnCode',
            'bill__bill_number': 'billNumber',
            'bill__customer_billing_id__bill_number': 'billNumber',
            'supplier__name': 'supplierName',
            'item__name': 'itemName',
            'return_reason': 'returnReason',
            'quantity': 'quantity',
            'price': 'price',
            'tax': 'tax',
            'total_price': 'totalPrice',
            'created_date_time': 'createdDateTime'
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
    def check_uniqueness(key: str, value: str, bill_number: str) -> None | dict:
        """
        The key can be any of the following: 'item_id', 'supplier_id'\n
        The value is the associated data with respect to the key.
        """
        data = None
        if key == 'item_id':
            data = ReturnItem.objects.filter(bill__bill_number=bill_number, item_id=value).first()
        elif key == 'supplier_id':
            data = ReturnItem.objects.filter(bill__bill_number=bill_number, supplier_id=value).first()

        return data
