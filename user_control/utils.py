from ad_control.models import OrderModel, AdvertiseModel
from user_control.models import CustomerModel, AdvertiserModel


def get_pending_orders(request):
    pending_orders = []
    if request.user.is_authenticated and request.user.is_customer:
        customer = CustomerModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(customer=customer)
        order_list = list(order_queryset)
        pending_orders = [item for item in order_list
                          if item.customer.user == request.user
                          and not item.is_approved
                          and not item.is_canceled
                          and not item.advertiser_paid_approval
                          and not item.customer_paid_approval
                          and not item.is_running
                          and not item.is_complete]
    elif request.user.is_authenticated and request.user.is_advertiser:
        user = request.user
        advertiser = AdvertiserModel.objects.get(user=user)
        advertise_queryset = AdvertiseModel.objects.filter(advertiser=advertiser)
        advertise_list = list(advertise_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list if item.advertise in advertise_list]
        pending_orders = [item for item in final_order_list
                          if not item.is_approved
                          and not item.is_canceled
                          and not item.advertiser_paid_approval
                          and not item.customer_paid_approval
                          and not item.is_running
                          and not item.is_complete]

    return pending_orders


def get_unpaid_orders(request):
    unpaid_orders = []
    if request.user.is_authenticated and request.user.is_customer:
        customer = CustomerModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(customer=customer)
        order_list = list(order_queryset)
        unpaid_orders = [item for item in order_list
                         if item.customer.user == request.user
                         and item.is_approved
                         and not item.is_canceled
                         and not item.advertiser_paid_approval
                         and not item.is_running
                         and not item.is_complete]
    elif request.user.is_authenticated and request.user.is_advertiser:
        user = request.user
        advertiser = AdvertiserModel.objects.get(user=user)
        advertise_queryset = AdvertiseModel.objects.filter(advertiser=advertiser)
        advertise_list = list(advertise_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list
                            if item.advertise in advertise_list]
        unpaid_orders = [item for item in final_order_list
                         if item.is_approved
                         and not item.is_canceled
                         and not item.advertiser_paid_approval
                         and not item.is_running
                         and not item.is_complete]
    return unpaid_orders


def get_ads_to_run(request):
    ads_to_run = []
    if request.user.is_authenticated and request.user.is_customer:
        customer = CustomerModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(customer=customer)
        order_list = list(order_queryset)
        ads_to_run = [item for item in order_list
                      if item.customer.user == request.user
                      and item.is_approved
                      and not item.is_canceled
                      and item.advertiser_paid_approval
                      and item.customer_paid_approval
                      and not item.is_running
                      and not item.is_complete]
    elif request.user.is_authenticated and request.user.is_advertiser:
        user = request.user
        advertiser = AdvertiserModel.objects.get(user=user)
        advertise_queryset = AdvertiseModel.objects.filter(advertiser=advertiser)
        advertise_list = list(advertise_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list
                            if item.advertise in advertise_list]
        ads_to_run = [item for item in final_order_list
                      if item.is_approved
                      and not item.is_canceled
                      and item.advertiser_paid_approval
                      and item.customer_paid_approval
                      and not item.is_running
                      and not item.is_complete]
    return ads_to_run


def get_running_ads(request):
    running_ads = []
    if request.user.is_authenticated and request.user.is_customer:
        customer = CustomerModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(customer=customer)
        order_list = list(order_queryset)
        running_ads = [item for item in order_list
                       if item.customer.user == request.user
                       and item.is_approved
                       and not item.is_canceled
                       and item.advertiser_paid_approval
                       and item.customer_paid_approval
                       and item.is_running
                       and not item.is_complete]
    elif request.user.is_authenticated and request.user.is_advertiser:
        user = request.user
        advertiser = AdvertiserModel.objects.get(user=user)
        advertise_queryset = AdvertiseModel.objects.filter(advertiser=advertiser)
        advertise_list = list(advertise_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list
                            if item.advertise in advertise_list]
        running_ads = [item for item in final_order_list
                       if item.is_approved
                       and not item.is_canceled
                       and item.advertiser_paid_approval
                       and item.customer_paid_approval
                       and item.is_running
                       and not item.is_complete]
    return running_ads


def get_finished_ads(request):
    finished_ads = []
    if request.user.is_authenticated and request.user.is_customer:
        customer = CustomerModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(customer=customer)
        order_list = list(order_queryset)
        finished_ads = [item for item in order_list
                        if item.customer.user == request.user
                        and item.is_approved
                        and not item.is_canceled
                        and item.advertiser_paid_approval
                        and item.customer_paid_approval
                        and not item.is_running
                        and item.is_complete]
    elif request.user.is_authenticated and request.user.is_advertiser:
        user = request.user
        advertiser = AdvertiserModel.objects.get(user=user)
        advertise_queryset = AdvertiseModel.objects.filter(advertiser=advertiser)
        advertise_list = list(advertise_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list
                            if item.advertise in advertise_list]
        finished_ads = [item for item in final_order_list
                        if item.is_approved
                        and not item.is_canceled
                        and item.advertiser_paid_approval
                        and item.customer_paid_approval
                        and not item.is_running
                        and item.is_complete]
    return finished_ads
