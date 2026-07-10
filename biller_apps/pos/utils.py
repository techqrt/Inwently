import pandas

from biller_apps.common.common import Common
from biller_apps.pos.models import POS


class POSUtils:
    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'pos_id': 'posId',
            'pos_code': 'posCode',
            'customer__name': 'customerName',
            'item__name': 'itemName',
            'quantity': 'quantity',
            'price': 'price',
            'tax': 'tax',
            'discount': 'discount',
            'total': 'total',
            'created_date': 'createdDate',
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        if 'createdDate' in self.columns_required:
            dataframe['createdDate'] = pandas.to_datetime(dataframe['createdDate'])
            dataframe['createdDate'] = dataframe['createdDate'].dt.strftime('%Y-%m-%d')
        if len(self.columns_required) == 0:
            dataframe['createdDate'] = pandas.to_datetime(dataframe['createdDate'])
            dataframe['createdDate'] = dataframe['createdDate'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)
        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, pos_code: str) -> None | dict:
        """
        The key can be any of the following: 'item_id', 'customer_id'
        The value is the associated data with respect to the key.
        """
        data = None
        if key == 'item_id':
            data = POS.objects.filter(pos_code=pos_code, item_id=value).first()
        elif key == 'customer_id':
            data = POS.objects.filter(pos_code=pos_code, customer_id=value).first()

        return data
