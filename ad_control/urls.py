from django.urls import path
from .views import *

urlpatterns = [
    path('post-ad/', post_ad_view, name='post-ad'),
    path('update-ad/<str:pk>', update_ad_view, name='update-ad'),

    path('<str:pk>', ad_detail_view, name='ad-detail'),

    path('confirm-order/<str:pk>', confirm_order_view, name='confirm-order'),
    path('order-details/<str:pk>', order_details_view, name='order-details'),

    path('advertiser/unchecked-orders/', advertiser_unchecked_order_view, name='advertiser-unchecked-orders'),
    path('advertiser/unpaid-orders/', advertiser_unpaid_order_view, name='advertiser-unpaid-orders'),
    path('advertiser/ads-to-run/', advertiser_ads_to_run_view, name='advertiser-ads-to-run'),
    path('advertiser/running-ads/', advertiser_running_ads_view, name='advertiser-running-ads'),
    path('advertiser/finished-ads/', advertiser_finished_ads_view, name='advertiser-finished-ads'),

    path('customer/pending-orders/', customer_pending_order_view, name='customer-pending-orders'),
    path('customer/unpaid-orders/', customer_unpaid_order_view, name='customer-unpaid-orders'),
    path('customer/ads-to-run/', customer_ads_to_run_view, name='customer-ads-to-run'),
    path('customer/running-ads/', customer_running_ads_view, name='customer-running-ads'),
    path('customer/finished-ads/', customer_finished_ads_view, name='customer-finished-ads'),
]
