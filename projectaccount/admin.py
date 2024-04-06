from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,PasswordRest


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "pk",
        "username",
        "phone",
        "date_joined",
        "last_login",
        "email",
        "is_admin",
        "is_active",
        "raw_password",
        "role",
    )
    search_fields = (
        "pk",
        "phone",
    )
    readonly_fields = ("pk", "date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


class PasswordRestAdmin(admin.ModelAdmin):
    list_display = ("id", "account","is_active","otp")
admin.site.register(PasswordRest, PasswordRestAdmin)

