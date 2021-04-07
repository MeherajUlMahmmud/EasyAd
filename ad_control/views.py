from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ad_control.forms import *
from ad_control.models import *
from user_control.utils import *


@login_required
def post_ad_view(request):
    task = "Post New"

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    form = PostAdForm()
    if request.method == 'POST':
        form = PostAdForm(request.POST, request.FILES)
        if form.is_valid():
            new_ad = form.save(commit=False)
            new_ad.user = request.user
            form.save()
            return redirect('home')
        else:
            context = {
                'task': task,
                'form': form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'ads_to_run': ads_to_run,
                'running_ads': running_ads,
                'finished_ads': finished_ads,
            }
            return render(request, 'ad_control/post-update-ad.html', context)

    context = {
        'task': task,
        'form': form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'ad_control/post-update-ad.html', context)


@login_required
def update_ad_view(request, pk):
    task = "Update"
    ad_item = AdvertiseModel.objects.get(id=pk)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    form = PostAdForm(instance=ad_item)
    if request.method == 'POST':
        form = PostAdForm(request.POST, request.FILES, instance=ad_item)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'task': task,
                'form': form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'ads_to_run': ads_to_run,
                'running_ads': running_ads,
                'finished_ads': finished_ads,
            }
            return render(request, 'ad_control/post-update-ad.html', context)

    context = {
        'task': task,
        'form': form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'ad_control/post-update-ad.html', context)


@login_required
def ad_detail_view(request, pk):
    ad_item = AdvertiseModel.objects.get(id=pk)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    try:
        customer_ordered = OrderModel.objects.get(customer=request.user, advertise=ad_item)
    except:
        customer_ordered = None

    location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

    if ad_item.location is not None:
        locations = ad_item.location.split(' ')
        location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

        for location in locations:
            location_link += location + "%20"

        location_link += "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"

    if request.GET.get('deactivateAd'):
        ad_item.is_active = False
        ad_item.save()
        return redirect('ad-detail', ad_item.id)

    if request.GET.get('activateAd'):
        ad_item.is_active = True
        ad_item.save()
        return redirect('ad-detail', ad_item.id)

    context = {
        'ad_item': ad_item,
        'location_link': location_link,
        'customer_ordered': customer_ordered,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'ad_control/ad-detail.html', context)


@login_required
def confirm_order_view(request, pk):
    ad_item = AdvertiseModel.objects.get(id=pk)
    customer = CustomerModel.objects.get(user=request.user)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    form = ConfirmOrderForm()
    if request.method == 'POST':
        form = ConfirmOrderForm(request.POST, request.FILES)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.advertise = ad_item

            duration = int(form.cleaned_data['duration'])
            price_rate = form.cleaned_data['price_rate']

            new_order.duration = duration
            new_order.price_rate = price_rate

            total = 1
            if price_rate == "Day":
                total = duration * ad_item.price
            elif price_rate == "Month":
                total = duration * 30 * ad_item.price

            new_order.total_cost = total

            form.save()
            return redirect('home')
        else:
            context = {
                'ad_item': ad_item,
                'form': form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'ads_to_run': ads_to_run,
                'running_ads': running_ads,
                'finished_ads': finished_ads,
            }
            return render(request, 'user_control/customer/confirm-order.html', context)

    context = {
        'ad_item': ad_item,
        'form': form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/customer/confirm-order.html', context)


@login_required
def order_details_view(request, pk):
    order_item = OrderModel.objects.get(id=pk)
    ad_item = order_item.advertise
    customer = CustomerModel.objects.get(user=request.user)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'order_item': order_item,
        'ad_item': ad_item,
        'customer': customer,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/order-details.html', context)


@login_required
def advertiser_unchecked_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    if request.GET.get('acceptOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_approved = True
        order_item.save()
        return redirect('unchecked-orders')

    if request.GET.get('rejectOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_canceled = True
        order_item.save()
        return redirect('unchecked-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/advertiser/unchecked-orders.html', context)


# TODO
@login_required
def advertiser_unpaid_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    if request.GET.get('acceptOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_approved = True
        order_item.save()
        return redirect('unchecked-orders')

    if request.GET.get('rejectOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_canceled = True
        order_item.save()
        return redirect('unchecked-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/advertiser/unpaid-orders.html', context)


@login_required
def advertiser_ads_to_run_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    if request.GET.get('runAd'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.advertiser_paid_approval = True
        order_item.is_running = True
        order_item.save()
        return redirect('advertiser-ads-to-run-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/advertiser/ads-to-run.html', context)


@login_required
def advertiser_running_ads_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    if request.GET.get('adFinished'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_running = False
        order_item.is_complete = True
        order_item.save()
        return redirect('advertiser-running-ads')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/advertiser/running-ads.html', context)


@login_required
def advertiser_finished_ads_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/advertiser/finished-ads.html', context)


@login_required
def customer_pending_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    if request.GET.get('cancelOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_canceled = True
        order_item.save()
        return redirect('customer-pending-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/customer/pending-orders.html', context)


@login_required
def customer_unpaid_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    if request.GET.get('submitPayment'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.customer_paid_approval = True
        order_item.save()

        transactionID = request.GET.get('transactionID')
        phoneNumber = request.GET.get('phoneNumber')
        OrderPaymentModel.objects.create(order=order_item, transaction_id=transactionID,
                                         phone_number=phoneNumber)
        return redirect('customer-unpaid-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/customer/unpaid-orders.html', context)


@login_required
def customer_ads_to_run_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/customer/ads-to-run.html', context)


@login_required
def customer_running_ads_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/customer/running-ads.html', context)


@login_required
def customer_finished_ads_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/customer/finished-ads.html', context)
