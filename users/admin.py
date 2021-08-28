from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Credentials",
            {
                "fields": [
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password",
                ]
            },
        ),
        (
            "Miscellaneous",
            {"fields": ["is_active", "email_confirmed"]},
        ),
        (
            "Permissions",
            {
                "fields": [
                    "is_staff",
                    "is_superuser",
                    "is_admin",
                ]
            },
        ),
    ]

    list_display = ("email", "username", "first_name", "last_name", "last_login")
    list_filter = ["last_login"]

    search_fields = ["email", "username", "first_name", "last_name"]


admin.site.register(User, UserAdmin)
