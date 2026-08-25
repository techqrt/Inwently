import json

import pandas
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.billing.dataclasses.request.create import BillingRequest
from biller_apps.billing.dataclasses.request.delete import BillingDeleteRequest
from biller_apps.billing.models.billing import Billing

from biller_apps.billing.serializers.request.get import BillingGetRequest
from biller_apps.billing.utils import BillingUtils
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.employees.models.employees import Employees
from biller_apps.item.models.items import Items
from biller_apps.shops.models import Shops


class BillingView:
    def __init__(self):
        self.data_created = "Bill added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Bill deleted successfully"
        self.data_no_match = "No matching bill number found"
        self.data_no_match_employee = "No matching employee found"
        self.data_no_match_shop = "No matching shop found"
        self.item_list_empty = "Given Item list is empty. Please add few items"
        self.data_match = "Bill already exists"

        super().__init__()

    def create_prepare_data(self, params: BillingRequest, organisation_name: str) -> pandas.DataFrame:
        dataframe = pandas.DataFrame.from_records(params.items)
        dataframe.dropna(inplace=True)
        if dataframe.shape[0] == 0:
            raise ValueError(self.item_list_empty)
        items = Items.get_with_item_list(organisation_name=organisation_name,
                                         item_code_list=list(dataframe['item_code'].unique()))
        items_dataframe = pandas.DataFrame.from_records(items)
        dataframe = pandas.merge(left=dataframe, right=items_dataframe, how='left', left_on='item_code',
                                 right_on='item_code')
        dataframe['created_at'] = timezone.now()
        return dataframe

    def create_validator(self, params: BillingRequest, token_payload: Payload) -> ValueError | tuple:
        employee = Employees.get_by_email(email=params.billed_by,
                                          organisation_name=token_payload.organisationName)
        if employee is None:
            raise ValueError(self.data_no_match_employee)
        shop = Shops.objects.filter(shop_code=params.shop_code).values('shop_id').first()
        if shop is None:
            raise ValueError(self.data_no_match_shop)
        # print("employee & shop:", employee, shop)
        return employee, shop

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: BillingRequest, token_payload: Payload) -> Response:
        employee, shop = self.create_validator(params=params, token_payload=token_payload)
        dataframe = self.create_prepare_data(params=params, organisation_name=token_payload.organisationName)
        with transaction.atomic():
            for index, value in dataframe.iterrows():
                Billing().create(created_at=value['created_at'],
                                 employee_id=employee['employee_id'], item_id=value['item_id'],
                                 organisation_id=employee['organisation_id_id'], shop_id=shop['shop_id'],
                                 quantity=value['quantity'], mrp_price=0.0)

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload) -> Response:
        from decimal import Decimal
        from django.db.models import Sum
        from biller_apps.billing.models.customer_bills import CustomerBills
        from biller_apps.pos.models import POS

        queryset = CustomerBills.objects.filter(
            organisation_id__company_name=token_payload.organisationName
        ).order_by('-created_at').values(
            'customer_bills_id', 'bill_number', 'created_at', 'discounts', 'discounts_unit', 'wave_off',
            'pos_id', 'shop_id__shop_code',
        )

        pages = Paginator(queryset, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        page_bills = list(pages.page(params.page_num))

        bill_numbers = [bill['bill_number'] for bill in page_bills]
        line_sums = {
            row['customer_billing_id__bill_number']: row['total_price']
            for row in Billing.objects.filter(customer_billing_id__bill_number__in=bill_numbers).values(
                'customer_billing_id__bill_number'
            ).annotate(total_price=Sum('total_price'))
        }

        pos_ids = [bill['pos_id'] for bill in page_bills if bill['pos_id']]
        pos_lookup = {
            row['pos_id']: row
            for row in POS.objects.filter(pos_id__in=pos_ids).values('pos_id', 'pos_code', 'customer__name')
        }

        result = []
        for bill in page_bills:
            subtotal = Decimal(str(line_sums.get(bill['bill_number'], 0)))
            discounts = Decimal(str(bill['discounts']))
            wave_off = Decimal(str(bill['wave_off']))
            if bill['discounts_unit'] == 'percentage':
                discount_amount = subtotal * (discounts / Decimal('100'))
            else:
                discount_amount = discounts
            total_price = subtotal - discount_amount - wave_off

            pos_info = pos_lookup.get(bill['pos_id'], {})
            result.append({
                'createdAt': bill['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                'billNumber': bill['bill_number'],
                'totalPrice': float(total_price.quantize(Decimal('0.01'))),
                'customerName': pos_info.get('customer__name'),
                'shopCode': bill['shop_id__shop_code'],
                'posCode': pos_info.get('pos_code'),
            })

        data = Utils.add_page_parameter(final_data=result, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK,
                        data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_extract(self, params: BillingGetRequest, token_payload: Payload):
        from decimal import Decimal
        from biller_apps.billing.models.customer_bills import CustomerBills

        customer_bills = CustomerBills.objects.filter(
            organisation_id__company_name=token_payload.organisationName, bill_number=params.bill_number
        ).values(
            'customer_bills_id', 'bill_number', 'created_at', 'discounts', 'discounts_unit', 'wave_off',
            'billed_by__employee_code', 'shop_id__shop_code',
        ).first()
        if not customer_bills:
            raise ValueError(self.data_no_match)

        items = list(Billing.objects.filter(
            customer_billing_id__bill_number=params.bill_number,
            customer_billing_id__organisation_id__company_name=token_payload.organisationName,
        ).values('item_id__item_code', 'item_id__name', 'quantity', 'total_price'))

        subtotal = sum((Decimal(str(item['total_price'])) for item in items), Decimal('0'))
        discounts = Decimal(str(customer_bills['discounts']))
        wave_off = Decimal(str(customer_bills['wave_off']))
        if customer_bills['discounts_unit'] == 'percentage':
            discount_amount = subtotal * (discounts / Decimal('100'))
        else:
            discount_amount = discounts
        amount = subtotal - discount_amount - wave_off

        data = {
            'customer_bills_id': customer_bills['customer_bills_id'],
            'bill_number': customer_bills['bill_number'],
            'shop_code': customer_bills['shop_id__shop_code'],
            'billed_by': customer_bills['billed_by__employee_code'],
            'discounts': str(discounts),
            'discounts_unit': customer_bills['discounts_unit'],
            'wave_off': str(wave_off),
            'amount': str(amount.quantize(Decimal('0.01'))),
            'created_at': customer_bills['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'items': [
                {
                    'item_code': item['item_id__item_code'],
                    'item_name': item['item_id__name'],
                    'quantity': item['quantity'],
                    'total_price': item['total_price'],
                } for item in items
            ],
        }
        return Response(status=status.HTTP_200_OK,
                        data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: BillingDeleteRequest, token_payload: Payload) -> Response:
        data = Billing.remove(organisation_name=token_payload.organisationName, bill_number=params.bill_number)
        return Response(status=status.HTTP_200_OK,
                        data=Utils.success_response_data(message=self.data_delete))
