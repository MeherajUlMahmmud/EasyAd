from django.db import models
from user_control.models import AdvertiserModel, CustomerModel


class AdvertiseModel(models.Model):
    ADVERTISEMENT_TYPE_CHOICES = [
        ('Bill Board', 'Bill Board'),
        ('Vehicle', 'Vehicle'),
    ]

    PRICE_RATE_TYPE_CHOICES = [
        ('Day', 'Day'),
        ('Month', 'Month'),
    ]

    SIZE_SCALE_TYPE_CHOICES = [
        ('Inches', 'Inches'),
        ('Feet', 'Feet'),
        ('Meter', 'Meter'),
    ]

    advertiser = models.ForeignKey(AdvertiserModel, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=255)
    facing = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rate = models.CharField(max_length=30, choices=PRICE_RATE_TYPE_CHOICES)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    size_scale = models.CharField(max_length=30, choices=SIZE_SCALE_TYPE_CHOICES)
    advertisement_type = models.CharField(max_length=30, choices=ADVERTISEMENT_TYPE_CHOICES)
    additional_note = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.location


class OrderModel(models.Model):
    PRICE_RATE_TYPE_CHOICES = [
        ('Day', 'Day'),
        ('Month', 'Month'),
    ]

    customer = models.ForeignKey(CustomerModel, null=True, blank=True, on_delete=models.CASCADE)
    advertise = models.ForeignKey(AdvertiseModel, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    duration = models.CharField(max_length=30)
    price_rate = models.CharField(max_length=30, choices=PRICE_RATE_TYPE_CHOICES)
    total_cost = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    additional_note = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    advertiser_paid_approval = models.BooleanField(default=False)
    customer_paid_approval = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


class OrderPaymentModel(models.Model):
    order = models.ForeignKey(OrderModel, null=True, blank=True, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
