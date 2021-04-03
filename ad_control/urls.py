from django.urls import path
from .views import *

urlpatterns = [
    path('post-ad/', post_ad_view, name='post-ad'),
    path('<str:pk>', ad_detail_view, name='ad-detail'),
    path('confirm-order/<str:pk>', confirm_order_view, name='confirm-order'),
    path('checkout/', checkout_view, name='checkout'),
]
