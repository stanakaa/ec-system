from django.db import models
from django.core.validators import MinValueValidator


class User(models.Model):

    class Meta:
        db_table = "account_user"

    user_id = models.CharField(verbose_name="会員ID", max_length=128, primary_key=True, db_index=True)
    password = models.CharField(verbose_name="パスワード", max_length=256)
    name = models.CharField(verbose_name="名前", max_length=128)
    address = models.CharField(verbose_name="住所", max_length=256)

    def __str__(self):
        return self.name
    

class Admin(models.Model):

    class Meta:
        db_table = "administrator_admin"

    admin_id = models.CharField(verbose_name="管理者ID", max_length=128, primary_key=True, db_index=True)
    password = models.CharField(verbose_name="パスワード", max_length=256)

    def __str__(self):
        return self.admin_id