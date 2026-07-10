import pandas
from biller_apps.common.common import Common
from biller_apps.general_report.models import GeneralReport


class GeneralReportUtils:

    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'item__name': 'ItemName',
            'supplier__name': 'SupplierName',
            'quantity': 'Quantity',
            'buying_price': 'BuyingPrice',
            'landing_cost': 'LandingCost',
            'selling_price': 'SellingPrice',
            'tax': 'Tax',
            'bill_amount': 'BillAmount',
            'created_date_time': 'CreatedDateTime',
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)

        # Format date fields if they are in the required columns
        if 'purchaseCreatedDateTime' in self.columns_required:
            dataframe['purchaseCreatedDateTime'] = pandas.to_datetime(dataframe['purchaseCreatedDateTime'])
            dataframe['purchaseCreatedDateTime'] = dataframe['purchaseCreatedDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'quotationCreatedDate' in self.columns_required:
            dataframe['quotationCreatedDate'] = pandas.to_datetime(dataframe['quotationCreatedDate'])
            dataframe['quotationCreatedDate'] = dataframe['quotationCreatedDate'].dt.strftime('%Y-%m-%d')

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
        The key can be one of the following: 'report_id', 'purchase_id', 'quotation_id'
        The value is the associated data with respect to the key.
        """
        data = None
        if key == 'report_id':
            data = GeneralReport.objects.filter(
                organisation_id__company_name=organisation_name, report_id=value
            ).first()
        elif key == 'purchase_id':
            data = GeneralReport.objects.filter(
                organisation_id__company_name=organisation_name, purchase_id=value
            ).first()
        elif key == 'quotation_id':
            data = GeneralReport.objects.filter(
                organisation_id__company_name=organisation_name, quotation_id=value
            ).first()

        return data
