from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'last_login', 'is_admin', 'is_advertiser', 'is_customer')
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    ordering = ('email',)
    # list_filter = ()
    fieldsets = ()
    list_filter = ('is_admin', 'is_active', 'is_advertiser', 'is_customer')
    # fieldsets = (
    #     (None, {'fields': ('email', 'password', 'date_joined', 'last_login', )}),
    #     ('Info', {'fields': ('name',)}),
    #     ('Permissions', {'fields': ('is_admin', 'is_applicant' 'is_company')}),
    # )


class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


admin.site.register(User, AccountAdmin)
admin.site.register(AdvertiserModel, AdvertiserAdmin)
admin.site.register(CustomerModel, CustomerAdmin)
admin.site.register(FeedbackModel)
