import pandas

from biller_apps.common.common import Common


class ItemUtils:
    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'name': 'name',
            'description': 'description',
            'code': 'code',
            'is_active': 'isActive',
            'item_code': 'itemCode',
            'brand_id__brand_code': 'brandCode',
            'brand_id__name': 'brandName',
            'category_id__name': 'categoryName',
            'category_id__category_code': 'categoryCode',
            'supplier_id__name': 'supplierName',
            'supplier_id__supplier_code': 'supplierCode',
            'created_time': 'createdTime',
            'image_url': "imageUrl",
            'hsn_code': 'hsnCode',
            'tax_code_id__name':'taxName',
            'tax_code_id__tax_code':'taxCode'
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        if 'createdTime' in self.columns_required:
            dataframe['createdTime'] = pandas.to_datetime(dataframe['createdTime'])
            dataframe['createdTime'] = dataframe['createdTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        if len(self.columns_required) == 0:
            dataframe['createdTime'] = pandas.to_datetime(dataframe['createdTime'])
            dataframe['createdTime'] = dataframe['createdTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)
        dataframe = dataframe[self.columns_required]

        return dataframe.to_json(orient='records')
