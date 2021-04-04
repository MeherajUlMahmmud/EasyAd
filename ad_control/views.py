from django.shortcuts import render, redirect

from ad_control.forms import *
from ad_control.models import *


def post_ad_view(request):
    task = "Post New"
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
                'form': form
            }
            return render(request, 'ad_control/post-update-ad.html', context)

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'ad_control/post-update-ad.html', context)


def ad_detail_view(request, pk):
    ad_item = AdvertiseModel.objects.get(id=pk)

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

    # if request.GET.get('orderNow'):
    #     ad_item.is_active = True
    #     ad_item.save()
    #     return redirect('ad-detail', ad_item.id)

    context = {
        'ad_item': ad_item,
        'location_link': location_link,
        'customer_ordered': customer_ordered,
    }
    return render(request, 'ad_control/ad-detail.html', context)


def confirm_order_view(request, pk):
    ad_item = AdvertiseModel.objects.get(id=pk)
    customer = CustomerModel.objects.get(user=request.user)

    form = ConfirmOrderForm()
    if request.method == 'POST':
        form = ConfirmOrderForm(request.POST, request.FILES)
        # print("Inside post")
        if form.is_valid():
            # print("inside valid")
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.advertise = ad_item

            duration = int(form.cleaned_data['duration'])
            # print(duration)
            # print(type(duration))
            price_rate = form.cleaned_data['price_rate']
            # print(price_rate)

            new_order.duration = duration
            new_order.price_rate = price_rate

            total = 1
            if price_rate == "Day":
                total = duration * ad_item.price
            elif price_rate == "Month":
                total = duration * 30 * ad_item.price

            new_order.total_cost = total

            form.save()
            # print("Order saved")
            return redirect('home')
        else:
            print("Inside invalid")
            context = {
                'ad_item': ad_item,
                'form': form
            }
            return render(request, 'ad_control/confirm-order.html', context)

    context = {
        'ad_item': ad_item,
        'form': form,
    }
    return render(request, 'ad_control/confirm-order.html', context)


def checkout_view(request):
    return render(request, 'ad_control/checkout.html')
