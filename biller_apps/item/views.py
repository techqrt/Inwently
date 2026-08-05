import json
from dataclasses import asdict

import pandas
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.item.dataclasses.request.bulk_create import BulkItemRequest
from biller_apps.item.dataclasses.request.create import ItemRequest
from biller_apps.item.dataclasses.request.delete_many import ItemDeleteManyRequest
from biller_apps.item.dataclasses.request.delete import ItemDelete
from biller_apps.item.dataclasses.request.get import ItemGet
from biller_apps.item.dataclasses.response.create import ItemCreateResponse
from biller_apps.item.es_query import ItemEsQuery
from biller_apps.item.models.items import Items
from biller_apps.item.serializers.request.update import ItemUpdate
from biller_apps.item.utils import ItemUtils
from biller_apps.organisation.models import Organisation
from biller_apps.supplier.models import Supplier
from biller_apps.taxes.models import Taxes


class ItemView:
    def __init__(self) -> None:
        super().__init__()
        self.data_create = "Item added successfully"
        self.data_no_match_shop = "No matching shop found"
        self.data_no_match_org = "No matching organisation found"
        self.data_no_match_brand = "No matching brand found"
        self.data_no_match_category = "No matching category found"
        self.data_no_match_supplier = "No matching supplier found"
        self.data_no_match_item = "No matching item found"
        self.data_update = "Item updated successfully"
        self.data_update_version = "Item version updated successfully"
        self.data_delete = "Item deleted successfully"
        self.delete_error = "No matching data(organisation_name/Item_name) found"
        self.data_delete_only_one = "Item Version cannot be deleted as it has only 1 version"
        self.data_delete_version = "Item Version deleted successfully"
        self.data_item_not_found = "Item version not found"
        self.data_get = "Data fetched successfully"
        self.data_no_match = "No matching supplier found"

    def parse_csv(self, csv_file):
        # Read the CSV file into a DataFrame
        decoded_file = csv_file.read().decode('utf-8')
        df = pandas.read_csv(pandas.compat.StringIO(decoded_file))

        # Convert the DataFrame rows to a list of ItemRequest instances
        df['created_time'] = pandas.to_datetime(df['created_time'], errors='coerce').fillna(timezone.now())
        df['bar_qr_auto'] = df['bar_qr_auto'].str.lower() == 'true'

        items = [
            ItemRequest(
                name=row['name'] or '',
                description=row['description'] or '',
                bar_qr_code=row['bar_qr_code'] or '',
                bar_qr_auto=row['bar_qr_auto'],
                brand_code=row['brand_code'] or '',
                category_code=row['category_code'] or '',
                supplier_code=row['supplier_code'] or '',
                created_time=row['created_time'],
                item_image_url=row['item_image_url'] or '',
            ) for index, row in df.iterrows()
        ]

        return items

    def key_checks(self, params: ItemRequest | ItemUpdate, token_payload: Payload):
        
        organisation = Organisation.objects.filter(company_name=token_payload.organisationName).values(
            'organisation_id').first()
        if organisation is None:
            raise ValueError(self.data_no_match_org)
        brand = Brand.objects.filter(brand_code=params.brand_code).values('brand_id').first()
        if brand is None:
            raise ValueError(self.data_no_match_brand)
        category = Category.objects.filter(category_code=params.category_code).values('category_id').first()
        if category is None:
            raise ValueError(self.data_no_match_category)
        supplier = Supplier.objects.filter(supplier_code=params.supplier_code).values('supplier_id').first()
       
        if supplier is None:
            raise ValueError(self.data_no_match_supplier)
        
        #tax_code = Taxes.get(organisation_name=token_payload.organisationName, tax_code=params.tax_code)
        if params.tax_code:
            tax_code = Taxes.get(
              organisation_name=token_payload.organisationName,
              tax_code=params.tax_code
            )

            if tax_code is None:
                raise ValueError("No matching tax found")
        else:
            tax_code = None
        
        
        return organisation, brand, category, supplier, tax_code

    @Common().exception_handler
    @Publish.status_update
    def bulk_create_extract(self, params: BulkItemRequest, token_payload: Payload):

        items = self.parse_csv(params)
        created_items = []

        with transaction.atomic():
            for item in items:
                key_check = self.key_checks(params=item, token_payload=token_payload)
                organisation, brand, category, supplier, tax_code= key_check

                item_id, item_code = Items().create(
                    organisation_id=organisation['organisation_id'],
                    category_id=category['category_id'],
                    supplier_id=supplier['supplier_id'],
                    brand_id=brand['brand_id'],
                    name=item.name,
                    description=item.description,
                    created_time=item.created_time,
                    bar_qr_code=item.bar_qr_code,
                    organisation_name=token_payload.organisationName,
                    image_url=item.item_image_url,
                    hsn_code=item.hsn_code,
                    tax_id=tax_code['tax_id'] if tax_code else None,
                )
                created_items.append({'item_id': item_id, 'item_code': item_code})

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_create,
                                                                                    data=asdict(created_items)))

    @Common().exception_handler
    @Publish.status_update
    
    def create_extract(self, params: ItemRequest, token_payload: Payload):
        key_check = self.key_checks(params=params, token_payload=token_payload)
        organisation, brand, category, supplier, tax_code = key_check

        with transaction.atomic():
            item_id, item_code = Items().create(organisation_id=organisation['organisation_id'],
                                                category_id=category['category_id'],
                                                supplier_id=supplier['supplier_id'],
                                                brand_id=brand['brand_id'], name=params.name,
                                                description=params.description,
                                                bar_qr_code=params.bar_qr_code,
                                                organisation_name=token_payload.organisationName,
                                                image_url=params.image_url,
                                                tax_id=tax_code['tax_id'] if tax_code else None,
                                                hsn_code=params.hsn_code)
           # print("Item Created with ID:", item_id, "and Code:", item_code)
        data = ItemCreateResponse(itemCode=item_code,code=item_code)
                                   
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_create,
                                                                                    data=asdict(data)))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: ItemUpdate, token_payload: Payload):
        key_check = self.key_checks(params, token_payload=token_payload)
        organisation, brand, category, supplier,tax_code = key_check
        items = Items().get_with_code(item_code=params.item_code, organisation_name=token_payload.organisationName)
        if items is None:
            raise ValueError(self.data_no_match_item)

        Items().update(item_id=items['item_id'], category_id=category['category_id'],
                       supplier_id=supplier['supplier_id'],
                       brand_id=brand['brand_id'], name=params.name, description=params.description,
                       bar_qr_code=params.bar_qr_code, image_url=params.image_url,hsn_code=params.hsn_code,tax_id=tax_code['tax_id'] if tax_code else None,)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: ItemDelete, token_payload: Payload):
        item = Items().get_with_code(item_code=params.item_code, organisation_name=token_payload.organisationName)
        if item is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Items().remove(item_id=item['item_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(Items.get_all(organisation_name=token_payload.organisationName,params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        items = pages.page(params.page_num)
        inventory_utils = ItemUtils(columns_required=params.values_list)
        data = json.loads(inventory_utils.mapper(data=items))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK,
                        data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data  = ItemEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(status=status.HTTP_200_OK,data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: ItemDeleteManyRequest, token_payload: Payload):
        item = Items.get_with_code_list(item_code=params.item_code, organisation_name=token_payload.organisationName)
        if len(item) != len(params.item_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(item)
        item_ids = dataframe['item_id'].tolist()
        with transaction.atomic():
            Items.remove_from_list(item_ids=item_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def get_extract(self, params: ItemGet, token_payload: Payload):
        items = Items.get(organisation_name=token_payload.organisationName, item_code=params.item_code)
        if len(items) == 0:
            raise ValueError(self.data_no_match)
        inventory_utils = ItemUtils(columns_required=params.values_list)
        data = json.loads(inventory_utils.mapper(data=items))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
