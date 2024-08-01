from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["img_url"]}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["img_url"]}),)

admin.site.register(User, UserAdmin)
