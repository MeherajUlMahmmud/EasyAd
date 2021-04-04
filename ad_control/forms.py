from django.forms import ModelForm
from django import forms
from .models import *


class PostAdForm(ModelForm):
    image = forms.ImageField(required=True, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    is_active = forms.BooleanField(initial=True)

    class Meta:
        model = AdvertiseModel
        fields = '__all__'
        exclude = ['user']


class ConfirmOrderForm(ModelForm):
    PRICE_RATE_TYPE_CHOICES = [
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
        exclude = ['customer', 'advertise', 'total_cost', 'is_approved', 'is_paid', 'is_running', 'is_complete']
