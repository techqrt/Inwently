import pandas
from biller_apps.common.common import Common
from biller_apps.stock_transfer.models import StockTransfer


class StockTransferUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'organisation_id__company_name': 'organisationName',
            'source_shop_id__name': 'sourceShop',
            'destination_shop_id__name': 'destinationShop',
            'item_id__name': 'itemName',
            'quantity': 'quantity',
            'transfer_date_time': 'transferDateTime',
            'created_date_time': 'createdDateTime',
            'status': 'status',
            'remarks': 'remarks',
            'requested_by': 'requestedBy',
            'approved_by': 'approvedBy',
            'transfer_id': 'transferId',
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)

        # Format date fields if they are in the required columns
        if 'transferDateTime' in self.columns_required:
            dataframe['transferDateTime'] = pandas.to_datetime(dataframe['transferDateTime'])
            dataframe['transferDateTime'] = dataframe['transferDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'createdDateTime' in self.columns_required:
            dataframe['createdDateTime'] = pandas.to_datetime(dataframe['createdDateTime'])
            dataframe['createdDateTime'] = dataframe['createdDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # If no specific columns are required, return the full data
        if len(self.columns_required) == 0:
            return dataframe.to_json(orient='records')
        else:
            # Validate the required columns
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)

        # Filter the dataframe based on the required columns
        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, organisation_name: str) -> None | dict:
        """
        The key can be one of the following: 'transfer_id', 'status'\n
        The value is the associated data with respect to the key.
        """
        data = None
        if key == 'transfer_id':
            data = StockTransfer.objects.filter(
                organisation_id__company_name=organisation_name, transfer_id=value
            ).first()
        elif key == 'status':
            data = StockTransfer.objects.filter(
                organisation_id__company_name=organisation_name, status=value
            ).first()

        return data
