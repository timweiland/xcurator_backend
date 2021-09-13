from django.contrib import admin
from rest_framework_simplejwt import token_blacklist
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from users.models import User


class NewOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, NewOutstandingTokenAdmin)


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
