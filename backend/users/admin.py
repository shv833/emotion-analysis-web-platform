from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone_number", "birthday", "avatar")}),
        ("Roles", {"fields": ("role",)}),
        ("Group Info", {"fields": ("group",)}),
        ("Parent Info", {"fields": ("parent_info",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                ),
            },
        ),
    )
    readonly_fields = ("date_joined", "last_login")
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


admin.site.register(User, CustomUserAdmin)
