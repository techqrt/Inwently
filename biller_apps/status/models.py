from django.db import models


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=100, default='', unique=True)
    status = models.CharField(max_length=100)
    progress = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = 'status'

    @staticmethod
    def get(status_id):
        return Status.objects.filter(uuid=status_id).values('uuid', 'status', 'progress').first()
