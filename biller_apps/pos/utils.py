# biller_apps/pos/utils.py
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from biller_apps.customer.models import Customer
from biller_apps.customer_quotation.models import CustomerQuotation
from biller_apps.customer_quotation.utils import CustomerQuotationUtils
from biller_apps.item.models.items import Items
from biller_apps.shops.models import Shops
from biller_apps.pos.models import POS, POSItem, POSDispatch


class POSUtils:

    @staticmethod
    def _calculate_total(price, tax, discount, quantity):
        return (price + tax) * quantity - discount

    @staticmethod
    def _recalculate_amount(pos: POS) -> None:
        subtotal = POSItem.objects.filter(pos_id=pos).aggregate(s=Sum('total'))['s'] or Decimal('0')
        discounts = Decimal(pos.discounts)
        wave_off = Decimal(pos.wave_off)
        if pos.discounts_unit == 'percentage':
            discount_amount = subtotal * (discounts / Decimal('100'))
        else:
            discount_amount = discounts
        pos.amount = subtotal - discount_amount - wave_off
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
            if quotation.status != CustomerQuotation.STATUS_PHONE_CONFIRMED:
                raise ValueError(
                    f"Customer quotation '{customer_quotation_code}' is in '{quotation.status}' "
                    f"status and cannot be converted to a Proforma Invoice."
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
            billed_by_id=billed_by,
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

        # Admin confirmation no longer generates the invoice directly — it hands the
        # PI off to the Inventory team's queue instead of executing immediately.
        pos.status = POS.STATUS_INVENTORY_PENDING
        pos.save(update_fields=["status"])
        return pos

    @staticmethod
    @transaction.atomic
    def inventory_confirm(pos_id, organisation_id, confirmed_by_id=None):
        import uuid

        from django.db.models import F

        from biller_apps.inventory.models import Inventory, InventoryLog

        pos = POS.objects.select_for_update().filter(
            pos_id=pos_id, organisation_id_id=organisation_id
        ).first()
        if not pos:
            raise ValueError("POS not found.")
        # STATUS_CONFIRMED accepted here too, as a bridge for PIs confirmed before this
        # workflow existed — they must still pass through inventory confirmation.
        if pos.status not in (POS.STATUS_INVENTORY_PENDING, POS.STATUS_CONFIRMED):
            raise ValueError(f"Cannot confirm inventory for a POS in '{pos.status}' status.")

        pos_items = list(POSItem.objects.filter(pos_id=pos))
        if not pos_items:
            raise ValueError("Cannot confirm inventory for an empty POS.")

        # This is the deduction step moved from execute_to_billing — same
        # InventoryLog(SALE_DEDUCT) semantics, now backed by an atomic
        # conditional update instead of a read-modify-write, so concurrent
        # confirmations can no longer race past the stock check together.
        batch_id = uuid.uuid4()
        for pos_item in pos_items:
            updated = Inventory.objects.filter(
                item_id=pos_item.item_id, shop_id=pos.shop_id, organisation_id_id=organisation_id,
                balance_qty__gte=pos_item.quantity,
            ).update(balance_qty=F('balance_qty') - pos_item.quantity)

            if updated == 0:
                inventory = Inventory.objects.filter(
                    item_id=pos_item.item_id, shop_id=pos.shop_id, organisation_id_id=organisation_id
                ).first()
                available = inventory.balance_qty if inventory else 0
                raise ValueError(
                    f"Insufficient stock for item code '{pos_item.item_id.item_code}': "
                    f"have {available}, need {pos_item.quantity}."
                )

            inventory = Inventory.objects.get(
                item_id=pos_item.item_id, shop_id=pos.shop_id, organisation_id_id=organisation_id
            )
            InventoryLog.objects.create(
                inventory_id=inventory,
                inventory_code=inventory.inventory_code,
                eventtype=InventoryLog.EVENT_SALE_DEDUCT,
                batch_id=batch_id,
                status=InventoryLog.STATUS_SUCCESS,
                bill_number=pos.pos_code,
            )

        pos.inventory_confirmed_by_id = confirmed_by_id
        pos.inventory_confirmed_at = timezone.now()
        pos.status = POS.STATUS_DISPATCH_PENDING
        pos.save(update_fields=["inventory_confirmed_by", "inventory_confirmed_at", "status"])
        return pos

    @staticmethod
    @transaction.atomic
    def dispatch_add_details(pos_id, organisation_id, logistics_company, logistics_charges, added_by_id=None):
        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status != POS.STATUS_DISPATCH_PENDING:
            raise ValueError(f"Cannot add dispatch details to a POS in '{pos.status}' status.")

        dispatch_details, _ = POSDispatch.objects.update_or_create(
            pos_id=pos,
            defaults={
                "logistics_company": logistics_company,
                "logistics_charges": logistics_charges,
                "added_by_id": added_by_id,
            },
        )
        return dispatch_details

    @staticmethod
    @transaction.atomic
    def dispatch_confirm(pos_id, organisation_id, confirmed_by_id=None):
        pos = POS.objects.select_for_update().filter(
            pos_id=pos_id, organisation_id_id=organisation_id
        ).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status != POS.STATUS_DISPATCH_PENDING:
            raise ValueError(f"Cannot confirm dispatch for a POS in '{pos.status}' status.")

        dispatch_details = POSDispatch.objects.filter(pos_id=pos).first()
        if not dispatch_details or not dispatch_details.logistics_company:
            raise ValueError("Dispatch details must be added before dispatch can be confirmed.")

        pos.dispatch_confirmed_by_id = confirmed_by_id
        pos.dispatch_confirmed_at = timezone.now()
        pos.status = POS.STATUS_READY_FOR_EXECUTION
        pos.save(update_fields=["dispatch_confirmed_by", "dispatch_confirmed_at", "status"])
        return pos

    @staticmethod
    @transaction.atomic
    def cancel(pos_id, organisation_id):
        import uuid

        from django.db.models import F

        from biller_apps.inventory.models import Inventory, InventoryLog

        pos = POS.objects.select_for_update().filter(
            pos_id=pos_id, organisation_id_id=organisation_id
        ).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status == POS.STATUS_EXECUTED:
            raise ValueError("Cannot cancel a POS that has already been executed to an invoice.")
        if pos.status == POS.STATUS_CANCELLED:
            raise ValueError("POS is already cancelled.")

        # inventory_confirmed_at is only ever set once, at the point stock was
        # deducted (see inventory_confirm) — it's a more reliable "was stock
        # already taken?" signal than the current status string.
        if pos.inventory_confirmed_at is not None:
            pos_items = list(POSItem.objects.filter(pos_id=pos))
            batch_id = uuid.uuid4()
            for pos_item in pos_items:
                updated = Inventory.objects.filter(
                    item_id=pos_item.item_id, shop_id=pos.shop_id, organisation_id_id=organisation_id,
                ).update(balance_qty=F('balance_qty') + pos_item.quantity)

                if updated == 0:
                    InventoryLog.objects.create(
                        inventory_id=None,
                        inventory_code=None,
                        eventtype=InventoryLog.EVENT_SALE_REVERSAL,
                        batch_id=batch_id,
                        status=InventoryLog.STATUS_FAILED,
                        error_message=(
                            f"Inventory row for item code '{pos_item.item_id.item_code}' no longer exists; "
                            f"stock reversal for cancelled POS '{pos.pos_code}' could not be applied."
                        ),
                        bill_number=pos.pos_code,
                    )
                    continue

                inventory = Inventory.objects.get(
                    item_id=pos_item.item_id, shop_id=pos.shop_id, organisation_id_id=organisation_id
                )
                InventoryLog.objects.create(
                    inventory_id=inventory,
                    inventory_code=inventory.inventory_code,
                    eventtype=InventoryLog.EVENT_SALE_REVERSAL,
                    batch_id=batch_id,
                    status=InventoryLog.STATUS_SUCCESS,
                    bill_number=pos.pos_code,
                )

        pos.status = POS.STATUS_CANCELLED
        pos.save(update_fields=["status"])
        if pos.customer_quotation_id:
            CustomerQuotationUtils.revert_to_confirmed(pos.customer_quotation_id, organisation_id)
        return pos

    # =========================================================
    # EXECUTE — final invoice step. Inventory has already been checked
    # and deducted at inventory_confirm(); this step only generates the
    # final invoice from a PI that has completed the full workflow.
    # =========================================================
    @staticmethod
    @transaction.atomic
    def execute_to_billing(pos_id, organisation_id, organisation_name, billed_by_id=None):
        from biller_apps.billing.models.customer_bills import CustomerBills
        from biller_apps.billing.models.billing import Billing

        pos = POS.objects.filter(pos_id=pos_id, organisation_id_id=organisation_id).first()
        if not pos:
            raise ValueError("POS not found.")
        if pos.status == POS.STATUS_EXECUTED:
            raise ValueError("POS has already been executed to an invoice.")
        if pos.status != POS.STATUS_READY_FOR_EXECUTION:
            raise ValueError(
                "POS must complete inventory and dispatch confirmation before it can be executed to an invoice."
            )

        pos_items = list(POSItem.objects.filter(pos_id=pos))
        if not pos_items:
            raise ValueError("Cannot execute an empty POS.")

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

        pos.status = POS.STATUS_EXECUTED
        pos.save(update_fields=["status"])
        customer_bills.amount = pos.amount
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
        customer_quotation_id = pos.customer_quotation_id
        pos.delete()
        if customer_quotation_id:
            CustomerQuotationUtils.revert_to_confirmed(customer_quotation_id, organisation_id)
        return True