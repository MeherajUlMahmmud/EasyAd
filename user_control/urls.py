from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home_view, name='home'),

    # user login, logout and registration url
    path('account/login', login_view, name='login'),
    path('account/logout', logout_view, name='logout'),
    path('account/advertiser-registration', advertiser_signup_view, name='advertiser-register'),
    path('account/customer-registration', customer_signup_view, name='customer-register'),

    # applicant and company feed url
    path('advertiser/advertiser-dashboard', advertiser_dashboard, name='advertiser-dashboard'),
    path('customer/customer-dashboard', customer_dashboard, name='customer-dashboard'),
    # path('advertiser/search-result', search_result, name='search-result'),

    # applicant profile, public profile and company profile url
    # path('advertiser/advertiser-profile/<str:pk>/', advertiser_profile, name='advertiser-profile'),
    # path('company/company-profile/<str:pk>/', company_profile, name='company-profile'),

    # advertiser and company profile edit url
    # path('advertiser/advertiser-edit-profile', advertiser_edit_profile, name='advertiser-edit-profile'),
    # path('company/company-edit-profile', company_edit_profile, name='company-edit-profile'),

    # utilities
    # path('confirm-email-password', authentication_view, name='authentication'),
    path('account-settings/', account_settings, name='settings'),
    path('about', about_view, name='about'),
    path('contact', contact_view, name='contact'),
    #
    # path('reset-password/',
    #      auth_views.PasswordResetView.as_view(template_name="user/password-reset.html"),
    #      name="reset-password"),
    # path('reset-password-sent/',
    #      auth_views.PasswordResetDoneView.as_view(template_name="user/password-reset-sent.html"),
    #      name="password_reset_done"),
    #
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name="user/password-reset-form.html"),
    #      name="password_reset_confirm"),
    #
    # path('reset-password-complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name="user/password-reset-done.html"),
    #      name="password_reset_complete"),
]
