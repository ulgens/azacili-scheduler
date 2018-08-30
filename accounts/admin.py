from django.contrib import admin

from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name")
    search_fields = ("username", "first_name", "last_name")
    autocomplete_fields = ("sections", )

    fieldsets = [
        (
            None,
            {"fields": ["username", "first_name", "last_name", "date_joined", "sections"]}
        ),
        (
            "Auth & Permissions",
            {"fields": ["password", "is_active", "is_staff", "is_superuser", "groups", "user_permissions"]}
        ),
    ]


admin.site.register(User, UserAdmin)
