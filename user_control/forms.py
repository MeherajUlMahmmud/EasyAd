from django import forms
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.forms import ModelForm

from .models import *


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Username or Password")


class AdvertiserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 character including numeric values',
    )
    is_advertiser = forms.BooleanField(initial=True)
    check = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "is_advertiser", "check")


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 character including numeric values',
    )
    is_customer = forms.BooleanField(initial=True)
    check = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "is_customer", "check")


class AdvertiserEditProfileForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = AdvertiserModel
        fields = '__all__'
        exclude = ['user']


class CustomerEditProfileForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = CustomerModel
        fields = '__all__'
        exclude = ['user']


class AccountInformationForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email')
