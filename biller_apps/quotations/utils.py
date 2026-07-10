import pandas

from biller_apps.common.common import Common
from biller_apps.quotations.models import Quotation


class QuotationUtils:
    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'quotation_id': 'quotationId',
            'quotation_code': 'quotationCode',
            'supplier__name': 'supplierName',
            'item__name': 'itemName',
            'description': 'description',
            'brand': 'brand',
            'quantity': 'quantity',
            'price': 'price',
            'tax': 'tax',
            'total': 'total',
            'purchase': 'purchase',
            'sales': 'sales',
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
            if 'createdDate' in dataframe.columns:
                dataframe['createdDate'] = pandas.to_datetime(dataframe['createdDate'])
                dataframe['createdDate'] = dataframe['createdDate'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)
        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, quotation_code: str) -> None | dict:
        """
        The key can be any of the following: 'item_id', 'supplier_id'
        The value is the associated data with respect to the key.
        """
        data = None
        if key == 'item_id':
            data = Quotation.objects.filter(quotation_code=quotation_code, item_id=value).first()
        elif key == 'supplier_id':
            data = Quotation.objects.filter(quotation_code=quotation_code, supplier_id=value).first()

        return data
