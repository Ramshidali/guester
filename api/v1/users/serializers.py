from datetime import datetime
from urllib import request
from customers.models import AppFeedback, Customer, FavoriteFood, FavoriteRestaurant
from dishes.models import Cuisine, Dish, DishCategory, DishImage
from rest_framework import serializers
from shops.models import BrandOffer, MoreOffer, ShopDelivery, ShopDish, ShopDishImage, ShopFacility, ShopGallery, ShopGalleryType,ShopOffer,Shop, ShopRating, ShopSafetyPrecaution, ShopStory, ShopWorkingDay
from brands.models import Brand
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Sum
# import googlemaps


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('name','image','logo')


class BrandoffersSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    brand_pk = serializers.SerializerMethodField()

    class Meta:
        model = BrandOffer
        fields = ('id','brand_name','brand_pk','title','image')

    def get_brand_name(self,instance):
        return instance.brand.name

    def get_brand_pk(self,instance):
        return instance.brand.pk


class ShopOfferSerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField()
    shop_rating = serializers.SerializerMethodField()

    class Meta:
        model = ShopOffer
        fields = ('id','title','image','shop_name','shop_rating')

    def get_shop_name(self,instance):
        return instance.shop.name

    def get_shop_rating(self,instance):
        return instance.shop.rating


class OfferShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ('id','name','image','location','rating')


class ShopSerializer(serializers.ModelSerializer):
    total_review = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ('id','name','logo','image','location','average_cost_for_two','rating','total_review','distance','location_name','is_favorite','category')

    def get_location_name(self,instance):
        return instance.location.short_name

    def get_total_review(self,instance):
        total_reviews = ShopRating.objects.filter(shop=instance.pk,is_deleted=False).count()
        return total_reviews

    def get_distance(self,instance):
        try:
            user_location = self.context.get("user_location")
            distance = Shop.objects.filter(pk=instance.pk,is_deleted=False,is_verified=True).annotate(distance=Distance('located', user_location)
                                ).first().distance
            distance_km =round(distance.km,2)
            # print(distance.km,"===========",type(distance))
            if distance_km <= 0.0 :
                distance = round(distance.mi)
                return f"{distance} mi"
            elif distance_km < 1 :
                distance = round(distance.m)
                return f"{distance} m"
            else :
                return f"{distance_km} km"
        except:
            return None

    def get_is_favorite(self,instance):
        request = self.context.get("request")
        if Customer.objects.filter(user__username=request.user,is_deleted=False).exists():
            customer = Customer.objects.get(user__username=request.user,is_deleted=False)
            if FavoriteRestaurant.objects.filter(shop__pk=instance.pk,customer=customer,is_deleted=False,is_favorite=True).exists():
                return True
            else:
                return False
        else:
            return False

    def get_category(self,instance):
        return "40"


class MoreOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoreOffer
        fields = ('id','shop','icon','is_featured','title','description')


class ShopGallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopGallery
        fields = ('file_type','file','thumbnail')


class ShopGalleryTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopGalleryType
        fields = ('id','name')


class ShopFacilitySerializer(serializers.ModelSerializer):
    facility_id = serializers.SerializerMethodField()
    facility_title = serializers.SerializerMethodField()
    facility_icon = serializers.SerializerMethodField()

    class Meta:
        model = ShopFacility
        fields = ('id','shop','facility_id','facility_title','facility_icon','description','image_1','image_2','image_3')

    def get_facility_id(self,instance):
        return instance.facility.pk

    def get_facility_title(self,instance):
        return instance.facility.title

    def get_facility_icon(self,instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.facility.icon.url)


class ShopSafetySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopSafetyPrecaution
        fields = ['title']


class ShopViewSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    working_time = serializers.SerializerMethodField()
    working_status = serializers.SerializerMethodField()
    working_message = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    badge = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        exclude = ('auto_id','creator','updater','date_added','date_updated','is_deleted','is_updated','is_rejected','rejected_reason','zone','sub_zone','located','shop_type')

    def get_location(self,instance):
        return instance.location.short_name

    def get_latitude(self,instance):
        return float(instance.location.latitude)

    def get_longitude(self,instance):
        return float(instance.location.longitude)

    def get_working_time(self,instance):
        working_time = self.context.get("working_time")
        return working_time

    def get_working_status(self,instance):
        working_status = self.context.get("working_status")
        return working_status

    def get_working_message(self,instance):
        working_message = self.context.get("working_message")
        return working_message

    def get_total_reviews(self,instance):
        return ShopRating.objects.filter(shop=instance.pk,is_deleted=False).count()

    def get_distance(self,instance):
        try:
            user_location = self.context.get("user_location")
            distance = Shop.objects.filter(pk=instance.pk,is_deleted=False,is_verified=True).annotate(distance=Distance('located', user_location)
                                ).first().distance
            distance_km =round(distance.km,2)
            # print(distance.km,"===========",type(distance))
            if distance_km <= 0.0 :
                distance = round(distance.mi)
                return f"{distance} mi"
            elif distance_km < 1 :
                distance = round(distance.m)
                return f"{distance} m"
            else :
                return f"{distance_km} km"
        except:
            return None

    def get_category(self,instance):
        return "40"

    def get_badge(self,instance):
        request = self.context.get('request')
        if instance.badge.icon:
            icon = request.build_absolute_uri(instance.badge.icon.url)
        else:
            icon = ""
        return {
            "id" : instance.badge.id,
            "title" : instance.badge.title,
            "icon" : icon,
        }


class ShopWorkingHoursSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = ShopWorkingDay
        fields = ['day','start_time','end_time']

    def get_day(self,instance):
        return instance.day.day

    def get_start_time(self,instance):
        return instance.start_time.strftime("%I:%M %p")

    def get_end_time(self,instance):
        return instance.end_time.strftime("%I:%M %p")


class ShopCuisinesSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField()

    class Meta:
        model = Cuisine
        fields = ['id','name','image','type','type_name']

    def get_type_name(self,instance):
        return instance.get_type_display()


class ShopStorySerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField()
    shop_location_name = serializers.SerializerMethodField()
    shop_latitude = serializers.SerializerMethodField()
    shop_longitude = serializers.SerializerMethodField()

    class Meta:
        model = ShopStory
        fields = ('customer','shop','image','video','shop_name','shop_location_name','shop_latitude','shop_longitude')

    def get_shop_name(self, instance) :
        return self.shop.name

    def get_shop_location_name(self, instance) :
        return self.shop.location.short_name

    def get_shop_latitude(self, instance) :
        return self.shop.location.latitude

    def get_shop_longitude(self, instance) :
        return self.shop.location.longitude


class ShopRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopRating
        fields = ('review','customer_service','food_quality','likely_to_return','ambience','hygiene')


class ShopDeliveryPartnerSerializer(serializers.ModelSerializer):
    delivery_partner_name = serializers.SerializerMethodField()
    delivery_partner_logo = serializers.SerializerMethodField()

    class Meta:
        model = ShopDelivery
        fields = ('shop_link','delivery_partner_name','delivery_partner_logo')

    def get_delivery_partner_name(self,instance) :
        return instance.delivery_partner.name

    def get_delivery_partner_logo(self,instance) :
        request = self.context.get('request')
        return request.build_absolute_uri(instance.delivery_partner.logo.url)


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_image = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = ShopRating
        fields = ['customer_name','customer_image','review','date','avg_rating']

    def get_customer_name(self,instance):
        return instance.customer.name

    def get_customer_image(self,instance):
        request = self.context.get('request')
        if instance.customer.photo:
            image = request.build_absolute_uri(instance.customer.photo.url)
        else:
            image = ""
        return image

    def get_date(self,instance) :
        return instance.date_added.strftime("%d/%b/%Y")

    def get_avg_rating(self,instance):
        request = self.context.get('request')
        try :
            instances = ShopRating.objects.filter(shop__pk=instance.shop.pk,is_deleted=False)
            customer_service = instances.aggregate(Sum('customer_service')).get('customer_service__sum')
            food_quality = instances.aggregate(Sum('food_quality')).get('food_quality__sum')
            likely_to_return = instances.aggregate(Sum('likely_to_return')).get('likely_to_return__sum')
            ambience = instances.aggregate(Sum('ambience')).get('ambience__sum')
            hygiene = instances.aggregate(Sum('hygiene')).get('hygiene__sum')

            total_rating =  customer_service + food_quality + likely_to_return + ambience +  hygiene
            total_rating_count = instances.count()

            return {
                "total_review": total_rating_count,
                "total_rating": round((total_rating / total_rating_count) / 5, 1),
            }
        except:
            return {
                "total_review": 0,
                "total_rating": 0,
            }


class ProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('name','phone','location','latitude','longitude','photo')

    def get_photo(self, instance):
        if instance.photo :
            request = self.context.get('request')
            image_url = instance.photo.url
            return request.build_absolute_uri(image_url)
        else:
            None


class ProfileImageSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['photo']

    def get_photo(self, instance):
        request = self.context.get('request')
        image_url = instance.photo.url
        return request.build_absolute_uri(image_url)


class DishImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ShopDishImage
        fields = ['id','image']

    def get_image(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url
        return request.build_absolute_uri(image_url)


class ShopDishSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    more_images = serializers.SerializerMethodField()
    dietary_type_id = serializers.SerializerMethodField()
    dietary_type_name = serializers.SerializerMethodField()
    dish_pk = serializers.SerializerMethodField()
    dish_timing_id = serializers.SerializerMethodField()
    dish_timing_name = serializers.SerializerMethodField()
    dish_category_id = serializers.SerializerMethodField()
    dish_category_name = serializers.SerializerMethodField()
    dish_cuisin_name = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    offer_price = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    shop_pk = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    shop_location = serializers.SerializerMethodField()
    avg_price_of_two = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = ShopDish
        fields = ('id','name','description','dietary_type_id','dietary_type_name','dish_pk','dish_timing_id','dish_timing_name',
                  'dish_category_id','dish_category_name','dish_cuisin_name','is_verified','image','more_images','amount','offer_price',
                  'is_favorite','shop_pk','shop_name','logo',
                  'shop_location','avg_price_of_two','avg_rating','distance')

    def get_more_images(self,instance):
        request = self.context.get('request')
        if ShopDishImage.objects.filter(shop_dish__dish__pk=instance.dish.pk,is_deleted=False).exists():
            instances = ShopDishImage.objects.filter(shop_dish__dish__pk=instance.dish.pk,is_deleted=False)
            return DishImageSerializer(instances, many=True, context={"request": request}).serialized.data

    def get_name(self,instance):
        return instance.dish.name

    def get_dietary_type_id(self,instance):
        return instance.dish.dietary_type

    def get_dietary_type_name(self,instance):
        return instance.dish.get_dietary_type_display()

    def get_dish_cuisin_name(self,instance):
        return instance.dish.cuisine.name

    def get_amount(self,instance):
        return instance.price

    def get_offer_price(self,instance):
        return instance.offer_price()

    def get_dish_pk(self,instance):
        return instance.dish.pk

    def get_dish_timing_id(self,instance):
        return instance.dish.dish_timing

    def get_dish_timing_name(self,instance):
        return instance.dish.get_dish_timing_display()

    def get_dish_category_id(self,instance):
        return instance.dish.dish_category.pk

    def get_dish_category_name(self,instance):
        return instance.dish.dish_category.name

    def get_is_verified(self,instance):
        return instance.dish.is_verified

    def get_image(self,instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.dish.image.url)

    def get_more_images(self,instance):
        return instance.dish.name

    def get_is_favorite(self,instance):
        request = self.context.get('request')
        if Customer.objects.filter(user__username=request.user,is_deleted=False).exists():
            if FavoriteFood.objects.filter(customer__user=request.user,shop_dish=instance.pk,is_favorite=True,is_deleted=False).exists():
                return True
            else:
                return False
        else:
            return False

    def get_shop_pk(self,instance):
        return instance.shop.pk

    def get_shop_name(self,instance):
        return instance.shop.name

    def get_logo(self,instance):
        try:
            request = self.context.get('request')
            url = request.build_absolute_uri(instance.shop.logo.url)
        except :
            url = None
        return url

    def get_shop_location(self,instance):
        return instance.shop.location.short_name

    def get_avg_price_of_two(self,instance):
        return instance.shop.average_cost_for_two

    def get_avg_rating(self,instance):
        try :
            instances = ShopRating.objects.filter(shop__pk=instance.shop.pk,is_deleted=False)
            customer_service = instances.aggregate(Sum('customer_service')).get('customer_service__sum')
            food_quality = instances.aggregate(Sum('food_quality')).get('food_quality__sum')
            likely_to_return = instances.aggregate(Sum('likely_to_return')).get('likely_to_return__sum')
            ambience = instances.aggregate(Sum('ambience')).get('ambience__sum')
            hygiene = instances.aggregate(Sum('hygiene')).get('hygiene__sum')

            total_rating =  customer_service + food_quality + likely_to_return + ambience +  hygiene
            total_rating_count = instances.count()

            return {
                "total_review": total_rating_count,
                "total_rating": round((total_rating / total_rating_count) / 5, 1),
            }
        except:
            return {
                "total_review": 0,
                "total_rating": 0,
            }

    def get_distance(self,instance):
        try:
            user_location = self.context.get("user_location")
            distance = Shop.objects.filter(pk=instance.shop.pk,is_deleted=False,is_verified=True).annotate(distance=Distance('located', user_location)
                                ).first().distance
            distance_km =round(distance.km,2)
            # print(distance.km,"===========",type(distance))
            if distance_km <= 0.0 :
                distance = round(distance.mi)
                return f"{distance} mi"
            elif distance_km < 1 :
                distance = round(distance.m)
                return f"{distance} m"
            else :
                return f"{distance_km} km"
        except:
            return None


class FavoriteFoodSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteFood
        fields = ('dish','is_favorite','category')

    def get_category(self,instance):
        return "30"


class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteRestaurant
        exclude = ('auto_id','creator','updater','date_added','date_updated','is_deleted')

    def get_category(self,instance):
        return "40"


class DishSerializer(serializers.ModelSerializer):
    more_images = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id','name','dietary_type','dish_timing','dish_category','is_verified','image','more_images','amount','is_favorite','category')

    def get_more_images(self,instance):
        request = self.context.get('request')
        if ShopDishImage.objects.filter(shop_dish__dish__pk=instance.pk,is_deleted=False).exists():
            instances = ShopDishImage.objects.filter(shop_dish__dish__pk=instance.pk,is_deleted=False)
            return DishImageSerializer(instances, many=True, context={"request": request}).data

    def get_amount(self,instance):
        if not self.context.get('shop_pk') is None :
            shop_pk = self.context.get('shop_pk')
            # print(shop_pk,"ppppp")
            return ShopDish.objects.get(dish__pk=instance.pk,shop__pk=shop_pk,is_deleted=False).price
        else:
            return None

    def get_is_favorite(self,instance):
        request = self.context.get('request')

        if request.user.is_authenticated:
            if FavoriteFood.objects.filter(customer__user=request.user,shop_dish__dish__pk=instance.pk,is_favorite=True,is_deleted=False).exists():
                return True
            else:
                return False
        else:
            return False

    def get_category(self,instance):
        return "30"


class DishCategorySerializer(serializers.ModelSerializer):
    total_dish = serializers.SerializerMethodField()

    class Meta:
        model = DishCategory
        fields = ('id','name','total_dish')

    def get_total_dish(self,instance):
        request = self.context.get('request')
        shop_pk = self.context.get('shop_pk')
        return ShopDish.objects.filter(shop_id=shop_pk,dish__dish_category=instance,is_deleted=False,dish__is_verified=True).count()


class ShopMapLocationSerializer(serializers.ModelSerializer):
    coordinate = serializers.SerializerMethodField()
    total_review = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ('coordinate','id','name','logo','image','location','average_cost_for_two','rating','total_review','distance','location_name','is_favorite','category')

    def get_coordinate(self,instance):
        return {
                "latitude" : float(instance.location.latitude),
                "longitude" : float(instance.location.longitude),
            }

    def get_location_name(self,instance):
        return instance.location.short_name

    def get_total_review(self,instance):
        total_reviews = ShopRating.objects.filter(shop=instance.pk,is_deleted=False).count()
        return total_reviews

    def get_distance(self,instance):
        try:
            user_location = self.context.get("user_location")
            distance = Shop.objects.filter(pk=instance.pk,is_deleted=False,is_verified=True).annotate(distance=Distance('located', user_location)
                                ).first().distance
            distance_km =round(distance.km,2)
            # print(distance.km,"===========",type(distance))
            if distance_km <= 0.0 :
                distance = round(distance.mi)
                return f"{distance} mi"
            elif distance_km < 1 :
                distance = round(distance.m)
                return f"{distance} m"
            else :
                return f"{distance_km} km"
        except:
            return None

    def get_is_favorite(self,instance):
        request = self.context.get("request")
        if Customer.objects.filter(user__username=request.user,is_deleted=False).exists():
            customer = Customer.objects.get(user__username=request.user,is_deleted=False)
            if FavoriteRestaurant.objects.filter(shop__pk=instance.pk,customer=customer,is_deleted=False,is_favorite=True).exists():
                return True
            else:
                return False
        else:
            return False

    def get_category(self,instance):
        return "40"


class AppFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppFeedback
        fields = ['rating','feedback']


