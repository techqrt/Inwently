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
    def review(customer_quotation_id, organisation_id, status, reviewed_by_id=None):
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
        return quotation

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