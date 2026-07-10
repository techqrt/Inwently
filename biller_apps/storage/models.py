from django.db import models
from django.utils import timezone


class Storage(models.Model):
    storage_id = models.AutoField(primary_key=True)
    file_url = models.CharField(default='', max_length=200)
    uploaded_datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'storage'

    def create(self, file_url: str) -> int:
        self.file_url = file_url
        self.save()
        return self.storage_id

    @staticmethod
    def remove(file_url: str):
        Storage.objects.filter(file_url=file_url).delete()
