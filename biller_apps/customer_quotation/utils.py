# biller_apps/customer_quotation/utils.py
from django.db import transaction  

from biller_apps.customer_quotation.models import CustomerQuotation, CustomerQuotationItem
from biller_apps.item.models.items import Items
from biller_apps.shops.models import Shops


class CustomerQuotationUtils:

    @staticmethod
    @transaction.atomic
    def create(customer_name, customer_phone, shop_code, items, organisation_id,
               organisation_name, customer_email=""):
        shop = Shops.objects.filter(shop_code=shop_code, organisation_id_id=organisation_id).first()
        if not shop:
            raise ValueError(f"Shop with shop_code '{shop_code}' does not exist.")

        # Resolve every item_code up front — fail before writing anything if any is bad.
        resolved_items = []
        for entry in items:
            item = Items.objects.filter(
                item_code=entry.item_code, organisation_id_id=organisation_id
            ).first()
            if not item:
                raise ValueError(f"Item with item_code '{entry.item_code}' does not exist.")
            resolved_items.append((item, entry.quantity))

        quotation = CustomerQuotation.objects.create(
            organisation_id_id=organisation_id,
            shop_id=shop,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
        )
        quotation.customer_quotation_code = (
            ''.join([i[0] for i in organisation_name.split()]) + '_' + str(quotation.customer_quotation_id)
        )
        quotation.save()

        for item, quantity in resolved_items:
            CustomerQuotationItem.objects.create(
                customer_quotation_id=quotation, item_id=item, quantity=quantity,
            )

        return quotation

    @staticmethod
    @transaction.atomic
    def review(customer_quotation_id, organisation_id, organisation_name, status, reviewed_by_id=None):
        quotation = CustomerQuotation.objects.filter(
            customer_quotation_id=customer_quotation_id, organisation_id_id=organisation_id
        ).first()
        if not quotation:
            raise ValueError("Customer quotation not found.")

        if quotation.status not in (CustomerQuotation.STATUS_PENDING,):
            raise ValueError(f"Cannot review a quotation in '{quotation.status}' status.")

        quotation.status = status
        if reviewed_by_id:
            quotation.reviewed_by_id = reviewed_by_id
        quotation.save(update_fields=["status", "reviewed_by"])

        pos = None
        if status == CustomerQuotation.STATUS_PHONE_CONFIRMED:
            pos = CustomerQuotationUtils._auto_create_proforma_invoice(
                quotation=quotation, organisation_id=organisation_id,
                organisation_name=organisation_name, billed_by=reviewed_by_id,
            )
        return quotation, pos

    @staticmethod
    def _auto_create_proforma_invoice(quotation, organisation_id, organisation_name, billed_by=None):
        """Called by review() the moment a quotation becomes phone_confirmed — builds
        a draft Proforma Invoice (POS) from the quotation's items, using the item
        master's own price/tax as a starting point for staff to adjust afterward."""
        from decimal import Decimal

        from biller_apps.customer.models import Customer
        from biller_apps.pos.dataclasses.request.update import POSItemAddEntry
        from biller_apps.pos.utils import POSUtils

        customer = Customer.objects.filter(
            mobile_number=quotation.customer_phone, organisation_id_id=organisation_id
        ).first()
        if not customer:
            raise ValueError(
                f"No customer profile found for phone '{quotation.customer_phone}'. "
                "Link or create the customer record before confirming this quotation."
            )

        items = []
        for line in CustomerQuotationItem.objects.filter(customer_quotation_id=quotation):
            item = line.item_id
            price = item.plain_price or Decimal('0')
            tax_amount = Decimal('0')
            if item.tax_code_id:
                tax_amount = (price * Decimal(str(item.tax_code.total_tax))) / Decimal('100')
            items.append(POSItemAddEntry(
                item_code=item.item_code, quantity=line.quantity,
                price=price, tax=tax_amount, discount=Decimal('0'),
            ))

        return POSUtils.create(
            customer_code=customer.customer_code,
            shop_code=quotation.shop_id.shop_code,
            organisation_id=organisation_id,
            organisation_name=organisation_name,
            items=items,
            billed_by=billed_by,
            customer_quotation_code=quotation.customer_quotation_code,
        )

    @staticmethod
    def get(organisation_id, customer_quotation_id=None, customer_quotation_code=None):
        filters = {"organisation_id_id": organisation_id}
        filters["customer_quotation_id" if customer_quotation_id else "customer_quotation_code"] = (
            customer_quotation_id or customer_quotation_code
        )
        quotation = CustomerQuotation.objects.filter(**filters).first()
        if not quotation:
            raise ValueError("Customer quotation not found.")

        items = list(CustomerQuotationItem.objects.filter(customer_quotation_id=quotation).values(
            "customer_quotation_item_id", "item_id__item_code", "item_id__name", "quantity",
        ))
        return quotation, items

    @staticmethod
    def get_all(organisation_id, status=None, ordering="-created_at"):
        queryset = CustomerQuotation.objects.filter(organisation_id_id=organisation_id)
        if status:
            queryset = queryset.filter(status=status)
        queryset = queryset.order_by(ordering)
        return queryset.values(
            "customer_quotation_id", "customer_quotation_code", "customer_name",
            "customer_phone", "customer_email", "status", "created_at",
        )

    @staticmethod
    def mark_converted(customer_quotation_id, organisation_id):
        """Called by POSUtils when a POS is created from this quotation."""
        CustomerQuotation.objects.filter(
            customer_quotation_id=customer_quotation_id, organisation_id_id=organisation_id
        ).update(status=CustomerQuotation.STATUS_CONVERTED)

    @staticmethod
    def revert_to_confirmed(customer_quotation_id, organisation_id):
        """Called by POSUtils when the POS created from this quotation is cancelled or
        deleted before execution, so the quotation doesn't stay stranded as 'converted'
        with no resulting sale — reopens it for a fresh POS to be created."""
        CustomerQuotation.objects.filter(
            customer_quotation_id=customer_quotation_id, organisation_id_id=organisation_id,
            status=CustomerQuotation.STATUS_CONVERTED,
        ).update(status=CustomerQuotation.STATUS_PHONE_CONFIRMED)