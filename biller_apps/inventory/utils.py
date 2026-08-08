import pandas

from biller_apps.common.common import Common
from biller_apps.inventory.models import Inventory

from django.db import transaction
from biller_apps.item.models.items import Items
from biller_apps.shops.models import Shops


class InventoryUtils:
    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'inventory_id': 'inventoryId',
            'inventory_code': 'inventoryCode',
            'item_id__item_code': 'itemCode',
            'item_id__name': 'itemName',
            'item_id__description': 'description',
            'shop_id__shop_code': 'shopCode',
            'shop_id__name': 'shopName',
            'expiry_date': 'expiryDate',
            'price': 'price',
            'balance_qty': 'balanceQty',
            'organisation_id__company_name': 'organisationName',
            'created_time': 'createdTime',
            'store_mapping': 'storeMapping',
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)

        if 'createdTime' in dataframe.columns and (len(self.columns_required) == 0 or 'createdTime' in self.columns_required):
            dataframe['createdTime'] = pandas.to_datetime(dataframe['createdTime'])
            dataframe['createdTime'] = dataframe['createdTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        if 'expiryDate' in dataframe.columns and (len(self.columns_required) == 0 or 'expiryDate' in self.columns_required):
            dataframe['expiryDate'] = pandas.to_datetime(dataframe['expiryDate'], errors='coerce')
            dataframe['expiryDate'] = dataframe['expiryDate'].dt.strftime('%Y-%m-%d')
            # NaT (from a null expiry_date) becomes the string 'NaT' after strftime — normalize to None.
            dataframe['expiryDate'] = dataframe['expiryDate'].where(dataframe['expiryDate'] != 'NaT', None)

        if len(self.columns_required) == 0:
            return dataframe.to_json(orient='records')

        Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                   columns_required=self.columns_required)

        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def check_uniqueness(key: str, value: str, organisation_name: str) -> None | dict:
        """
        The key can be either 'sku' or 'item_name'.
        The value is the associated data with respect to the key.
        """
        data = None
        if key == 'item_name':
            data = Inventory.objects.filter(item_id__name=value, organisation_id__company_name=organisation_name).first()
        elif key == 'sku':
            data = Inventory.objects.filter(item_id__sku_code=value, organisation_id__company_name=organisation_name).first()

        return data

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def create(
        item_code,
        shop_code,
        organisation_id,
        organisation_name,
        expiry_date,
        price,
        balance_qty,
        store_mapping=""
    ):
        item = Items.objects.filter(
            item_code=item_code,
            organisation_id_id=organisation_id
        ).first()

        if not item:
            raise ValueError(f"Item with item_code '{item_code}' does not exist.")

        shop = Shops.objects.filter(
            shop_code=shop_code,
            organisation_id_id=organisation_id
        ).first()

        if not shop:
            raise ValueError(f"Shop with shop_code '{shop_code}' does not exist.")

        inventory_exists = Inventory.objects.filter(
            item_id=item,
            shop_id=shop,
            organisation_id_id=organisation_id
        ).exists()

        if inventory_exists:
            raise ValueError("Inventory already exists for this item and shop.")

        inventory = Inventory.objects.create(
            item_id=item,
            shop_id=shop,
            organisation_id_id=organisation_id,
            expiry_date=expiry_date,
            price=price,
            balance_qty=balance_qty,
            store_mapping=store_mapping,
        )

        inventory.inventory_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(inventory.inventory_id)
        inventory.save()

        return inventory

    # =========================================================
    # GET
    # =========================================================

    @staticmethod
    def get(organisation_id, inventory_id=None, inventory_code=None):
        if not inventory_id and not inventory_code:
            raise ValueError("Either inventory_id or inventory_code is required.")

        filters = {"organisation_id_id": organisation_id}
        if inventory_id:
            filters["inventory_id"] = inventory_id
        else:
            filters["inventory_code"] = inventory_code

        return Inventory.objects.filter(**filters).values(
            "inventory_id",
            "inventory_code",
            "item_id__item_code",
            "item_id__name",
            "item_id__description",
            "shop_id__shop_code",
            "shop_id__name",
            "expiry_date",
            "price",
            "balance_qty",
            "created_time",
            "store_mapping"
        ).first()

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all(
        organisation_id,
        shop_code=None,
        item_code=None,
        filter_key=None,
        filter_value=None,
        ordering="-created_time"
    ):
        """
        ordering: a Django order_by()-ready field string (e.g. '-item_id__name'), already
        resolved by the caller (InventoryGetAll dataclass is the single source of truth for
        translating sort_by/sort_order into this string).
        """
        queryset = Inventory.objects.filter(organisation_id_id=organisation_id)

        if shop_code:
            queryset = queryset.filter(shop_id__shop_code=shop_code)

        if item_code:
            queryset = queryset.filter(item_id__item_code=item_code)

        filter_mapping = {
            "item_code": "item_id__item_code",
            "item_name": "item_id__name",
            "shop_code": "shop_id__shop_code",
            "shop_name": "shop_id__name",
            "store_mapping": "store_mapping",
            "price": "price",
            "balance_qty": "balance_qty",
        }

        if filter_key and filter_value:
            field = filter_mapping.get(filter_key)

            if not field:
                raise ValueError(f"Filtering by '{filter_key}' is not allowed.")

            queryset = queryset.filter(**{f"{field}__icontains": filter_value})

        queryset = queryset.order_by(ordering)

        return queryset.values(
            "inventory_id",
            "inventory_code",
            "item_id__item_code",
            "item_id__name",
            "item_id__description",
            "shop_id__shop_code",
            "shop_id__name",
            "expiry_date",
            "price",
            "balance_qty",
            "created_time",
            "store_mapping"
        )

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def update(
        inventory_id,
        organisation_id,
        item_code=None,
        shop_code=None,
        expiry_date=None,
        price=None,
        balance_qty=None,
        store_mapping=None
    ):
        inventory = Inventory.objects.filter(
            inventory_id=inventory_id,
            organisation_id_id=organisation_id
        ).first()

        if not inventory:
            raise ValueError("Inventory not found.")

        if item_code is not None:
            item = Items.objects.filter(
                item_code=item_code,
                organisation_id_id=organisation_id
            ).first()

            if not item:
                raise ValueError(f"Item with item_code '{item_code}' does not exist.")

            inventory.item_id = item

        if shop_code is not None:
            shop = Shops.objects.filter(
                shop_code=shop_code,
                organisation_id_id=organisation_id
            ).first()

            if not shop:
                raise ValueError(f"Shop with shop_code '{shop_code}' does not exist.")

            inventory.shop_id = shop

        if expiry_date is not None:
            inventory.expiry_date = expiry_date

        if price is not None:
            inventory.price = price

        if balance_qty is not None:
            inventory.balance_qty = balance_qty

        if store_mapping is not None:
            inventory.store_mapping = store_mapping

        duplicate = Inventory.objects.filter(
            item_id=inventory.item_id,
            shop_id=inventory.shop_id,
            organisation_id_id=organisation_id
        ).exclude(inventory_id=inventory_id).exists()

        if duplicate:
            raise ValueError("Inventory already exists for this item and shop.")

        inventory.save()

        return inventory

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def delete(inventory_id, organisation_id):
        inventory = Inventory.objects.filter(
            inventory_id=inventory_id,
            organisation_id_id=organisation_id
        ).first()

        if not inventory:
            raise ValueError("Inventory not found.")

        inventory.delete()

        return True