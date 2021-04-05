from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.text import slugify

from user_control.decorators import *
from user_control.forms import *
from ad_control.models import *


@unauthenticated_user
def home_view(request):
    context = {
    }
    return render(request, 'user_control/index.html', context)


@unauthenticated_user
def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user and user.is_advertiser:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('advertiser-dashboard')

            elif user and user.is_customer:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('customer-dashboard')
            else:
                messages.error(request, 'Username or Password is incorrect.')
                return redirect('login')
        else:
            return render(request, 'user_control/login.html', {'form': form})

    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user_control/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@unauthenticated_user
def advertiser_signup_view(request):
    if request.method == "POST":
        advertiser_form = AdvertiserRegistrationForm(request.POST)
        if advertiser_form.is_valid():
            advertiser_form.save()
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, email=email, password=password)
            slug_str = "%s %s" % (user.name, user.id)
            user.slug = slugify(slug_str)
            user.save()
            AdvertiserModel.objects.create(user=user)
            login(request, user)
            return redirect('advertiser-dashboard')
        else:
            context = {
                'advertiser_form': advertiser_form
            }
            return render(request, 'user_control/advertiser/advertiser-signup.html', context)
    else:
        advertiser_form = AdvertiserRegistrationForm()

    context = {
        'advertiser_form': advertiser_form
    }
    return render(request, 'user_control/advertiser/advertiser-signup.html', context)


@unauthenticated_user
def customer_signup_view(request):
    if request.method == "POST":
        customer_form = CustomerRegistrationForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, email=email, password=password)
            slug_str = "%s %s" % (user.name, user.id)
            user.slug = slugify(slug_str)
            user.save()
            CustomerModel.objects.create(user=user)
            login(request, user)
            return redirect('customer-dashboard')
        else:
            context = {
                'customer_form': customer_form
            }
            return render(request, 'user_control/customer/customer-signup.html', context)
    else:
        customer_form = CustomerRegistrationForm()

    context = {
        'customer_form': customer_form
    }
    return render(request, 'user_control/customer/customer-signup.html', context)


@login_required
@show_to_advertiser(allowed_roles=['admin', 'is_advertiser'])
def advertiser_dashboard(request):
    ad_queryset = AdvertiseModel.objects.all()
    ad_list = list(ad_queryset)
    order_queryset = OrderModel.objects.all()
    order_list = list(order_queryset)
    unchecked_orders = [item for item in order_list
                        if item.advertise.user == request.user
                        and not item.is_approved
                        and not item.is_canceled]
    unpaid_orders = [item for item in order_list
                     if item.advertise.user == request.user
                     and item.is_approved
                     and not item.is_paid]
    context = {
        'ad_list': ad_list,
        'unchecked_orders': unchecked_orders,
        'unpaid_orders': unpaid_orders,
    }
    return render(request, 'user_control/advertiser/advertiser-dashboard.html', context)


@login_required
@show_to_customer(allowed_roles=['admin', 'is_customer'])
def customer_dashboard(request):
    ad_queryset = AdvertiseModel.objects.filter(is_active=True)
    ad_list = list(ad_queryset)

    customer = CustomerModel.objects.get(user=request.user)
    order_queryset = OrderModel.objects.filter(customer=customer)
    order_list = list(order_queryset)
    pending_orders = [item for item in order_list
                      if item.customer.user == request.user
                      and not item.is_approved]
    unpaid_orders = [item for item in order_list
                     if item.customer.user == request.user
                     and item.is_approved
                     and not item.customer_paid_approval]
    ads_to_run = [item for item in order_list
                  if item.customer.user == request.user
                  and item.is_approved
                  and item.customer_paid_approval
                  and not item.is_running]
    running_ads = [item for item in order_list
                   if item.customer.user == request.user
                   and item.is_approved
                   and item.customer_paid_approval
                   and item.is_running
                   and not item.is_complete]
    finished_ads = [item for item in order_list
                    if item.customer.user == request.user
                    and item.is_approved
                    and item.customer_paid_approval
                    and not item.is_running
                    and item.is_complete]
    context = {
        'order_list': order_list,
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
        'recent_ads': ad_list[:3],
    }
    return render(request, 'user_control/customer/customer-dashboard.html', context)


@login_required
def profile_view(request, slug):
    return render(request, "user_control/profile.html")


def about_view(request):
    return render(request, "about.html")


def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email_add = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        send_mail(
            subject + ' from ' + name,
            message,
            email_add,
            ['officialjobland777@gmail.com', ],
            # the mail address that the email will be sent to
        )
        messages.success(request, "Feedback sent successfully.")

        return render(request, 'contact.html')

    return render(request, 'contact.html')


def account_settings(request):
    return render(request, 'settings.html')