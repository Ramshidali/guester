from versatileimagefield.fields import VersatileImageField

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from main.models import BaseModel
from dishes.models import Dish
from main.variables import phone_regex
from shops.models import Shop, ShopDish


class Customer(BaseModel):
    name = models.CharField(max_length=128 )
    phone = models.CharField(max_length=15, validators=[phone_regex],)
    email = models.EmailField(null=True,blank=True)
    location = models.CharField(max_length=128 )
    latitude = models.CharField(max_length=128 )
    longitude = models.CharField(max_length=128 )
    photo = VersatileImageField('Image', upload_to="Customer/profile")
    user = models.ForeignKey(
        "auth.User", blank=True, related_name="user_%(class)s_objects", on_delete=models.CASCADE)
    password = models.CharField(max_length=256)
    otp = models.CharField(max_length=4, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'customer'
        verbose_name = ('customer')
        verbose_name_plural = ('customers')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.phone)
    
    
class Otp(models.Model):
    phone = models.CharField(max_length=256, null=False)
    otp = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('phone', )
        verbose_name = 'otp'
        verbose_name_plural = 'otp'

    def __str__(self):
        return self.phone
    
    
class OtpMail(models.Model):
    email = models.EmailField(max_length=256, null=False)
    otp = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('email', )
        verbose_name = 'email otp'
        verbose_name_plural = 'email otp'

    def __str__(self):
        return self.email


class FavoriteFood(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shop_dish = models.ForeignKey(ShopDish, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        db_table = 'favorite_food'
        verbose_name = ('Favorite Food')
        verbose_name_plural = ('Favorite Food')
        ordering = ('auto_id', )

    def __str__(self):
        return f'{self.customer.name} - {self.shop_dish.dish}'
    

class FavoriteRestaurant(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        db_table = 'favorite_Restaurant'
        verbose_name = ('Favorite Restaurant')
        verbose_name_plural = ('Favorite Restaurant')
        ordering = ('auto_id', )

    def __str__(self):
        return f'{self.customer.name} - {self.shop.name}'
    
    
class AppFeedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback =models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        db_table = 'feedback'
        verbose_name = ('feedback')
        verbose_name_plural = ('feedbacks')
        ordering = ('-date_added', )

    def __str__(self):
        return str(self.customer)