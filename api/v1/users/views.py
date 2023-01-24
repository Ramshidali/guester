import datetime
from datetime import datetime

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from django.db.models import Sum

from api.v1.general.functions import generate_serializer_errors
from api.v1.users.serializers import  *
from customers.models import AppFeedback, Customer, FavoriteFood, FavoriteRestaurant
from dishes.models import Cuisine, Dish, DishCategory
from general.functions import get_auto_id
from shops.models import BrandOffer, MoreOffer, ShopDelivery, ShopDish, ShopFacility, ShopGallery, ShopGalleryType,ShopOffer,Shop, ShopRating, ShopSafetyPrecaution, ShopStory, ShopWorkingDay
from brands.models import Brand

from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def restaurant_offers(request):
    """
    for showing the all offers of restaurants from nearest, when selecting location or getting all offers
    :param request:
    :return:
    """
    # print(request.GET.get("latitude"),"latitude")
    # print(request.GET.get("longitude"),"longitude")
    try:
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None
    # print(user_location)
    brand_instances = Brand.objects.filter(is_deleted=False)
    brand_instance_data = brand_instances.values_list("id",flat=True)

    if user_location:
        instances = Shop.objects.filter(is_deleted=False,is_verified=True).annotate(distance=Distance('located', user_location)
                          ).exclude(brand__in=brand_instance_data).order_by('distance')
        # .filter(distance__lte = 10000)
        instance_data = instances.values_list("id",flat=True)
        shop_offer_instances = ShopOffer.objects.filter(shop__in=instance_data,is_active=True,is_deleted=False)
        offer_serialized = ShopOfferSerializer(shop_offer_instances, many=True, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": offer_serialized.data,
        }
    else:
        instances = Shop.objects.filter(is_deleted=False,is_verified=True).exclude(brand__in=brand_instance_data).order_by('distance')[:3]
        # .filter(distance__lte = 10000)
        instance_data = instances.values_list("id",flat=True)
        shop_offer_instances = ShopOffer.objects.filter(shop__in=instance_data,is_active=False,is_deleted=False)
        offer_serialized = ShopOfferSerializer(shop_offer_instances, many=True, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": offer_serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def restaurents(request):
    """
    for showing the restaurants from nearest, when selecting location or getting all offers
    :param request:
    :return:
    """
    try:
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None
    # print(user_location)

    if user_location:
        # print("------")
        brand_instances = Brand.objects.filter(is_deleted=False)
        brand_instance_data = brand_instances.values_list("id",flat=True)

        instances = Shop.objects.filter(is_deleted=False,is_verified=True).annotate(distance=Distance('located', user_location)
                          ).exclude(brand__in=brand_instance_data).order_by('distance')[:3]
        # .filter(distance__lte = 10000)
        serialized = ShopSerializer(instances, many=True, context={"request": request,
                                                                   "user_location" : user_location,
                                                                   "user" : request.user,
                                                                   })
        # instance_data = instances.values_list("id",flat=True)

        # shop_offer_instances = ShopOffer.objects.filter(shop__in=instance_data,is_deleted=False)
        # offer_serialized = ShopOfferSerializer(shop_offer_instances, many=True, context={"request": request})
        # # print(shop_offer_instances,"===============++++")

        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }
    else:
        # print("*************")
        instances = Shop.objects.filter(is_deleted=False,is_verified=True).order_by('rating')[:3]
        serialized = ShopSerializer(instances, many=True, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def brands(request):
    """
    for showing the brands from nearest shop, when selecting location or getiing all offers
    :param request:
    :return:
    """
    try:
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None
    # print(user_location)

    if user_location:
        # print("------")
        brand_instances = Brand.objects.filter(is_deleted=False).values_list("id",flat=True)
        shop_instances = Shop.objects.filter(brand__in=brand_instances,is_deleted=False,is_verified=True).annotate(distance=Distance('located', user_location)).order_by('distance')
        brand_id = shop_instances.values_list("brand__pk",flat=True)

        brand_offer = BrandOffer.objects.filter(brand__in=brand_id,is_active=True,is_deleted=False)
        brand_offer_serialized = BrandoffersSerializer(brand_offer, many=True, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": brand_offer_serialized.data,
        }
    else:
        brand_instances = Brand.objects.filter(is_deleted=False).values_list("id",flat=True)
        shop_instances = Shop.objects.filter(brand__in=brand_instances,is_deleted=False,is_verified=True)
        brand_id = shop_instances.values_list("brand__pk",flat=True)

        brand_offer = BrandOffer.objects.filter(brand__in=brand_id,is_active=False,is_deleted=False)
        brand_offer_serialized = BrandoffersSerializer(brand_offer, many=True, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": brand_offer_serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shops_list(request):
    """
    for showing the shops
    :param request:
    :return:
    """
    try:
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None
    # print(user_location)
    shop_dish_instances = ShopDish.objects.filter(is_deleted=False)
    instances = Shop.objects.filter(is_deleted=False,is_verified=True)

    if request.GET.get("dietary_type") :
        dietary_type = request.GET.get("dietary_type")
        dt = shop_dish_instances.filter(dish__dietary_type=dietary_type).values("shop.pk")
        instances = instances.filter(pk__in=dt)

    if request.GET.get("price") :
        price = request.GET.get("price")
        if 'highest' in price:
            instances = instances.order_by('-average_cost_for_two')

        elif 'lowest' in price:
            instances = instances.order_by('average_cost_for_two')

    if request.GET.get("shop_type") :
        shop_type = request.GET.get("shop_type")
        st = shop_dish_instances.filter(shop__shop_type=shop_type).values("shop.pk")
        instances = instances.filter(pk__in=st)

    if request.GET.get("cuisine") :
        cuisine = request.GET.get("cuisine").split(",")
        # print(cuisine)
        cuisine_instance = Cuisine.objects.filter(pk__in=cuisine).values_list("pk")
        # print(cuisine_instance)
        c = shop_dish_instances.filter(dish__cuisine__in=cuisine_instance).values_list("shop__pk")
        # print(c)
        instances = instances.filter(pk__in=c)

    if request.GET.get("food_time") :
        food_time = request.GET.get("food_time").split(",")
        ft = shop_dish_instances.filter(dish__dish_timing__in=food_time).values_list("shop__pk")
        instances = instances.filter(pk__in=ft)

    if user_location:
        # print("------")
        instances = instances.annotate(distance=Distance('located', user_location)).filter(distance__lte = 10000).order_by('distance')

        serialized = ShopSerializer(instances, many=True, context={"request": request, "user_location" : user_location, "user" : request.user})
        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }
    else:
        # print("*************")
        instances = instances.order_by('rating')
        serialized = ShopSerializer(instances, many=True, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_view(request):
    """
    for showing the single view of shop
    :param request:
    :return:
    """
    response_data = {}
    pk = request.GET.get("shop_pk")

    instance = Shop.objects.get(pk=pk,is_deleted=False,is_verified=True)

    try:
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None

    dayint = datetime.today().weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = days[dayint]
    working_status = False
    working_time = False
    working_message = "closed"

    if ShopWorkingDay.objects.filter(shop=instance,day__day=weekday,is_deleted=False).exists() :
        time_now = datetime.now().time().strftime("%H:%M:%S")
        working_day = ShopWorkingDay.objects.filter(shop=instance,day__day=weekday,is_deleted=False).first()
        if str(working_day) == weekday :
            if not str(working_day.start_time) > str(time_now) and str(time_now) <= str(working_day.end_time) :
                working_status = True
                working_message = "Open"
                start_time = working_day.start_time.strftime("%I:%M %p")
                end_time = working_day.end_time.strftime("%I:%M %p")
                working_time = f"{start_time} - {end_time}"

    serialized = ShopViewSerializer(instance, context={
        "request": request,
        "user_location" : user_location,
        "working_status" : working_status,
        "working_message" : working_message,
        "working_time" : working_time,
        })

    more_offers = MoreOffer.objects.filter(shop=instance,is_deleted=False)
    more_offers_serializer = MoreOfferSerializer(more_offers, many=True, context={"request": request})

    shop_safety = ShopSafetyPrecaution.objects.filter(shop=instance,is_deleted=False)
    shop_safety_serializer = ShopSafetySerializer(shop_safety, many=True, context={"request": request})

    working_hours = ShopWorkingDay.objects.filter(shop=instance,is_deleted=False)
    workingday_serialized = ShopWorkingHoursSerializer(working_hours, many=True, context={"request": request})

    response_data = {
            "StatusCode": 6000,
            "data" : {
                "shop_data": serialized.data,
                "working_hours_data": workingday_serialized.data,
                "more_offers_data": more_offers_serializer.data,
                "shop_safety_data": [data.get("title") for data in shop_safety_serializer.data],
            }

        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_facility_view(request):
    """
    for showing facility on shop single page
    :param request:
    :return:
    """
    response_data = {}
    pk = request.GET.get("shop_pk")

    if Shop.objects.filter(pk=pk,is_deleted=False,is_verified=True).exists():
        instance = Shop.objects.get(pk=pk,is_deleted=False,is_verified=True)

        shop_facility = ShopFacility.objects.filter(shop=instance,is_deleted=False)
        shop_facility_serializer = ShopFacilitySerializer(shop_facility, many=True, context={"request": request})

        response_data = {
                "StatusCode": 6000,
                "data": shop_facility_serializer.data,
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message" : "no data"
            }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_gallery_view(request):
    """
    for showing gallery on shop single page
    :param request:
    :return:
    """
    response_data = {}

    if ShopGallery.objects.filter(is_deleted=False).exists():
        shop_gallery = ShopGallery.objects.filter(is_deleted=False)

        if request.GET.get("shop_pk") :
            shop_pk = request.GET.get("shop_pk")
            shop = Shop.objects.get(pk=shop_pk,is_deleted=False)
            shop_gallery = shop_gallery.filter(shop=shop)

        if request.GET.get("gallery_type") :
            gallery_type = request.GET.get("gallery_type")
            gallery_type = ShopGalleryType.objects.get(pk=gallery_type,is_deleted=False)
            shop_gallery = shop_gallery.filter(gallery_type=gallery_type)

        shop_gallery_serializer = ShopGallerySerializer(shop_gallery, many=True, context={"request": request})
        response_data = {
                "StatusCode": 6000,
                "data": shop_gallery_serializer.data,
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "No Data",
            }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_gallery_types(request):
    """
    for showing gallery types
    :param request:
    :return:
    """
    response_data = {}

    if ShopGalleryType.objects.filter(is_deleted=False).exists():
        shop_gallery_types = ShopGalleryType.objects.filter(is_deleted=False)

        serializer = ShopGalleryTypeSerializer(shop_gallery_types, many=True, context={"request": request})
        response_data = {
                "StatusCode": 6000,
                "data": serializer.data,
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "No Data",
            }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_offers(request):
    """
    for showing offers in single view of shop
    :param request:
    :return:
    """
    response_data = {}
    pk = request.GET.get("shop_pk")

    instance = ShopOffer.objects.filter(shop__pk=pk,is_active=True,is_deleted=False)
    serialized = ShopOfferSerializer(instance, many=True, context={"request": request})

    response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_cuisines(request):
    """
    for showing cuisines in single view of shop
    :param request:
    :return:
    """
    response_data = {}
    pk = request.GET.get("shop_pk")
    cuisine_type = request.GET.get("cuisine_type")

    instances = Cuisine.objects.filter(is_deleted=False)

    if pk :
        shop_dish = ShopDish.objects.filter(shop__pk=pk,is_deleted=False).values_list('dish__cuisine__pk')
        instances = instances.filter(pk__in=shop_dish)

    if cuisine_type :
        instances = instances.filter(type=cuisine_type)

    serialized = ShopCuisinesSerializer(instances, many=True, context={"request": request})

    response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_dishes_view(request):
    response_data = {}
    pk = request.GET.get("shop_pk")
    dietary_type = request.GET.get("dietary_type")

    try:
        cuisine = request.GET.get("cuisine").split(",")
    except:
        cuisine = None

    instances = ShopDish.objects.filter(shop__pk=pk,shop__is_verified=True,dish__is_verified=True,is_deleted=False)

    if instances.exists() :
        if request.GET.get("cuisine") :
            cuisine = request.GET.get("cuisine").split(",")
            # print(cuisine)
            cuisine_instance = Cuisine.objects.filter(pk__in=cuisine).values_list("pk")
            # print(cuisine_instance)
            instances = instances.filter(dish__cuisine__pk__in=cuisine_instance)

        if dietary_type :
            instances = instances.filter(dish__dietary_type=dietary_type)

        serialized = ShopDishSerializer(instances, many=True, context={"request": request,"shop_pk": pk})

        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else :
        response_data = {
            "StatusCode": 6001,
            "message": "No Data",
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_stories(request):
    """
    for showing stories
    :param request:
    :return:
    """
    response_data = {}
    if request.GET.get("customer_pk") and request.GET.get("shop_pk"):
        # print("in shop and customer")
        shop_pk = request.GET.get("shop_pk")
        customer_pk = request.GET.get("customer_pk")
        instance = ShopStory.objects.filter(customer__pk=customer_pk,shop__pk=shop_pk,is_deleted=False)

    elif request.GET.get("shop_pk") :
        # print("in shop")
        pk = request.GET.get("shop_pk")
        instance = ShopStory.objects.filter(shop__pk=pk,is_deleted=False)

    elif request.GET.get("customer_pk") :
        # print("in customer")
        pk = request.GET.get("customer_pk")
        instance = ShopStory.objects.filter(customer__pk=pk,is_deleted=False)

    else :
        instance = ShopStory.objects.filter(is_deleted=False)

    serialized = ShopStorySerializer(instance, many=True, context={"request": request})

    response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_rating(request):
    """
    for showing reviews in single view of shop
    :param request:
    :return:
    """
    response_data = {}
    pk = request.GET.get("shop_pk")

    if request.GET.get("shop_pk") :
        # print('inshop',pk)
        if ShopRating.objects.filter(shop__pk=pk,is_deleted=False).exists():
            try :
                instance = ShopRating.objects.filter(shop__pk=pk,is_deleted=False)

                customer_service = instance.aggregate(Sum('customer_service')).get('customer_service__sum')
                food_quality = instance.aggregate(Sum('food_quality')).get('food_quality__sum')
                likely_to_return = instance.aggregate(Sum('likely_to_return')).get('likely_to_return__sum')
                ambience = instance.aggregate(Sum('ambience')).get('ambience__sum')
                hygiene = instance.aggregate(Sum('hygiene')).get('hygiene__sum')

                total_rating =  customer_service + food_quality + likely_to_return + ambience +  hygiene

                serialized = ReviewSerializer(instance, many=True, context={"request": request})

                total_review_count = ShopRating.objects.filter(shop__pk=pk,is_deleted=False).count()

                response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "hygiene_rating": round((hygiene / total_review_count), 1),
                            "hygiene_percentage": round((hygiene / total_rating) * 100),
                            "ambience_rating" : round((ambience / total_review_count), 1),
                            "ambience_percentage": round((ambience / total_rating) * 100),
                            "food_quality_rating": round((food_quality / total_review_count), 1),
                            "food_quality_percentage": round((food_quality / total_rating) * 100),
                            "customer_service_rating": round((customer_service / total_review_count), 1),
                            "customer_service_percentage": round((customer_service / total_rating) * 100),
                            "likely_to_return_rating": round((likely_to_return / total_review_count), 1),
                            "likely_to_return_percentage": round((likely_to_return / total_rating) * 100),
                            "total_review": total_review_count,
                            "total_rating": round((total_rating / total_review_count) / 5, 1),
                            "reviews" : serialized.data,
                        }
                    }

            except ZeroDivisionError :
                response_data = {
                "StatusCode": 6000,
                "data": {
                    "hygiene_rating": 0,
                    "hygiene_percentage": 0,
                    "ambience_rating" : 0,
                    "ambience_percentage": 0,
                    "food_quality_rating": 0,
                    "food_quality_percentage": 0,
                    "customer_service_rating": 0,
                    "customer_service_percentage": 0,
                    "likely_to_return_rating": 0,
                    "likely_to_return_percentage": 0,
                    "total_review": 0,
                    "total_rating": 0,
                    "reviews" : [],
                }
            }
        else :
            response_data = {
                "StatusCode": 6000,
                "data": {
                    "hygiene_rating": 0,
                    "hygiene_percentage": 0,
                    "ambience_rating" : 0,
                    "ambience_percentage": 0,
                    "food_quality_rating": 0,
                    "food_quality_percentage": 0,
                    "customer_service_rating": 0,
                    "customer_service_percentage": 0,
                    "likely_to_return_rating": 0,
                    "likely_to_return_percentage": 0,
                    "total_review": 0,
                    "total_rating": 0,
                    "reviews" : [],
                }
            }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def post_review(request):

    try:
        review = request.data['review']
        shop_pk = request.data['shop_pk']
        hygiene = request.data['hygiene']
        ambience = request.data['ambience']
        food_quality = request.data['food_quality']
        customer_service = request.data['customer_service']
        likely_to_return = request.data['likely_to_return']
    except:
        response_data = {
            "StatusCode" : 6001,
            "title" : "Invalid data",
        }

        return Response(response_data, status=status.HTTP_200_OK)

    serialized = ShopRatingSerializer(data=request.data)
    customer =  Customer.objects.get(user=request.user,is_deleted=False)
    shop = Shop.objects.get(pk=shop_pk,is_deleted=False)

    if not ShopRating.objects.filter(shop__pk=shop_pk,customer__user=request.user,is_deleted=False).exists():

        if serialized.is_valid():
            auto_id = get_auto_id(ShopRating)
            data = ShopRating.objects.create(
                    auto_id = auto_id,
                    creator = request.user,
                    updater = request.user,

                    shop = shop,
                    review = review,
                    hygiene = hygiene,
                    ambience = ambience,
                    customer = customer,
                    food_quality = food_quality,
                    customer_service = customer_service,
                    likely_to_return = likely_to_return,
                )
            response_data = {
                    "StatusCode": 6000,
                    "message": "Success",
                }

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            message = generate_serializer_errors(serialized._errors)
            response_data = {
                "StatusCode" : 6001,
                "message" : message,
            }
    else:
        instance = ShopRating.objects.filter(shop__pk=shop_pk,customer__user=request.user,is_deleted=False)

        if serialized.is_valid():
            instance.update(
                review = review,
                hygiene = hygiene,
                ambience = ambience,
                customer = customer,
                food_quality = food_quality,
                customer_service = customer_service,
                likely_to_return = likely_to_return,
            )

            response_data = {
                    "StatusCode": 6000,
                    "message": "Updated",
                }

        else:
            message = generate_serializer_errors(serialized._errors)
            response_data = {
                "StatusCode" : 6001,
                "message" : message,
            }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_delivery_partners(request):
    """
    for showing delivery partners
    :param request:
    :return:
    """
    response_data = {}
    pk = request.GET.get("shop_pk")

    if request.GET.get("shop_pk") :
        instance = ShopDelivery.objects.filter(shop__pk=pk,is_deleted=False)
    else:
        instance = ShopDelivery.objects.filter(is_deleted=False)

    serialized = ShopDeliveryPartnerSerializer(instance, many=True, context={"request": request})

    response_data = {
            "StatusCode": 6000,
            "delivery_partners_data": serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def profile_view(request):

    user = Customer.objects.get(user=request.user,is_deleted=False)
    serialized = ProfileSerializer(user, context={"request": request})

    fav_food = FavoriteFood.objects.filter(customer=user,is_favorite=True,is_deleted=False)
    food_serialized = FavoriteFoodSerializer(fav_food, many=True, context={"request": request})

    fav_restaurant = FavoriteRestaurant.objects.filter(customer=user,is_favorite=True,is_deleted=False)
    restaurant_serialized = FavoriteRestaurantSerializer(fav_restaurant, many=True, context={"request": request})

    response_data = {
            "StatusCode": 6000,
            "user_data": serialized.data,
            "food_data": food_serialized.data,
            "restaurant_data": restaurant_serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def app_feedback(request):
    try:
        rating = request.data['rating']
        feedback = request.data['feedback']
    except:
        response_data = {
            "StatusCode" : 6001,
            "title" : "Invalid data",
        }

        return Response(response_data, status=status.HTTP_200_OK)


    customer = Customer.objects.get(user=request.user,is_deleted=False)
    if not AppFeedback.objects.filter(customer=customer).exists():
        serialized = AppFeedbackSerializer(data=request.data)

        if serialized.is_valid():
            data = AppFeedback.objects.create(
                    customer = customer,
                    rating = rating,
                    feedback = feedback,
                )

            response_data = {
                    "StatusCode": 6000,
                    "message": "Success",
                }

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            message = generate_serializer_errors(serialized._errors)
            response_data = {
                "StatusCode" : 6001,
                "message" : message,
            }

    else:
        AppFeedback.objects.filter(customer=customer).update(
            rating = rating,
            feedback = feedback,
            )

        response_data = {
            "StatusCode": 6000,
            "message": "Updated",
            }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def favorite_food_view(request):
    user = Customer.objects.get(user=request.user,is_deleted=False)

    fav_food = FavoriteFood.objects.filter(customer=user,is_favorite=True,is_deleted=False).values_list("shop_dish")
    dish =  ShopDish.objects.filter(pk__in=fav_food,is_deleted=False)
    food_serialized = ShopDishSerializer(dish, many=True, context={"request": request,"user": request.user})

    response_data = {
            "StatusCode": 6000,
            "data": food_serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def favorite_restaurant_view(request):
    try:
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None

    user = Customer.objects.get(user=request.user,is_deleted=False)

    fav_restaurant = FavoriteRestaurant.objects.filter(customer=user,is_favorite=True,is_deleted=False).values_list("shop")
    shop_instance =  Shop.objects.filter(pk__in=fav_restaurant,is_deleted=False)
    restaurant_serialized = ShopSerializer(shop_instance, many=True, context={"request": request,"user_location": user_location,"user": request.user})

    response_data = {
            "StatusCode": 6000,
            "restaurant_data": restaurant_serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def check_favorite(request):

    try:
        category = request.GET.get('category') #category means 2 types food(30) and restaurant(40)
        pk = request.GET.get('pk') #get pk by restaurent or food
    except:
        response_data = {
            "StatusCode" : 6001,
            "title" : "Invalid data",
        }

        return Response(response_data, status=status.HTTP_200_OK)

    if category == "30" :
        if FavoriteFood.objects.filter(dish__pk=pk,customer__user=request.user,is_favorite=True,is_deleted=False).exists():

            response_data = {
                "StatusCode" : 6000,
                "Status" : True,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else :
            response_data = {
                "StatusCode" : 6001,
                "Status" : False,
            }

            return Response(response_data, status=status.HTTP_200_OK)

    elif category == "40" :
        if FavoriteRestaurant.objects.filter(shop__pk=pk,customer__user=request.user,is_favorite=True,is_deleted=False).exists():

            response_data = {
                "StatusCode" : 6000,
                "Status" : True,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else :
            response_data = {
                "StatusCode" : 6001,
                "Status" : False,
            }

            return Response(response_data, status=status.HTTP_200_OK)

    else :
        response_data = {
            "StatusCode" : 6001,
            "message" : "invalid category"
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def favorite(request):

    try:
        category = request.data['category'] #category means 2 types food(30) and restaurant(40)
        pk = request.data['pk'] #get pk by restaurants or food\
        # print(category,type(category))
    except:
        response_data = {
            "StatusCode" : 6001,
            "title" : "Invalid data",
        }

        return Response(response_data, status=status.HTTP_200_OK)

    customer = Customer.objects.get(user=request.user,is_deleted=False)

    if category == "30" :
        pk = request.data['pk'] #get shopdish pk
        shop_dish_instance = ShopDish.objects.get(pk=pk,is_deleted=False)

        favorite_food_instances = FavoriteFood.objects.filter(shop_dish__pk=pk,customer__user=request.user,is_deleted=False)

        if not favorite_food_instances.exists():

            FavoriteFood.objects.create(
                auto_id=get_auto_id(FavoriteFood),
                creator=request.user,
                updater=request.user,
                customer=customer,
                shop_dish=shop_dish_instance,
                is_favorite=True,
                )
            response_data = {
                    "StatusCode": 6000,
                    "title": "Success",
                    "message": "Added To Favorite",
                }

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            if favorite_food_instances.filter(is_favorite=False,).exists():
                favorite_food_instances.update(is_favorite=True)

                response_data = {
                        "StatusCode": 6000,
                        "title": "Success",
                        "message": "Added To Favorite",
                    }

                return Response(response_data, status=status.HTTP_200_OK)

            elif favorite_food_instances.filter(is_favorite=True).exists():
                favorite_food_instances.update(is_favorite=False)

                response_data = {
                        "StatusCode": 6000,
                        "title": "Success",
                        "message": "Removed From Favorite",
                    }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                        "StatusCode": 6001,
                    }

                return Response(response_data, status=status.HTTP_200_OK)

    elif category == "40" :
        favorite_restaurant_instances = FavoriteRestaurant.objects.filter(shop__pk=pk,customer__user=request.user,is_deleted=False)
        restaurant_instances = Shop.objects.get(pk=pk,is_deleted=False)
        # print(restaurant_instances)

        if not favorite_restaurant_instances.exists():

            FavoriteRestaurant.objects.create(
                auto_id=get_auto_id(FavoriteRestaurant),
                creator=request.user,
                updater=request.user,
                shop=restaurant_instances,
                customer=customer,
                is_favorite=True,
                )
            response_data = {
                    "StatusCode": 6000,
                    "title": "Success",
                    "message": "Added To Favorite",
                }

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            if favorite_restaurant_instances.filter(is_favorite=False).exists():

                favorite_restaurant_instances.update(is_favorite=True)

                response_data = {
                        "StatusCode": 6000,
                        "title": "Success",
                        "message": "Added To Favorite",
                    }

                return Response(response_data, status=status.HTTP_200_OK)

            elif favorite_restaurant_instances.filter(is_favorite=True).exists():

                favorite_restaurant_instances.update(is_favorite=False)

                response_data = {
                        "StatusCode": 6000,
                        "title": "Success",
                        "message": "Remove From Favorite",
                    }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                }

                return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "invalid category",
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def dish(request):
    pk = request.GET.get('pk')# dish pk
    if ShopDish.objects.filter(pk=pk,is_deleted=False).exists() :

        instance =  ShopDish.objects.get(pk=pk,is_deleted=False)
        serialized = ShopDishSerializer(instance, context={"request": request})

        response_data = {
                "StatusCode": 6000,
                "data": serialized.data,
            }

        return Response(response_data, status=status.HTTP_200_OK)

    else :
        response_data = {
                "StatusCode": 6001,
                "message": "No Data",
            }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def dish_category(request):
    shop_pk = request.GET.get("shop_pk")

    if ShopDish.objects.filter(shop__pk=shop_pk,is_deleted=False).exists() :
        instances =  DishCategory.objects.filter(is_deleted=False,is_verified=True)
        serialized = DishCategorySerializer(instances, many=True, context={"request": request,"shop_pk": shop_pk})

        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else :
        response_data = {
            "StatusCode": 6001,
            "message": "No Data",
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def dish_list(request):

    try :
        category = request.GET.get("category")
    except :
        category = None
    try :
       shop_pk = request.GET.get("shop_pk")
    except :
        shop_pk = None
    try :
        dietary_type = request.GET.get("dietary_type")
    except :
        dietary_type = None
    try :
        cuisine = request.GET.get("cuisine").split(",")
    except :
        cuisine = None

    instances = ShopDish.objects.filter(dish__is_verified=True,is_deleted=False)

    if ShopDish.objects.filter(dish__is_verified=True,is_deleted=False).exists() :

        if shop_pk :
            instances = instances.filter(shop__pk=shop_pk)

        if cuisine :
            instances = instances.filter(dish__cuisine__pk__in=cuisine)

        if category :
            instances = instances.filter(dish__dish_category__pk=category)

        if dietary_type:
            instances = instances.filter(dish__dietary_type=dietary_type)

        serialized = ShopDishSerializer(instances, many=True, context={"request": request,"shop_pk": shop_pk})

        response_data = {
            "StatusCode": 6000,
            "total-count": instances.count(),
            "data": serialized.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else :
        response_data = {
            "StatusCode": 6001,
            "message": "No Data",
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_map_view(request):
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


    category = request.GET.get('category')
    badge = request.GET.get('badge')
    distence = request.GET.get('distence')
    dietary_type = request.GET.get('dietary_type')
    avg_price_for_two = request.GET.get('max_avg_price_for_two')

    try:
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
    except:
        user_location = None

    instances = ShopDish.objects.filter(is_deleted=False,shop__is_verified=True)

    if cuisine:
        instances = instances.filter(dish__cuisine__in=cuisine)

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

    shops = instances.values_list("shop__pk")
    instances = Shop.objects.filter(pk__in=shops)

    if user_location:
        # print("------")
        instances = instances.annotate(distance=Distance('located', user_location)
                          ).order_by('distance')

    serialized = ShopMapLocationSerializer(instances, many=True, context={"request": request,"user_location": user_location,"user": request.user})

    response_data = {
        "StatusCode": 6000,
        "total-count": instances.count(),
        "data": serialized.data,
        }

    return Response(response_data, status=status.HTTP_200_OK)
