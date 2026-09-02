from django.db import migrations


def backfill_dispatch_permission(apps, schema_editor):
    Employees = apps.get_model('employees', 'Employees')
    DispatchPermission = apps.get_model('employees', 'DispatchPermission')

    for employee in Employees.objects.filter(dispatch_permission__isnull=True):
        permission = DispatchPermission.objects.create(dispatch=False)
        employee.dispatch_permission_id = permission.permission_id
        employee.save(update_fields=['dispatch_permission'])


def noop_reverse(apps, schema_editor):
    # Nothing to undo — leaving the backfilled rows in place on reverse is
    # harmless (same as any employee that genuinely has dispatch=False).
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_dispatchpermission_employees_dispatch_permission'),
    ]

    operations = [
        migrations.RunPython(backfill_dispatch_permission, noop_reverse),
    ]
