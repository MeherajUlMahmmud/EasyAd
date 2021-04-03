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
    image = forms.ImageField(required=True, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    is_active = forms.BooleanField(initial=False)
    is_approved = forms.BooleanField(initial=False)
    is_running = forms.BooleanField(initial=False)

    class Meta:
        model = OrderModel
        fields = '__all__'
        exclude = ['customer', 'advertise', 'total_cost']
