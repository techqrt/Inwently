import datetime
import urllib

from django.db import models
from django.db.models import Q
from django.utils import timezone

from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.organisation.models import Organisation
from biller_apps.supplier.models import Supplier
from biller_apps.taxes.models import Taxes


# item model
class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', unique=False)
    description = models.CharField(max_length=350, default='')
    code = models.CharField(max_length=100, default='', unique=True)
    hsn_code = models.CharField(max_length=100, null=True, blank=True, default=None)
    tax_code = models.ForeignKey(Taxes, on_delete=models.CASCADE, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=False)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)
    item_code = models.CharField(max_length=10, default='', unique=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, default=1)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=1)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    created_time = models.DateTimeField(default=timezone.now)
    image_url = models.TextField(default='', null=True)
    # Added Columns for No of Packets, SKU Code, Plain Price, Printed Price, and MOQ
    no_of_packets = models.IntegerField(default=1)
    sku_code = models.CharField(max_length=100, default='', null=True, blank=True)
    plain_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    printed_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    moq = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)

    class Meta:
        db_table = 'items'

    def create(self, name: str, description: str, organisation_name: str,
               bar_qr_code: str, organisation_id: int, brand_id: int, category_id: int, supplier_id: int,
               image_url: str, hsn_code: str, tax_id: int,
               no_of_packets: int = 1, sku_code: str = '', plain_price: float = 0.00,
               printed_price: float = 0.00, moq: float = 1.00,
               attributes: list | None = None, other_images: list | None = None):
        self.name = name
        self.description = description if description is not None else ''
        self.is_active = True
        self.organisation_id = Organisation.objects.get(organisation_id=organisation_id)
        self.brand_id = Brand.objects.get(brand_id=brand_id)
        self.category_id = Category.objects.get(category_id=category_id)
        self.supplier_id = Supplier.objects.get(supplier_id=supplier_id)
        self.created_time = timezone.now()
        self.image_url = image_url
        self.hsn_code = hsn_code if hsn_code else None
        if tax_id:
            self.tax_code = Taxes.objects.get(tax_id=tax_id)
        else:
            self.tax_code = None
        self.save()
        item_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.item_id)
        self.item_code = item_code
        if len(bar_qr_code) == 0:
            self.code = item_code
        else:
            self.code = bar_qr_code
        self.no_of_packets = no_of_packets
        self.sku_code = sku_code
        self.plain_price = plain_price
        self.printed_price = printed_price
        self.moq = moq
        self.save()

        if attributes:
            ItemAttribute.bulk_create(self, attributes)
        if other_images:
            ItemOtherImage.bulk_create(self, other_images)

        return self.item_id, self.code

    def update(self, item_id: int, name: str, description: str, bar_qr_code: str, brand_id: int, category_id: int,
               supplier_id: int, image_url: str, hsn_code: str, tax_id: int,
               no_of_packets: int = 1, sku_code: str = '', plain_price: float = 0.00,
               printed_price: float = 0.00, moq: float = 1.00,
               attributes: list | None = None, other_images: list | None = None):
        items = Items.objects.get(item_id=item_id)
        items.name = name
        items.description = description
        items.brand_id = Brand.objects.get(brand_id=brand_id)
        items.category_id = Category.objects.get(category_id=category_id)
        items.supplier_id = Supplier.objects.get(supplier_id=supplier_id)
        items.image_url = image_url
        items.hsn_code = hsn_code if hsn_code else None
        if tax_id:
            items.tax_code = Taxes.objects.get(tax_id=tax_id)
        else:
            items.tax_code = None
        if len(bar_qr_code) == 0:
            items.code = items.code
        else:
            items.code = bar_qr_code

        items.no_of_packets = no_of_packets
        items.sku_code = sku_code
        items.plain_price = plain_price
        items.printed_price = printed_price
        items.moq = moq

        # Replace child rows only if the caller actually passed new data,
        # so partial updates that don't touch attributes/images are untouched.
        if attributes is not None:
            ItemAttribute.objects.filter(item_id=items.item_id).delete()
            ItemAttribute.bulk_create(items, attributes)
        if other_images is not None:
            ItemOtherImage.objects.filter(item_id=items.item_id).delete()
            ItemOtherImage.bulk_create(items, other_images)

        items.save()
        return items.item_id

    @staticmethod
    def remove(item_id: int):
        ItemAttribute.objects.filter(item_id=item_id).delete()
        ItemOtherImage.objects.filter(item_id=item_id).delete()
        Items.objects.get(item_id=item_id).delete()

    @staticmethod
    def get(organisation_name: str, item_code: str = None, single: bool = False) -> list | dict:
        get_filter = Q(organisation_id__company_name=organisation_name)
        if item_code is not None:
            get_filter &= Q(item_code=item_code)

        fields = ('name', 'description', 'code', 'is_active', 'item_code',
                  'brand_id__brand_code', 'brand_id__name',
                  'category_id__name', 'category_id__category_code',
                  'supplier_id__name', 'supplier_id__supplier_code',
                  'image_url', 'item_id', 'hsn_code', 'tax_code_id__name', 'tax_code_id__tax_code',
                  'no_of_packets', 'sku_code', 'plain_price', 'printed_price', 'moq', 'created_time')

        if single:
            result = Items.objects.filter(get_filter).values(*fields).first()
            if result:
                result['attributes'] = ItemAttribute.get_all(result['item_id'])
                result['other_images'] = ItemOtherImage.get_all(result['item_id'])
            return result
        return Items.objects.filter(get_filter).values(*fields).order_by('name')

    @staticmethod
    def get_all(organisation_name: str, params: GetAll):
        filters = Q(organisation_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_key.lower() == 'is_active':
                filters = filters & Q(is_active=params.filter_value.lower() == 'true')
            else:
                filters = filters & Q(**{params.filter_key: params.filter_value})

        if len(params.search_key) > 0:
            filters = filters & Q(name__icontains=params.search_key)

        items = list(Items.objects.filter(filters).values(
            'item_id', 'name', 'description', 'code', 'is_active', 'item_code', 'brand_id__brand_code',
            'brand_id__name', 'category_id__name', 'category_id__category_code', 'supplier_id__name',
            'supplier_id__supplier_code', 'image_url', 'created_time',
            'no_of_packets', 'sku_code', 'plain_price', 'printed_price', 'moq').order_by(params.ordering))

        item_ids = [item['item_id'] for item in items]
        attributes_by_item = ItemAttribute.get_all_for_items(item_ids)
        other_images_by_item = ItemOtherImage.get_all_for_items(item_ids)
        for item in items:
            item['attributes'] = attributes_by_item.get(item['item_id'], [])
            item['other_images'] = other_images_by_item.get(item['item_id'], [])

        return items

    @staticmethod
    def get_with_item_list(organisation_name: str, item_code_list: list):
        return Items.objects.filter(item_code__in=item_code_list).values('item_code', 'itemversion__mrp_price',
                                                                          'item_id')

    @staticmethod
    def get_with_code(item_code: str, organisation_name: str) -> dict:
        return Items.objects.filter(item_code=item_code,
                                     organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'item_id').first()

    @staticmethod
    def get_with_code_list(item_code: list, organisation_name: str) -> list:
        return list(Items.objects.filter(item_code__in=item_code,
                                          organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'item_id'))

    @staticmethod
    def remove_from_list(item_ids: list) -> None:
        ItemAttribute.objects.filter(item_id__in=item_ids).delete()
        ItemOtherImage.objects.filter(item_id__in=item_ids).delete()
        Items.objects.filter(item_id__in=item_ids).delete()


# item attributes model
class ItemAttribute(models.Model):
    """One-to-many: an Item can have many attributes (e.g. Weight: 500 g, Length: 2 m)."""
    attribute_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='attributes')
    attribute_key = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)
    attribute_unit = models.CharField(max_length=50, default='', null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'item_attributes'

    @staticmethod
    def add(item: Items, attribute_key: str, attribute_value: str, attribute_unit: str = ''):
        attr = ItemAttribute(item_id=item, attribute_key=attribute_key,
                              attribute_value=attribute_value, attribute_unit=attribute_unit)
        attr.save()
        return attr.attribute_id

    @staticmethod
    def bulk_create(item: Items, attributes: list):
        """attributes: list of dicts like {'attribute_key': 'Weight', 'attribute_value': '500', 'attribute_unit': 'g'}"""
        objs = [
            ItemAttribute(item_id=item,
                           attribute_key=a.get('attribute_key', ''),
                           attribute_value=a.get('attribute_value', ''),
                           attribute_unit=a.get('attribute_unit', ''))
            for a in attributes
        ]
        ItemAttribute.objects.bulk_create(objs)

    @staticmethod
    def get_all(item_id: int) -> list:
        return list(ItemAttribute.objects.filter(item_id=item_id).values(
            'attribute_id', 'attribute_key', 'attribute_value', 'attribute_unit'))

    @staticmethod
    def get_all_for_items(item_ids: list) -> dict:
        """Returns {item_id: [{'attribute_id', 'attribute_key', 'attribute_value', 'attribute_unit'}, ...]}
        for every item_id in item_ids, in a single query — use this for list/paginated views
        instead of calling get_all() per item."""
        rows = ItemAttribute.objects.filter(item_id__in=item_ids).values(
            'item_id', 'attribute_id', 'attribute_key', 'attribute_value', 'attribute_unit')
        grouped = {}
        for row in rows:
            grouped.setdefault(row['item_id'], []).append({
                'attribute_id': row['attribute_id'],
                'attribute_key': row['attribute_key'],
                'attribute_value': row['attribute_value'],
                'attribute_unit': row['attribute_unit'],
            })
        return grouped

    @staticmethod
    def remove(attribute_id: int):
        ItemAttribute.objects.get(attribute_id=attribute_id).delete()


# item other images model
class ItemOtherImage(models.Model):
    """One-to-many: an Item can have many additional gallery images besides the primary image_url."""
    image_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='other_images')
    image_url = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'item_other_images'

    @staticmethod
    def add(item: Items, image_url: str):
        img = ItemOtherImage(item_id=item, image_url=image_url)
        img.save()
        return img.image_id

    @staticmethod
    def bulk_create(item: Items, image_urls: list):
        """image_urls: list of URL strings"""
        objs = [ItemOtherImage(item_id=item, image_url=url) for url in image_urls]
        ItemOtherImage.objects.bulk_create(objs)

    @staticmethod
    def get_all(item_id: int) -> list:
        return list(ItemOtherImage.objects.filter(item_id=item_id).values('image_id', 'image_url'))

    @staticmethod
    def get_all_for_items(item_ids: list) -> dict:
        """Returns {item_id: [{'image_id', 'image_url'}, ...]} for every item_id in item_ids,
        in a single query — use this for list/paginated views instead of calling get_all() per item."""
        rows = ItemOtherImage.objects.filter(item_id__in=item_ids).values('item_id', 'image_id', 'image_url')
        grouped = {}
        for row in rows:
            grouped.setdefault(row['item_id'], []).append({
                'image_id': row['image_id'],
                'image_url': row['image_url'],
            })
        return grouped

    @staticmethod
    def remove(image_id: int):
        ItemOtherImage.objects.get(image_id=image_id).delete()