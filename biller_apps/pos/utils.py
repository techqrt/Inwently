# biller_apps/pos/utils.py
from django.db import transaction
from django.db.models import Sum

from biller_apps.customer.models import Customer
from biller_apps.customer_quotation.models import CustomerQuotation
from biller_apps.customer_quotation.utils import CustomerQuotationUtils
from biller_apps.item.models.items import Items
from biller_apps.shops.models import Shops
from biller_apps.pos.models import POS, POSItem


class POSUtils:

    @staticmethod
    def _calculate_total(price, tax, discount, quantity):
        return (price + tax) * quantity - discount

    @staticmethod
    def _recalculate_amount(pos: POS) -> None:
        total = POSItem.objects.filter(pos_id=pos).aggregate(s=Sum('total'))['s'] or 0
        pos.amount = total
        pos.save(update_fields=['amount'])

    # =========================================================
    # CREATE — resolves customer_code / customer_quotation_code
    # =========================================================
    @staticmethod
    @transaction.atomic
    def create(customer_code, shop_code, organisation_id, organisation_name,
               items, billed_by=None, customer_quotation_code=None):

        # NOTE: assumes Customer has a `customer_code` field, mirroring
        # item_code/shop_code — confirm this against the real Customer model.
        customer = Customer.objects.filter(
            customer_code=customer_code, organisation_id_id=organisation_id
        ).first()
        if not customer:
            raise ValueError(f"Customer with customer_code '{customer_code}' does not exist.")

        shop = Shops.objects.filter(shop_code=shop_code, organisation_id_id=organisation_id).first()
        if not shop:
            raise ValueError(f"Shop with shop_code '{shop_code}' does not exist.")

        customer_quotation_id = None
        if customer_quotation_code:
            quotation = CustomerQuotation.objects.filter(
                customer_quotation_code=customer_quotation_code, organisation_id_id=organisation_id
            ).first()
            if not quotation:
                raise ValueError(
                    f"Customer quotation with code '{customer_quotation_code}' does not exist."
                )
            customer_quotation_id = quotation.customer_quotation_id

        resolved_items = []
        for entry in items:
            item = Items.objects.filter(
                item_code=entry.item_code, organisation_id_id=organisation_id
            ).first()
            if not item:
                raise ValueError(f"Item with item_code '{entry.item_code}' does not exist.")
            resolved_items.append((item, entry))

        pos = POS.objects.create(
            customer=customer,
            shop_id=shop,
            organisation_id_id=organisation_id,
            billed_by=billed_by,
            customer_quotation_id=customer_quotation_id,
        )
        pos.pos_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(pos.pos_id)
        pos.save()

        for item, entry in resolved_items:
            total = POSUtils._calculate_total(entry.price, entry.tax, entry.discount, entry.quantity)
            POSItem.objects.create(
                pos_id=pos, item_id=item, quantity=entry.quantity,
                price=entry.price, tax=entry.tax, discount=entry.discount, total=total,
            )

        POSUtils._recalculate_amount(pos)

        if customer_quotation_id:
            CustomerQuotationUtils.mark_converted(customer_quotation_id, organisation_id)

        return pos

    # =========================================================
    # UPDATE — partial replace of items + header fields
    # =========================================================
    @staticmethod
    @transaction.atomic
    def update(pos_id, organisation_id, items_to_add=None, items_to_update=None,
               items_to_remove=None, discounts=None, discounts_unit=None,
               wave_off=None, payment_type=None):
        items_to_add = items_to_add or []
        items_to_update = items_to_update or []
        items_to_remove = items_to_remove or []

        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status != POS.STATUS_DRAFT:
            raise ValueError(f"Cannot modify a POS in '{pos.status}' status.")

        if items_to_remove:
            deleted, _ = POSItem.objects.filter(
                pos_item_id__in=items_to_remove, pos_id=pos
            ).delete()
            if deleted != len(set(items_to_remove)):
                raise ValueError("One or more items_to_remove were not found on this POS.")

        for entry in items_to_update:
            pos_item = POSItem.objects.filter(pos_item_id=entry.pos_item_id, pos_id=pos).first()
            if not pos_item:
                raise ValueError(f"POS item '{entry.pos_item_id}' not found on this POS.")

            if entry.quantity is not None:
                pos_item.quantity = entry.quantity
            if entry.price is not None:
                pos_item.price = entry.price
            if entry.tax is not None:
                pos_item.tax = entry.tax
            if entry.discount is not None:
                pos_item.discount = entry.discount

            pos_item.total = POSUtils._calculate_total(
                pos_item.price, pos_item.tax, pos_item.discount, pos_item.quantity
            )
            pos_item.save()

        for entry in items_to_add:
            item = Items.objects.filter(
                item_code=entry.item_code, organisation_id_id=organisation_id
            ).first()
            if not item:
                raise ValueError(f"Item with item_code '{entry.item_code}' does not exist.")

            total = POSUtils._calculate_total(entry.price, entry.tax, entry.discount, entry.quantity)
            POSItem.objects.create(
                pos_id=pos, item_id=item, quantity=entry.quantity,
                price=entry.price, tax=entry.tax, discount=entry.discount, total=total,
            )

        header_fields = []
        if discounts is not None:
            pos.discounts = discounts
            header_fields.append("discounts")
        if discounts_unit is not None:
            pos.discounts_unit = discounts_unit
            header_fields.append("discounts_unit")
        if wave_off is not None:
            pos.wave_off = wave_off
            header_fields.append("wave_off")
        if payment_type is not None:
            pos.payment_type = payment_type
            header_fields.append("payment_type")
        if header_fields:
            pos.save(update_fields=header_fields)

        if not POSItem.objects.filter(pos_id=pos).exists():
            raise ValueError("POS cannot end up with zero items after update.")

        POSUtils._recalculate_amount(pos)
        return pos

    # =========================================================
    # STATUS TRANSITIONS
    # =========================================================
    @staticmethod
    @transaction.atomic
    def send_to_customer(pos_id, organisation_id):
        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status != POS.STATUS_DRAFT:
            raise ValueError(f"Cannot send a POS in '{pos.status}' status.")
        if not POSItem.objects.filter(pos_id=pos).exists():
            raise ValueError("Cannot send an empty POS.")

        pos.status = POS.STATUS_SENT_TO_CUSTOMER
        pos.save(update_fields=["status"])
        return pos

    @staticmethod
    @transaction.atomic
    def confirm(pos_id, organisation_id):
        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status not in (POS.STATUS_DRAFT, POS.STATUS_SENT_TO_CUSTOMER):
            raise ValueError(f"Cannot confirm a POS in '{pos.status}' status.")
        if not POSItem.objects.filter(pos_id=pos).exists():
            raise ValueError("Cannot confirm an empty POS.")

        pos.status = POS.STATUS_CONFIRMED
        pos.save(update_fields=["status"])
        return pos

    @staticmethod
    @transaction.atomic
    def cancel(pos_id, organisation_id):
        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status == POS.STATUS_EXECUTED:
            raise ValueError("Cannot cancel a POS that has already been executed to an invoice.")

        pos.status = POS.STATUS_CANCELLED
        pos.save(update_fields=["status"])
        return pos

    # =========================================================
    # EXECUTE — final invoice step, checks + deducts inventory
    # =========================================================
    @staticmethod
    @transaction.atomic
    def execute_to_billing(pos_id, organisation_id, organisation_name, billed_by_id=None):
        from biller_apps.billing.models.customer_bills import CustomerBills
        from biller_apps.billing.models.billing import Billing
        from biller_apps.inventory.models import Inventory

        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status == POS.STATUS_EXECUTED:
            raise ValueError("POS has already been executed to an invoice.")
        if pos.status != POS.STATUS_CONFIRMED:
            raise ValueError("POS must be confirmed before it can be executed to an invoice.")

        pos_items = list(POSItem.objects.filter(pos_id=pos))
        if not pos_items:
            raise ValueError("Cannot execute an empty POS.")

        inventory_rows = {}
        for pos_item in pos_items:
            inventory = Inventory.objects.filter(
                item_id=pos_item.item_id, shop_id=pos.shop_id, organisation_id_id=organisation_id
            ).first()
            if not inventory or inventory.balance_qty < pos_item.quantity:
                available = inventory.balance_qty if inventory else 0
                raise ValueError(
                    f"Insufficient stock for item code '{pos_item.item_id.item_code}': "
                    f"have {available}, need {pos_item.quantity}."
                )
            inventory_rows[pos_item.pos_item_id] = inventory

        customer_bills = CustomerBills.objects.create(
            organisation_id_id=organisation_id,
            shop_id=pos.shop_id,
            billed_by_id=billed_by_id or pos.billed_by_id,
            discounts=pos.discounts,
            discounts_unit=pos.discounts_unit,
            wave_off=pos.wave_off,
            pos_id=pos.pos_id,
        )
        customer_bills.bill_number = (
            ''.join([i[0] for i in organisation_name.split()]) + '_INV_' + str(customer_bills.customer_bills_id)
        )
        customer_bills.save()

        for pos_item in pos_items:
            Billing.objects.create(
                customer_billing_id=customer_bills,
                item_id=pos_item.item_id,
                quantity=pos_item.quantity,
                total_price=pos_item.total,
            )
            inventory = inventory_rows[pos_item.pos_item_id]
            inventory.balance_qty -= pos_item.quantity
            inventory.save(update_fields=["balance_qty"])

        pos.status = POS.STATUS_EXECUTED
        pos.save(update_fields=["status"])
        return customer_bills

    # =========================================================
    # GET / GET ALL / DELETE
    # =========================================================
    @staticmethod
    def get(organisation_id, pos_id=None, pos_code=None):
        if not pos_id and not pos_code:
            raise ValueError("Either pos_id or pos_code is required.")
        filters = {"organisation_id_id": organisation_id}
        filters["pos_id" if pos_id else "pos_code"] = pos_id or pos_code

        pos = POS.objects.filter(**filters).first()
        if not pos:
            raise ValueError("POS not found.")

        items = list(POSItem.objects.filter(pos_id=pos).values(
            "pos_item_id", "item_id__item_code", "item_id__name",
            "quantity", "price", "tax", "discount", "total",
        ))
        return pos, items

    @staticmethod
    def get_all(organisation_id, status=None, ordering="-created_date"):
        queryset = POS.objects.filter(organisation_id_id=organisation_id)
        if status:
            queryset = queryset.filter(status=status)
        queryset = queryset.order_by(ordering)
        return queryset.values(
            "pos_id", "pos_code", "customer__name", "shop_id__shop_code",
            "payment_type", "payment_status", "amount", "status",
            "customer_quotation_id", "created_date",
        )

    @staticmethod
    @transaction.atomic
    def delete(pos_id, organisation_id):
        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status == POS.STATUS_EXECUTED:
            raise ValueError("Cannot delete a POS that has already been executed to an invoice.")
        pos.delete()
        return True