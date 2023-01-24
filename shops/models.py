from decimal import Decimal

# from django.db import models
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from main.models import BaseModel
from main.variables import phone_regex


CATEGORY =(
    ("10","Customer Service"),
    ("20","Food Quality"),
    ("30","Likely to Return"),
    ("40","Ambience"),
    ("50","Hygiene"),
)

FILE_TYPE =(
    ("10","Image"),
    ("20","Video"),
)

OFFER_TYPE =(
    ("10","Rs"),
    ("20","Percentage"),
)


class ShopType(BaseModel):
    name = models.CharField(max_length=128 )
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="shops/", blank=True, null=True)
    icon = models.ImageField(upload_to="shops/", blank=True, null=True)

    class Meta:
        db_table = 'shop_type'
        verbose_name = ('shop_type')
        verbose_name_plural = ('shop_type')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class Zone(BaseModel):
    zone = models.CharField(max_length=128,unique=True)

    class Meta:
        db_table = 'shop_zone'
        verbose_name = ('shop_zone')
        verbose_name_plural = ('shop_zones')
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.zone)


class SubZone(BaseModel):
    name = models.CharField(max_length=128,unique=True)
    zone = models.ForeignKey('shops.Zone',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table = 'shop_sub_zone'
        verbose_name = ('shop_sub_zone')
        verbose_name_plural = ('shop_sub_zones')
        ordering = ('name',)

    def __str__(self):
        return str(self.name)


class Shop(BaseModel):
    name = models.CharField(max_length=128 )
    image = models.ImageField(upload_to="shops/")
    phone = models.CharField(max_length=15 ,validators=[phone_regex],)
    logo = models.ImageField(upload_to="shops/", blank=True, null=True)
    address = models.CharField(max_length=128,blank=True,null=True )
    location = models.ForeignKey("general.Location",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE,null=True,blank=True)
    email=models.EmailField()
    rating = models.PositiveIntegerField(default=5,validators=[MinValueValidator(1), MaxValueValidator(5)])
    brand = models.ForeignKey('brands.Brand',on_delete=models.CASCADE,blank=True,null=True)
    badge = models.ForeignKey('general.Badge',on_delete=models.CASCADE,blank=True,null=True)
    is_guester_assured = models.BooleanField(default=False)
    average_cost_for_two = models.DecimalField(default=0.00,decimal_places=0, max_digits=15,validators=[MinValueValidator(Decimal('0'))])
    website_link = models.CharField(max_length=128)
    shop_type = models.ForeignKey('shops.ShopType',on_delete=models.CASCADE,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    owner_name = models.CharField(max_length=128,blank=True,null=True )
    manager_name =models.CharField(max_length=128,blank=True,null=True )
    contact_number= models.CharField(max_length=15 ,validators=[phone_regex],blank=True,null=True)
    is_updated = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    rejected_reason =models.TextField(max_length=255,blank=True,null=True)
    zone = models.ForeignKey('shops.Zone',on_delete=models.CASCADE,blank=True,null=True)
    sub_zone = models.ForeignKey('shops.SubZone',on_delete=models.CASCADE,blank=True,null=True)

    located = models.PointField(blank=True, null=True)
    shop_timing = models.ManyToManyField('shops.ShopTiming')

    class Meta:
        db_table = 'shop'
        verbose_name = ('shop')
        verbose_name_plural = ('shops')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class ShopWorkingDay(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    day = models.ForeignKey('general.Days',on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()


    class Meta:
        db_table = 'shop_working_day'
        verbose_name = ('shop_working_day')
        verbose_name_plural = ('shop_working_days')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.day)


class ShopSafetyPrecaution(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    title = models.CharField(max_length=128)

    class Meta:
        db_table = 'shop_safety'
        verbose_name = ('shop_safety')
        verbose_name_plural = ('shop_safety')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class ShopGalleryType(BaseModel):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'shop_gallery_type'
        verbose_name = ('shop_gallery_type')
        verbose_name_plural = ('shop_gallery_type')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class ShopGallery(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    gallery_type = models.ForeignKey('shops.ShopGalleryType',on_delete=models.CASCADE)
    file_type =models.CharField(max_length=128,choices=FILE_TYPE)
    file = models.FileField(upload_to="shops/")
    thumbnail = models.ImageField(upload_to="shop-gallery/", blank=True, null=True)

    class Meta:
        db_table = 'shop_gallery'
        verbose_name = ('shop_gallery')
        verbose_name_plural = ('shop_gallery')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.shop)


class ShopRating(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    customer = models.ForeignKey('customers.Customer',on_delete=models.CASCADE)
    review = models.CharField(max_length=500)
    customer_service = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    food_quality = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    likely_to_return = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    ambience = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    hygiene = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        db_table = 'shop_rating'
        verbose_name = ('shop_rating')
        verbose_name_plural = ('shop_rating')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.shop)

    def rating(self):
        total_rating =  self.customer_service + self.food_quality + self.likely_to_return + self.ambience +  self.hygiene
        if total_rating:
            rating = total_rating / 5
        else :
            rating = 0

        return rating


class ShopDish(BaseModel):
    price = models.DecimalField(default=0.00,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    dish = models.ForeignKey('dishes.Dish',on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to="shops/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'shop_dish'
        verbose_name = ('shop_dish')
        verbose_name_plural = ('shop_dish')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.dish)

    def offer_price(self):
        if DishOffer.objects.filter(shop_dish=self.pk,is_active=True).exists() :
            offer = DishOffer.objects.get(shop_dish=self.pk,is_active=True)

            # offer type 10 = Rs , 20 = Percentage
            if offer.offer_type == "10":
                offer_price = self.price - int(offer.offer)

            if offer.offer_type == "20":
                offer_price = ((self.price * int(offer.offer))/100)
                offer_price = self.price - offer_price

            return str(offer_price)
        else :
            return None


class ShopDishImage(BaseModel):
    shop_dish = models.ForeignKey('shops.ShopDish',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shops/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'shop_dish_image'
        verbose_name = ('shop_dish_image')
        verbose_name_plural = ('shop_dish_image')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.shop_dish)


class DishOffer(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    shop_dish = models.ForeignKey('shops.ShopDish',on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    offer_type = models.CharField(max_length=128,choices=OFFER_TYPE)
    offer = models.CharField(max_length=128)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'dish_offer'
        verbose_name = ('dish_offer')
        verbose_name_plural = ('dish_offers')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.shop_dish)


class ShopDelivery(BaseModel):
    delivery_partner = models.ForeignKey('general.Delivery',on_delete=models.CASCADE)
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    shop_link = models.CharField(max_length=128,blank=True, null=True)

    class Meta:
            db_table = 'delivery_link'
            verbose_name = ('delivery link')
            verbose_name_plural = ('delivery links')
            ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class MoreOffer(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    icon = models.ImageField(upload_to="shops/")
    is_featured = models.BooleanField(default=False)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255)


    class Meta:
        db_table = 'more_offer'
        verbose_name = ('more_offer')
        verbose_name_plural = ('more_offers')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class ShopOffer(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shops/", blank=True, null=True)
    title = models.CharField(max_length=128)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'shop_offer'
        verbose_name = ('shop_offer')
        verbose_name_plural = ('shop_offers')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class BrandOffer(BaseModel):
    brand = models.ForeignKey('brands.Brand',on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to="shops/", blank=True, null=True)
    title = models.CharField(max_length=128)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'brand_offer'
        verbose_name = ('brand_offer')
        verbose_name_plural = ('brand_offers')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class ShopStory(BaseModel):
    customer = models.ForeignKey('customers.Customer',on_delete=models.CASCADE,blank=True,null=True)
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shops/stories", blank=True, null=True)
    video = models.FileField(upload_to="shops/stories", blank=True, null=True)


    class Meta:
        db_table = 'shop_story'
        verbose_name = ('shop_story')
        verbose_name_plural = ('shop_story')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class ShopAdmin(BaseModel):
    shop = models.OneToOneField('shops.Shop',on_delete=models.CASCADE)
    user = models.ForeignKey(
        "auth.User", blank=True, related_name="user_%(class)s_objects", on_delete=models.CASCADE)
    password= models.CharField(max_length=256)
    permission = models.ManyToManyField('users.Permission', blank=True)

    class Meta:
        db_table = 'shop_admin'
        verbose_name = ('shop_admin')
        verbose_name_plural = ('shop_admin')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.shop)


class ShopTiming(BaseModel):
    timing =models.CharField(max_length=255)

    class Meta:
        db_table = 'shop_timing'
        verbose_name = ('shop_timing')
        verbose_name_plural = ('shop_timings')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.timing)


class ShopFacility(BaseModel):
    shop = models.ForeignKey('shops.Shop',on_delete=models.CASCADE)
    facility = models.ForeignKey('general.Facility',on_delete=models.CASCADE)
    description =models.TextField(max_length=255,blank=True,null=True)
    image_1 = models.ImageField(upload_to="shops/", blank=True, null=True)
    image_2 = models.ImageField(upload_to="shops/", blank=True, null=True)
    image_3 = models.ImageField(upload_to="shops/", blank=True, null=True)

    class Meta:
        db_table = 'shop_facility'
        verbose_name = ('shop_facility')
        verbose_name_plural = ('shop_facilities')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.shop)