from django.db import models


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=100, default=None, null=True)
    country = models.CharField(max_length=100, default=None, null=True)
    street = models.CharField(max_length=100, default=None, null=True)

    class Meta:
        db_table = 'address'

    def create(self, state: str, country: str, street: str):
        self.state = state
        self.country = country
        self.street = street
        self.save()
        return self.address_id

    @staticmethod
    def update(state: str, country: str, street: str, address_id: int):
        address = Address.objects.get(address_id=address_id)
        address.state = state
        address.country = country
        address.street = street 
        address.save()
        return address.address_id

    @staticmethod
    def remove(address_id: int):
        Address.objects.get(address_id=address_id).delete()

    @staticmethod
    def remove_from_list(address_id: list) -> None:
        Address.objects.filter(address_id__in=address_id).delete()
