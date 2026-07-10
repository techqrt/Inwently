import pandas
from biller_apps.common.common import Common
from biller_apps.item.models.items import Items
from biller_apps.supplier.models import Supplier
from biller_apps.customer.models import Customer


class OverviewReportUtils:
    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        
        # Mapped column names for different models
        self.item_mapped_columns = {
            'item_id': 'ItemID',
            'name': 'ItemName',
            'description': 'ItemDescription',
            'code': 'ItemCode',
            'is_active': 'ItemActiveStatus',
            'item_code': 'ItemUniqueCode',
            'created_time': 'ItemCreatedTime',
            'image_url': 'ItemImageURL',
            'brand_id__name': 'BrandName',
            'brand_id__brand_code': 'BrandCode',
            'supplier_id__name': 'SupplierName',
            'supplier_id__supplier_code': 'SupplierCode',
            'category_id__name': 'CategoryName',
            'category_id__category_code': 'CategoryCode'
        }
        
        self.supplier_mapped_columns = {
            'supplier_id': 'SupplierID',
            'name': 'SupplierName',
            'mobile_number': 'SupplierMobile',
            'email_id': 'SupplierEmail',
            'supplier_code': 'SupplierCode',
            'gst_number': 'SupplierGST',
            'id_number': 'SupplierIDNumber',
            'id_type': 'SupplierIDType',
            'is_active': 'SupplierActiveStatus',
            'created_date_time': 'SupplierCreatedTime',
            'photo_url': 'SupplierPhotoURL',
            'id_proof_url': 'SupplierIDProofURL'
        }
        
        self.customer_mapped_columns = {
            'customer_id': 'CustomerID',
            'name': 'CustomerName',
            'mobile_number': 'CustomerMobile',
            'email_id': 'CustomerEmail',
            'customer_code': 'CustomerCode',
            'date_of_birth': 'CustomerDOB',
            'gender': 'CustomerGender',
            'martial_status': 'CustomerMaritalStatus',
            'religion': 'CustomerReligion',
            'blood_group': 'CustomerBloodGroup',
            'education': 'CustomerEducation',
            'occupation': 'CustomerOccupation',
            'is_active': 'CustomerActiveStatus',
            'created_date_time': 'CustomerCreatedTime',
            'photo_url': 'CustomerPhotoURL',
            'id_proof_url': 'CustomerIDProofURL'
        }

    def mapper(self, data: list, model_type: str) -> list | None | str:
        if len(data) == 0:
            return '[]'
        
        dataframe = pandas.DataFrame.from_records(data)
        
        # Select the appropriate mapping based on model_type
        if model_type == 'item':
            mapped_columns = self.item_mapped_columns
        elif model_type == 'supplier':
            mapped_columns = self.supplier_mapped_columns
        elif model_type == 'customer':
            mapped_columns = self.customer_mapped_columns
        else:
            return '[]'  # Return empty if model type is incorrect
        
        dataframe.rename(columns=mapped_columns, inplace=True)
        
        # Format date fields if applicable
        date_fields = ['ItemCreatedTime', 'SupplierCreatedTime', 'CustomerCreatedTime']
        for field in date_fields:
            if field in dataframe.columns:
                dataframe[field] = pandas.to_datetime(dataframe[field])
                dataframe[field] = dataframe[field].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # If no specific columns are required, return full data
        if len(self.columns_required) == 0:
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=mapped_columns,
                                      columns_required=self.columns_required)
        
        # Filter dataframe based on required columns
        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(model_type: str, key: str, value: str, organisation_name: str) -> None | dict:
        """
        The key can be 'item_id', 'supplier_id', or 'customer_id'.
        The value is the associated data with respect to the key.
        """
        data = None
        
        if model_type == 'item':
            data = Items.objects.filter(
                organisation_id__company_name=organisation_name, item_id=value
            ).first()
        elif model_type == 'supplier':
            data = Supplier.objects.filter(
                organisation_id__company_name=organisation_name, supplier_id=value
            ).first()
        elif model_type == 'customer':
            data = Customer.objects.filter(
                organisation_id__company_name=organisation_name, customer_id=value
            ).first()
        
        return data
