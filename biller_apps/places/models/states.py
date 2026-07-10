from django.db import models


class States(models.Model):
    state_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, default='')
    states = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'states'

    @staticmethod
    def get_states(country: str) -> list:
        return States.objects.filter(country=country).values('states').order_by('states')
