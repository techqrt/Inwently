from django.db import models



class AppTemplate(models.Model):
    pass

    class Meta:
        db_table = 'app_template'

    def create(self) -> int:
        pass

    @staticmethod
    def get() -> list:
        pass

    @staticmethod
    def remove() -> None:
        pass

    @staticmethod
    def update() -> None:
        pass


