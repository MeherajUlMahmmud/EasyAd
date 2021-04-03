from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            return redirect('customer-dashboard')
        elif request.user.is_authenticated and request.user.is_advertiser:
            return redirect('advertiser-dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def show_to_advertiser(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_admin or request.user.is_advertiser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator


def show_to_customer(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_admin or request.user.is_customer:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator
