from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from biller.constants import Constants
from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees


class Signals:
    pass

    @staticmethod
    @receiver(pre_delete, sender=EmployeeCredentials)
    def prevent_delete(sender, instance: EmployeeCredentials, **kwargs):
        if instance.secure:
            raise Exception(Constants.delete_not_allowed)

    @staticmethod
    @receiver(pre_save, sender=EmployeeCredentials)
    def prevent_update(sender, instance: EmployeeCredentials, **kwargs):
        if instance.secure:
            if instance.employee_credentials_id is not None:
                raise Exception(Constants.update_not_allowed)

    @staticmethod
    @receiver(pre_delete, sender=Employees)
    def prevent_delete(sender, instance: Employees, **kwargs):
        if instance.secure:
            raise Exception(Constants.delete_not_allowed)

    @staticmethod
    @receiver(pre_delete, sender=Category)
    def prevent_delete(sender, instance: Category, **kwargs):
        if instance.secure:
            raise Exception(Constants.delete_not_allowed)

    @staticmethod
    @receiver(pre_save, sender=Category)
    def prevent_update(sender, instance: Category, **kwargs):
        if instance.secure:
            if instance.category_id is not None:
                raise Exception(Constants.update_not_allowed)

    @staticmethod
    @receiver(pre_delete, sender=Brand)
    def prevent_delete(sender, instance: Brand, **kwargs):
        if instance.secure:
            raise Exception(Constants.delete_not_allowed)

    @staticmethod
    @receiver(pre_save, sender=Brand)
    def prevent_update(sender, instance: Brand, **kwargs):
        if instance.secure:
            if instance.brand_id is not None:
                raise Exception(Constants.update_not_allowed)
