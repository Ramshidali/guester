from datetime import datetime, timedelta, time
import datetime 

from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User

from staffs.models import Staff
from staffs.forms import PasswordForm
from customers.models import *
from shops.models import *
from dishes.models import *
from main.functions import get_current_role
# @check_mode

@login_required
def app(request):
    return HttpResponseRedirect(reverse('index'))


@login_required
def index(request):
    if get_current_role(request)=='shop_admin':
        instance = ShopAdmin.objects.get(user=request.user).shop
        facilities = ShopFacility.objects.filter(is_deleted=False, shop=instance)
        delivery_partners = ShopDelivery.objects.filter(is_deleted=False, shop=instance)
        dishes = ShopDish.objects.filter(is_deleted=False, shop=instance)
        gallery = ShopGallery.objects.filter(is_deleted=False, shop=instance)
        working_days = ShopWorkingDay.objects.filter(is_deleted=False, shop=instance)
        dish_offers = DishOffer.objects.filter(is_deleted=False, shop=instance)
        precautions = ShopSafetyPrecaution.objects.filter(is_deleted=False ,shop=instance)
        shop_offers = MoreOffer.objects.filter(is_deleted=False, shop=instance)
        shop_reviews = ShopRating.objects.filter(is_deleted=False, shop = instance)
        try:
            shop_admin = ShopAdmin.objects.get(is_deleted=False, shop=instance)
        except :
            shop_admin= None
        
        current_role = "shop-admin"
        context = {
            'instance': instance,
            'current_role' : current_role,
            'facilities' : facilities,
            'delivery_partners' : delivery_partners,
            'gallery' : gallery,
            'dishes' : dishes,
            'dish_offers' : dish_offers,
            'shop_offers' : shop_offers,
            'working_days' : working_days,
            'precautions' : precautions,
            'shop_reviews' : shop_reviews,
            'shop_admin' : shop_admin,
            'page_name' : 'Shop',
            'app_name' :'Shops',
            'page_title' : 'Shop',
            'is_need_light_box' : True,
        }
            
        return render(request, 'dashboard/shop-dashboard/dashboard.html', context)
        
    # elif get_current_role(request)=='staff' or  get_current_role(request)=='superadmin':
    else:
        today = datetime.datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.datetime.combine(today, time())
        today_end = datetime.datetime.combine(tomorrow, time())
        
        users = Customer.objects.filter(is_deleted=False).order_by("-date_added")
        total_users = users.count()
        users_today = users.filter(date_added__lte=today_end, date_added__gte=today_start).count()
        
        shops = Shop.objects.filter(is_deleted=False,is_verified=True).order_by("-date_added")
        shops_today = shops.filter(date_added__lte=today_end, date_added__gte=today_start).count()
        total_shops = shops.count()
        
        staffs = Staff.objects.filter(is_deleted=False).order_by("-date_added")
        staffs_today = staffs.filter(date_added__lte=today_end, date_added__gte=today_start).count()
        total_staffs = staffs.count()

        dishes = Dish.objects.filter(is_deleted=False, is_verified=True).order_by("-date_added")
        dishes_today = dishes.filter(date_added__lte=today_end, date_added__gte=today_start).count()
        total_dishes = dishes.count()
        
        shop_reviews = ShopRating.objects.filter(is_deleted=False).order_by("-date_added")
        
        if get_current_role(request)=='staff':
            
            current_role = "staff"
        else:
            current_role= "superadmin"
            
        print(current_role,"**********************************")
    
        context = {
            'page_title' : 'Dashboard',
            'current_role' : current_role,
            'total_users':total_users,
            'total_shops':total_shops,
            'users_today':users_today,
            'shops_today':shops_today,
            'staffs_today':staffs_today,
            'total_staffs':total_staffs,
            'dishes_today':dishes_today,
            'total_dishes':total_dishes,
            'dishes' : dishes,
            'users' : users,
            'shop_reviews' : shop_reviews,
        }
        
        return render(request,'dashboard/index.html', context)

    # else:
    #     context = {
    #         "title": "Permission Denied"
    #     }
    #     return render(request, 'errors/403.html', context)

@login_required
def profile(request):
    user_name =request.user
    user =User.objects.get(username=user_name)
    instance = Staff.objects.get(email = user.email)
    permissions = instance.permission.all()
    form = PasswordForm()
    
    context = {
        'page_title' : 'Profile',
        'form' : form,
        'user' : user,
        'instance' : instance,
        'permissions' : permissions,
    }
    
    return render(request,'dashboard/profile.html', context)