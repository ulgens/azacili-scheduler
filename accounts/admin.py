from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User

# No imports should use content of this file
__all__ = ()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "first_name", "last_name", "date_joined")
    search_fields = ("username", "first_name", "last_name")
    ordering = ("-date_joined", )

    readonly_fields = ("date_joined", "last_login")
    autocomplete_fields = ("sections", )


    fieldsets = [
        (
            None, {
                "fields": [
                    "username",
                    "first_name",
                    "last_name",
                    "date_joined",
                    "last_login",
                    "sections",
                ]}
        ),
        (
            "Auth & Permissions", {
                "fields": [
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]}
        ),
    ]
