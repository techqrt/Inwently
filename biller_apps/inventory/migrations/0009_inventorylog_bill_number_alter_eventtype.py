# Generated manually — additive, nullable field + choices update for InventoryLog

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_inventorylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorylog',
            name='bill_number',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventorylog',
            name='eventtype',
            field=models.CharField(choices=[('CREATE', 'Create'), ('UPDATE', 'Update'), ('BULK_CREATE', 'Bulk Create'), ('BULK_UPDATE', 'Bulk Update'), ('SALE_DEDUCT', 'Sale Deduct')], max_length=20),
        ),
    ]
