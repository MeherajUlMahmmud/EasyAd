from django.contrib import admin
from .models import *


class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'height', 'width', 'price')
    search_fields = ('user', 'location',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ('-date_posted',)
    fieldsets = ()
    list_filter = ('user', 'location', 'height', 'width')


admin.site.register(AdvertiseModel, AdvertiseAdmin)
