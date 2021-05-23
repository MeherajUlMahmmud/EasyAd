from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.text import slugify

from user_control.decorators import *
from user_control.forms import *
from ad_control.models import *
from user_control.utils import *


@unauthenticated_user
def home_view(request):
    return render(request, 'user_control/index.html')


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
    user = request.user
    advertiser = AdvertiserModel.objects.get(user=user)
    ad_queryset = AdvertiseModel.objects.filter(advertiser=advertiser)
    # ad_queryset = AdvertiseModel.objects.all()
    ad_list = list(ad_queryset)
    # print(ad_list)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'ad_list': ad_list,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/advertiser/advertiser-dashboard.html', context)


@login_required
@show_to_customer(allowed_roles=['admin', 'is_customer'])
def customer_dashboard(request):
    ad_queryset = AdvertiseModel.objects.filter(is_active=True)
    ad_list = list(ad_queryset)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    # order_queryset = OrderModel.objects.all()
    # order_list = list(order_queryset)
    # ordered_ad_list = [order.advertise for order in order_list]
    #
    # ad_list = [ad for ad in ad_list if ad not in ordered_ad_list]

    search_keyword = request.GET.get('q')
    if search_keyword is not None:
        new_list = ad_list
        ad_list = list(item for item in new_list if search_keyword in item.location.lower())

        context = {
            'ad_list': ad_list,
            'search_keyword': search_keyword,

            'pending_orders': pending_orders,
            'unpaid_orders': unpaid_orders,
            'ads_to_run': ads_to_run,
            'running_ads': running_ads,
            'finished_ads': finished_ads,
        }
        return render(request, 'user_control/customer/customer-dashboard.html', context)

    context = {
        'ad_list': ad_list,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'user_control/customer/customer-dashboard.html', context)


@login_required
def customer_profile_view(request, slug):
    # ad_queryset = AdvertiseModel.objects.filter(is_active=True)
    # ad_list = list(ad_queryset)
    user = User.objects.get(slug=slug)
    profile = CustomerModel.objects.get(user=user)

    orders = OrderModel.objects.filter(customer=profile, is_complete=True)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'user': user,
        'profile': profile,
        'orders': orders,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, "user_control/profile.html", context)


@login_required
def advertiser_profile_view(request, slug):
    user = User.objects.get(slug=slug)
    profile = AdvertiserModel.objects.get(user=user)
    ads = AdvertiseModel.objects.filter(advertiser=profile)
    orders = OrderModel.objects.filter(advertise__in=list(ads), is_complete=True)

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    context = {
        'user': user,
        'profile': profile,
        'ads': ads,
        'orders': orders,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, "user_control/profile.html", context)


@login_required
def advertiser_edit_profile(request):
    profile = AdvertiserModel.objects.get(user=request.user)

    form = AdvertiserEditProfileForm(instance=profile)
    if request.method == 'POST':
        form = AdvertiserEditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('advertiser-profile', request.user.slug)
        else:
            return redirect('edit-profile')

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'user_control/edit-profile.html', context)


@login_required
def customer_edit_profile(request):
    profile = CustomerModel.objects.get(user=request.user)

    form = CustomerEditProfileForm(instance=profile)
    if request.method == 'POST':
        form = CustomerEditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('customer-profile', request.user.slug)
        else:
            return redirect('edit-profile')

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'user_control/edit-profile.html', context)


def about_view(request):
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
    return render(request, "about.html", context)


def contact_view(request):
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

    if request.method == 'POST':
        name = request.POST['name']
        email_add = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        FeedbackModel.objects.create(name=name, email=email_add, subject=subject, message=message)

        # send_mail(
        #     subject + ' from ' + name,
        #     message,
        #     email_add,
        #     ['officialjobland777@gmail.com', ],
        #     # the mail address that the email will be sent to
        # )
        messages.success(request, "Feedback sent successfully.")

        return render(request, 'contact.html', context)

    return render(request, 'contact.html', context)


@login_required
def account_settings(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    ads_to_run = get_ads_to_run(request)
    running_ads = get_running_ads(request)
    finished_ads = get_finished_ads(request)

    user = request.user

    information_form = AccountInformationForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        information_form = AccountInformationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if information_form.is_valid():
            information_form.save()
            slug_str = "%s %s" % (user.name, user.id)
            user.slug = slugify(slug_str)
            user.save()
            return redirect('settings')

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            context = {
                'information_form': information_form,
                'password_form': password_form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'ads_to_run': ads_to_run,
                'running_ads': running_ads,
                'finished_ads': finished_ads,
            }
            return render(request, 'settings.html', context)
    context = {
        'information_form': information_form,
        'password_form': password_form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'ads_to_run': ads_to_run,
        'running_ads': running_ads,
        'finished_ads': finished_ads,
    }
    return render(request, 'settings.html', context)
