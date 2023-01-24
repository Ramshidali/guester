import json
import datetime

from math import fabs

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from main.functions import generate_form_errors, get_auto_id
from main.decorators import role_required, ajax_required, permissions_required
from customers.models import *
from main.functions import decrypt_message, encrypt_message, get_auto_id, get_otp
from shops.models import *


@login_required
def customers(request):
    instances = Customer.objects.filter(is_deleted=False, is_active=True).order_by("-date_added")
    revoked_instances = Customer.objects.filter(is_deleted=False, is_active=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'revoked_instances': revoked_instances, 
        'page_name' : 'Customers', 
        'app_name' :'Customers', 
        'page_title' : 'Customers', 
        'is_customer' : True,
        'filter_data' : filter_data
    }
    
    return render(request, 'dashboard/customers/customers.html', context)


@login_required
def customer(request, pk):
    instance = Customer.objects.get(pk=pk, is_deleted=False)
    fav_dishes = FavoriteFood.objects.filter(customer=instance)
    fav_spots = FavoriteRestaurant.objects.filter(customer=instance)
    shop_ratings = ShopRating.objects.filter(customer=instance)
    
    context = {
        'instance': instance, 
        'fav_dishes' : fav_dishes, 
        'fav_spots' : fav_spots, 
        'shop_ratings' : shop_ratings, 
        'page_name' : 'Customer', 
        'app_name' :'Customers', 
        'page_title' : 'Customer', 
        'is_need_light_box' : True, 
        'is_customer' : True,
    }
         
    return render(request, 'dashboard/customers/customer.html', context)


@login_required
@permissions_required(['can_revoke_customer'])
def revoke_customer(request, pk):
    instance = get_object_or_404(Customer.objects.filter(pk=pk, is_deleted=False))

    User.objects.filter(pk=instance.user.pk).update(is_active=False)
    Customer.objects.filter(pk=pk).update(is_active=False)

    response_data = {
        "status" : "success", 
        "title" : "Successfully Revoked", 
        "message" : "Access Successfully Revoked.", 
        "redirect" : "true", 
        "redirect_url" : reverse('customers:customers')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_grant_customer'])
def grant_customer(request, pk):
    instance = get_object_or_404(Customer.objects.filter(pk=pk, is_deleted=False))

    User.objects.filter(pk=instance.user.pk).update(is_active=True)
    Customer.objects.filter(pk=pk).update(is_active=True)

    response_data = {
        "status" : "success", 
        "title" : "Successfully Granted", 
        "message" : "Access Successfully Granted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('customers:customers')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')