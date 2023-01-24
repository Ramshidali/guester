from datetime import datetime

from django.db.models import Max
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr

from api.v1.filter.serializers import BadgeSerializer, CuisineSerializer, DaysSerializer, ReLocationSerializer, ReSearchSerializer, ShopTypeSerializer
from api.v1.users.serializers import DishSerializer, ShopDishSerializer, ShopSerializer
from customers.models import Customer
from dishes.models import DISH_TIMING, Cuisine, Dish
from general.functions import get_auto_id
from general.models import Badge, Days, Location, RecentLocation, RecentSearches
from shops.models import Shop, ShopDish, ShopType, ShopWorkingDay

from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def filter_cuisine(request):
    try:
        cuisine_type = request.GET.get('type') 
    except:
        cuisine_type = None
    
    cuisine_instances = Cuisine.objects.filter(is_verified=True,is_deleted=False)
    
    if cuisine_type :
        cuisine_instances = cuisine_instances.filter(type=cuisine_type)

    # cuisine = {}
    # cuisine_obj = list(cuisine_instances.values('id','name'))
    # cuisine['data'] = cuisine_obj
    
    serialized = CuisineSerializer(cuisine_instances, many=True, context={"request": request})
    
    response_data = {
        "StatusCode": 6000,
        "cuisine": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_filters(request):
    category_instances = ShopType.objects.filter(is_deleted=False)
    
    max_price_for_two = Shop.objects.filter(is_verified=True,is_rejected=False,is_deleted=False)
    max_amount = max_price_for_two.aggregate(Max('average_cost_for_two')).values()
    for amount in max_amount:
        amount = amount
    
    category = {}
    category_obj = list(category_instances.values('id','name'))
    category['data'] = category_obj
    
    dish_timing = []
    for key, v in DISH_TIMING:
        dish_timing.append({"id" : key,"time" : v})
    
    badge_instances = Badge.objects.filter(is_deleted=False)
    badge_serialized = BadgeSerializer(badge_instances, many=True, context={"request": request})
    
    days_instances = Days.objects.filter(is_deleted=False)
    days_serialized = DaysSerializer(days_instances, many=True, context={"request": request})
    
    shop_type_instances = ShopType.objects.filter(is_deleted=False)
    shop_type_serialized = ShopTypeSerializer(shop_type_instances, many=True, context={"request": request})
    
    response_data = {
        "StatusCode": 6000,
        "category": category,
        "dish_timing": dish_timing,
        "max_avg_price_for_two": str(amount),
        "max_distence": "50",
        "badge": badge_serialized.data,
        "working_days": days_serialized.data,
        "shop_types": shop_type_serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def apply_filter(request):
    instances = None
    instances = ShopDish.objects.filter(is_deleted=False)
    
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(shop__name__icontains=query) |
            Q(dish__name__icontains=query) |
            Q(shop__location__short_name__icontains=query)
        )
    
    try:
        cuisine = request.GET.get('cuisine').split(",")
    except:
        cuisine = None
    # print(cuisine)
    try:
        dish_timing = request.GET.get('dish_timing').split(",")
    except:
        dish_timing = None
    try:
        working_days = request.GET.get('working_days').split(",")
    except:
        working_days = None
        
    try:
        shop_type = request.GET.get('shop_type').split(",")
    except:
        shop_type = None
        
    try:    
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")
        
        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None
        
    category = request.GET.get('category')
    badge = request.GET.get('badge')
    distence = request.GET.get('distence')
    dietary_type = request.GET.get('dietary_type')
    avg_price_for_two = request.GET.get('max_avg_price_for_two')

    if cuisine:
        instances = instances.filter(dish__cuisine__pk__in=cuisine)

    if category:
        instances = instances.filter(dish__dish_category__pk=category)

    if dish_timing:
        instances = instances.filter(dish__dish_timing__in=dish_timing)

    if working_days:
        shop_working = ShopWorkingDay.objects.filter(day__pk__in=working_days,is_deleted=False).values_list("shop__pk")
        instances = instances.filter(shop__in=shop_working)
    
    if shop_type:
        instances = instances.filter(shop__shop_type__pk__in=shop_type)
    
    if avg_price_for_two:
        instances = instances.filter(shop__average_cost_for_two__lte=avg_price_for_two)
        
    if badge:
        instances = instances.filter(shop__badge__pk=badge)
        
    if dietary_type:
        instances = instances.filter(dish__dietary_type=dietary_type)
        
    if distence:
        instances = instances.filter(dish__dietary_type__in=badge).annotate(distance=Distance('located', user_location)).order_by('distance')
    
    dishes = instances.values_list("dish__pk")
    shops = instances.values_list("shop__pk")
    
    dish_serialized = []
    shop_serialized = []
    
    if Dish.objects.filter(pk__in=dishes, is_deleted=False).exists():
        # print("in dish condition")
        dish_instance = instances.filter(dish__pk__in=dishes, is_deleted=False).distinct()
        dish_serialized = ShopDishSerializer(dish_instance, many=True, context={"request": request}).data
        
    if Shop.objects.filter(pk__in=shops, is_deleted=False).exists():
        # print("in shop condition")
        shop_instance = instances.filter(shop__pk__in=shops, is_deleted=False).distinct()
        shop_serialized = ShopDishSerializer(shop_instance, many=True, context={"request": request, "user_location": user_location}).data
        
    # serialized = ShopDishSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": {
            "dishes" : dish_serialized,
            "shops" : shop_serialized,
            },
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def search(request):
    instances = ShopDish.objects.filter(shop__is_verified=True, dish__is_verified=True, is_deleted=False)

    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(shop__name__icontains=query) |
            Q(dish__name__icontains=query) |
            Q(shop__location__short_name__icontains=query)
        )

    serialized = ShopDishSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000, 
        "data": serialized.data
        }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def save_search(request):
    customer = Customer.objects.get(user=request.user,is_deleted=False)
    s = request.GET.get ("s")
    
    if not RecentSearches.objects.filter(customer=customer,keys=s,is_deleted=False).exists() :
        RecentSearches.objects.create(
            customer=customer,
            auto_id=get_auto_id(RecentSearches),
            creator=request.user,
            keys=s
        )
        response_data = {
            "StatusCode": 6000,
            "message": "Sucess",
        }
    else :
        RecentSearches.objects.filter(customer=customer,keys=s,is_deleted=False).update(
            date_updated = datetime.today()
        )
        response_data = {
            "StatusCode": 6000,
            "message": "Updated",
        }
        
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def save_location(request):
    customer = Customer.objects.get(user=request.user,is_deleted=False)
    latitude = request.GET.get ("latitude")
    longitude = request.GET.get ("longitude")
    short_name = request.GET.get ("location_name")
    
    try:
        
        if not RecentLocation.objects.filter(customer__user=request.user,latitude=latitude,longitude=longitude).exists() :
            RecentLocation.objects.create(
                customer=customer,
                auto_id=get_auto_id(RecentLocation),
                creator=request.user,
                latitude=latitude,
                longitude=longitude,
                short_name=short_name,
            )
            response_data = {
            "StatusCode": 6000,
            "message": "Success",
            }
        else:
            RecentLocation.objects.filter(customer__user=request.user,latitude=latitude,longitude=longitude).update(
                date_updated = datetime.today()
            )
            response_data = {
                "StatusCode": 6000,
                "message": "Updated",
            }
    except :
        response_data = {
            "StatusCode": 6001,
            "message": "No location Found",
        }
        
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_search(request):
    serach_instances = RecentSearches.objects.filter(customer__user=request.user).order_by('-date_updated')[:5]
    serach_serialized = ReSearchSerializer(serach_instances, many=True, context={"request": request})
    
    location_instances = RecentLocation.objects.filter(customer__user=request.user).order_by('-date_updated')[:5]
    location_serialized = ReLocationSerializer(location_instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": {
            "searches" : serach_serialized.data,
            "locations" : location_serialized.data,
            }
    }

    return Response(response_data, status=status.HTTP_200_OK)