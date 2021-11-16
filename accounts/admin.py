from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountAdmin(UserAdmin):
    model = Account
    list_display = ['username', 'email', 'is_active', 'date_joined', 'last_login']
    readonly_fields = ('date_joined', 'last_login',)
    filter_horizontal = ()
    list_filter = ('username', )
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
