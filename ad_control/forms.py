from django.forms import ModelForm
from django import forms
from .models import *


class PostAdForm(ModelForm):
    ADVERTISEMENT_TYPE_CHOICES = [
        ('', 'Advertisement Type'),
        ('Bill Board', 'Bill Board'),
        ('Vehicle', 'Vehicle'),
    ]
    PRICE_RATE_TYPE_CHOICES = [
        ('', 'Rate'),
        ('Day', 'Day'),
        ('Month', 'Month'),
    ]
    SIZE_SCALE_TYPE_CHOICES = [
        ('', 'Size Scale'),
        ('Inches', 'Inches'),
        ('Feet', 'Feet'),
        ('Meter', 'Meter'),
    ]

    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    price_rate = forms.CharField(widget=forms.Select(choices=PRICE_RATE_TYPE_CHOICES))
    size_scale = forms.CharField(widget=forms.Select(choices=SIZE_SCALE_TYPE_CHOICES))
    advertisement_type = forms.CharField(widget=forms.Select(choices=ADVERTISEMENT_TYPE_CHOICES))

    class Meta:
        model = AdvertiseModel
        fields = '__all__'
        exclude = ['advertiser', 'is_active']


class ConfirmOrderForm(ModelForm):
    PRICE_RATE_TYPE_CHOICES = [
        ('', 'Rate'),
        ('Day', 'Day'),
        ('Month', 'Month'),
    ]

    image = forms.ImageField(required=True, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    duration = forms.CharField(widget=forms.TextInput(attrs={'id': 'duration'}))
    price_rate = forms.CharField(widget=forms.Select(
        choices=PRICE_RATE_TYPE_CHOICES,
        attrs={'id': 'price_rate'}))

    class Meta:
        model = OrderModel
        fields = '__all__'
        exclude = ['customer', 'advertise', 'total_cost', 'is_approved', 'is_canceled', 'is_paid', 'is_running',
                   'is_complete']
