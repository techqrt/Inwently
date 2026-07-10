import pandas

from biller_apps.common.common import Common


class BillingUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'bill_number': 'billNumber',
            'created_at': 'createdAt',
            'quantity': 'quantity',
            'total_price': 'totalPrice',
            'item_id__name': 'itemName',
            'billed_by__employee_code': 'billedBy',
            'shop_id__shop_code': 'shopCode'
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        if len(self.columns_required) == 0:
            if 'createdAt' in dataframe.columns:
                dataframe['createdAt'] = pandas.to_datetime(dataframe['createdAt'])
                dataframe['createdAt'] = dataframe['createdAt'].dt.strftime('%Y-%m-%d %H:%M:%S')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)

        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')
