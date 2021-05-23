from django.contrib import admin
from .models import *


class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('advertiser', 'location', 'height', 'width', 'price')
    search_fields = ('advertiser', 'location',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ('-date_posted',)
    fieldsets = ()
    list_filter = ('advertiser', 'location', 'height', 'width')


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('customer', 'is_approved', 'is_canceled', 'advertiser_paid_approval', 'customer_paid_approval',
                    'is_running', 'is_complete')
    search_fields = ('customer',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ('-date_created',)
    fieldsets = ()
    list_filter = ('customer', 'is_approved', 'is_canceled', 'advertiser_paid_approval', 'customer_paid_approval',
                   'is_running', 'is_complete')


# class OrderPaymentModelAdmin(admin.ModelAdmin):
#     list_display = ('user', 'location', 'height', 'width', 'price')
#     search_fields = ('user', 'location',)
#     readonly_fields = ()
#
#     filter_horizontal = ()
#     ordering = ('-date_posted',)
#     fieldsets = ()
#     list_filter = ('user', 'location', 'height', 'width')


admin.site.register(AdvertiseModel, AdvertiseAdmin)
admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderPaymentModel)
