from django.contrib import admin
from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


# localhost/admin/　で管理者画面に入れるよ