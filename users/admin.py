from django.contrib import admin

from users.models import UserModel

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
