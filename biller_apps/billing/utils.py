import uuid

import pandas
from django.db import transaction
from django.db.models import F

from biller_apps.common.common import Common


class BillingUtils:

    # =========================================================
    # CREATE DIRECT — invoice created from scratch, no PI/quotation.
    # Inventory is deducted immediately (same atomic conditional-update +
    # InventoryLog(SALE_DEDUCT) shape as POSUtils.inventory_confirm), since a
    # direct invoice has no separate PI lifecycle to defer deduction through.
    # =========================================================
    @staticmethod
    @transaction.atomic
    def create_direct(customer_name, customer_phone, shop_code, organisation_id,
                       organisation_name, items, billed_by_id):
        from biller_apps.billing.models.billing import Billing
        from biller_apps.billing.models.customer_bills import CustomerBills
        from biller_apps.inventory.models import Inventory, InventoryLog
        from biller_apps.item.models.items import Items
        from biller_apps.shops.models import Shops

        shop = Shops.objects.filter(shop_code=shop_code, organisation_id_id=organisation_id).first()
        if not shop:
            raise ValueError(f"Shop with shop_code '{shop_code}' does not exist.")

        resolved_items = []
        for entry in items:
            item = Items.objects.filter(
                item_code=entry.item_code, organisation_id_id=organisation_id
            ).first()
            if not item:
                raise ValueError(f"Item with item_code '{entry.item_code}' does not exist.")
            resolved_items.append((item, entry))

        customer_bills = CustomerBills.objects.create(
            organisation_id_id=organisation_id,
            shop_id=shop,
            billed_by_id=billed_by_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
        )
        customer_bills.bill_number = (
            ''.join([i[0] for i in organisation_name.split()]) + '_INV_' + str(customer_bills.customer_bills_id)
        )
        customer_bills.save()

        batch_id = uuid.uuid4()
        for item, entry in resolved_items:
            updated = Inventory.objects.filter(
                item_id=item, shop_id=shop, organisation_id_id=organisation_id,
                balance_qty__gte=entry.quantity,
            ).update(balance_qty=F('balance_qty') - entry.quantity)

            if updated == 0:
                inventory = Inventory.objects.filter(
                    item_id=item, shop_id=shop, organisation_id_id=organisation_id
                ).first()
                available = inventory.balance_qty if inventory else 0
                raise ValueError(
                    f"Insufficient stock for item code '{item.item_code}': "
                    f"have {available}, need {entry.quantity}."
                )

            inventory = Inventory.objects.get(item_id=item, shop_id=shop, organisation_id_id=organisation_id)
            InventoryLog.objects.create(
                inventory_id=inventory,
                inventory_code=inventory.inventory_code,
                eventtype=InventoryLog.EVENT_SALE_DEDUCT,
                batch_id=batch_id,
                status=InventoryLog.STATUS_SUCCESS,
                bill_number=customer_bills.bill_number,
            )

            total = (entry.price + entry.tax) * entry.quantity - entry.discount
            Billing.objects.create(
                customer_billing_id=customer_bills, item_id=item,
                quantity=entry.quantity, total_price=total,
            )

        return customer_bills

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
