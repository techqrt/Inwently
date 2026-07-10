from django.db import models


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'country'

    @staticmethod
    def get_country() -> list:
        return Country.objects.filter().values('country').order_by('country')
