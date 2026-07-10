from argon2 import PasswordHasher
from django.db import models


class EmployeeCredentials(models.Model):
    employee_credentials_id = models.AutoField(primary_key=True)
    email_id = models.EmailField(max_length=50, default='', unique=True)
    password = models.CharField(max_length=100, default='')
    secure = models.BooleanField(default=False)

    class Meta:
        db_table = 'employee_credentials'

    def create(self, email_id: str, password: str, secure: bool = False) -> int:
        hasher = PasswordHasher()
        passw = hasher.hash(password)
        self.email_id = email_id
        self.password = passw
        self.secure = secure
        self.save()
        return self.employee_credentials_id

    @staticmethod
    def update(employee_credentials_id: int, new_password: str) -> int:
        hasher = PasswordHasher()
        passw = hasher.hash(new_password)
        obj = EmployeeCredentials.objects.get(employee_credentials_id=employee_credentials_id)
        obj.password = passw
        obj.save()
        return obj.employee_credentials_id

    @staticmethod
    def remove(employee_credentials_id: int) -> None:
        EmployeeCredentials.objects.get(employee_credentials_id=employee_credentials_id).delete()

    @staticmethod
    def get(email_id: str, password: str) -> dict:
        return EmployeeCredentials.objects.filter(email_id=email_id, password=password).values(
            'employee_credentials_id').first()

    @staticmethod
    def get_with_email(email_id: str) -> dict:
        return EmployeeCredentials.objects.filter(email_id=email_id).values().first()

    @staticmethod
    def remove_from_list(employee_credentials_id: list) -> None:
        EmployeeCredentials.objects.filter(employee_credentials_id__in=employee_credentials_id).delete()

