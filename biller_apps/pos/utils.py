# biller_apps/pos/utils.py
from django.db import transaction
from django.db.models import Sum

from biller_apps.item.models.items import Items
from biller_apps.shops.models import Shops
from biller_apps.pos.models import POS, POSItem
from biller_apps.customer_quotation.utils import CustomerQuotationUtils


class POSUtils:

    @staticmethod
    def _calculate_total(price, tax, discount, quantity) -> "Decimal":
        return (price + tax) * quantity - discount

    @staticmethod
    def _recalculate_pos_amount(pos: POS) -> None:
        total = POSItem.objects.filter(pos_id=pos).aggregate(s=Sum('total'))['s'] or 0
        pos.amount = total
        pos.save(update_fields=['amount'])

    # =========================================================
    # CREATE (header only — empty cart)
    # =========================================================
    # biller_apps/pos/utils.py — revised create()
    @staticmethod
    @transaction.atomic
    def create(customer_id, shop_code, organisation_id, organisation_name,
               items, billed_by=None, customer_quotation_id=None):
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

        pos = POS.objects.create(
            customer_id=customer_id, shop_id=shop, organisation_id_id=organisation_id,
            billed_by=billed_by, customer_quotation_id=customer_quotation_id,
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
    # ADD ITEM
    # =========================================================
    @staticmethod
    @transaction.atomic
    def add_item(pos_id, organisation_id, item_code, quantity, price, tax=0, discount=0):
        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS draft not found.")
        if pos.is_executed:
            raise ValueError("Cannot modify a finalized POS.")

        item = Items.objects.filter(item_code=item_code, organisation_id_id=organisation_id).first()
        if not item:
            raise ValueError(f"Item with item_code '{item_code}' does not exist.")

        # Stock check only (no deduction) — per current design.
        from biller_apps.inventory.models import Inventory
        inventory = Inventory.objects.filter(
            item_id=item, shop_id=pos.shop_id, organisation_id_id=organisation_id
        ).first()
        if not inventory or inventory.balance_qty < quantity:
            available = inventory.balance_qty if inventory else 0
            raise ValueError(
                f"Insufficient stock for '{item_code}': have {available}, need {quantity}."
            )

        total = POSUtils._calculate_total(price, tax, discount, quantity)
        pos_item = POSItem.objects.create(
            pos_id=pos, item_id=item, quantity=quantity,
            price=price, tax=tax, discount=discount, total=total,
        )
        POSUtils._recalculate_pos_amount(pos)
        return pos_item

    # =========================================================
    # UPDATE ITEM
    # =========================================================
    @staticmethod
    @transaction.atomic
    def update_item(pos_item_id, organisation_id, quantity=None, price=None, tax=None, discount=None):
        pos_item = POSItem.objects.filter(
            pos_item_id=pos_item_id, pos_id__organisation_id_id=organisation_id
        ).first()
        if not pos_item:
            raise ValueError("POS item not found.")
        if pos_item.pos_id.is_executed:
            raise ValueError("Cannot modify a finalized POS.")

        if quantity is not None:
            pos_item.quantity = quantity
        if price is not None:
            pos_item.price = price
        if tax is not None:
            pos_item.tax = tax
        if discount is not None:
            pos_item.discount = discount

        pos_item.total = POSUtils._calculate_total(
            pos_item.price, pos_item.tax, pos_item.discount, pos_item.quantity
        )
        pos_item.save()
        POSUtils._recalculate_pos_amount(pos_item.pos_id)
        return pos_item

    # =========================================================
    # DELETE ITEM
    # =========================================================
    @staticmethod
    @transaction.atomic
    def delete_item(pos_item_id, organisation_id):
        pos_item = POSItem.objects.filter(
            pos_item_id=pos_item_id, pos_id__organisation_id_id=organisation_id
        ).first()
        if not pos_item:
            raise ValueError("POS item not found.")
        if pos_item.pos_id.is_executed:
            raise ValueError("Cannot modify a finalized POS.")

        pos = pos_item.pos_id
        pos_item.delete()
        POSUtils._recalculate_pos_amount(pos)
        return True

    # =========================================================
    # GET (one POS + its items)
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

    # =========================================================
    # GET ALL
    # =========================================================
    @staticmethod
    def get_all(organisation_id, is_executed=None, ordering="-created_date"):
        queryset = POS.objects.filter(organisation_id_id=organisation_id)
        if is_executed is not None:
            queryset = queryset.filter(is_executed=is_executed)
        queryset = queryset.order_by(ordering)
        return queryset.values(
            "pos_id", "pos_code", "customer__name", "shop_id__shop_code",
            "payment_type", "amount", "is_executed", "quotation_id", "created_date",
        )

    # =========================================================
    # DELETE (whole draft, only if not finalized)
    # =========================================================
    @staticmethod
    @transaction.atomic
    def delete(pos_id, organisation_id):
        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.is_executed:
            raise ValueError("Cannot delete a finalized POS.")
        pos.delete()  # cascades to POSItem via on_delete=CASCADE
        return True

    
    @staticmethod
    @transaction.atomic
    def execute_to_billing(pos_id, organisation_id, billed_by_id=None):
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

        # Re-check stock at the moment of deduction — not a re-validation of
        # POSItem data itself, just guards against drift since add_item time.
        inventory_rows = {}
        for pos_item in pos_items:
            inventory = Inventory.objects.filter(
                item_id=pos_item.item_id, shop_id=pos.shop_id, organisation_id_id=organisation_id
            ).first()
            if not inventory or inventory.balance_qty < pos_item.quantity:
                available = inventory.balance_qty if inventory else 0
                raise ValueError(
                    f"Insufficient stock for '{pos_item.item_id.item_code}': "
                    f"have {available}, need {pos_item.quantity}."
                )
            inventory_rows[pos_item.pos_item_id] = inventory

        # Create the invoice header
        customer_bills = CustomerBills.objects.create(
            organisation_id_id=organisation_id,
            shop_id=pos.shop_id,
            billed_by_id=billed_by_id or (pos.billed_by_id if pos.billed_by_id else None),
            discounts=pos.discounts,
            discounts_unit=pos.discounts_unit,
            wave_off=pos.wave_off,
            pos_id=pos.pos_id,
        )
        customer_bills.bill_number = (
            'INV_' + str(customer_bills.customer_bills_id)  # scheme still open — see note below
        )
        customer_bills.save()

        # Copy each POSItem into a Billing row, and deduct stock
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