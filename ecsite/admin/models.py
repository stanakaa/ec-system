from django.db import models


class Admin(models.Model):

    class Meta:
        db_table = "administrator_admin"

    admin_id = models.CharField(verbose_name="管理者ID", max_length=128, primary_key=True, db_index=True)
    password = models.CharField(verbose_name="パスワード", max_length=256)

    def __str__(self):
        return self.admin_id
