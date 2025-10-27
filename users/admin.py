from django.contrib import admin

from users.models import UserModel, Follow


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']


@admin.register(Follow)
class FollowModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'following', 'created_at']
