from dataclasses import field
from django.db import models

from customers.models import Customer
from dishes.models import Dish
from main.models import BaseModel
from shops.models import Shop


class Facility(BaseModel):
    title = models.CharField(max_length=128 )
    icon = models.FileField(upload_to="facility/")

    class Meta:
        db_table = 'facility'
        verbose_name = ('facility')
        verbose_name_plural = ('facility')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)
    
    
class Badge(BaseModel):
    title = models.CharField(max_length=128 )
    icon = models.FileField(upload_to="badge/")
    description = models.TextField()

    class Meta:
        db_table = 'description'
        verbose_name = ('description')
        verbose_name_plural = ('description')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)
    
    
class Days(BaseModel):
    day = models.CharField(max_length=10)

    class Meta:
        db_table = 'days'
        verbose_name = ('days')
        verbose_name_plural = ('days')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.day)
    
    
class Delivery(BaseModel):
    name = models.CharField(max_length=128 )
    logo = models.FileField(upload_to="shops/")
    
    class Meta:
            db_table = 'delivery_partner'
            verbose_name = ('delivery partner')
            verbose_name_plural = ('delivery partners')
            ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)
    
    
class Phone(models.Model):
    phone = models.TextField(max_length=125)

    class Meta:
        db_table = 'phone'
        verbose_name = 'phone'
        verbose_name_plural = 'phone'

    def __int__(self):
        return self.phone
    
    
class Location(BaseModel):
    location = models.CharField(max_length=128, null=True)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    class Meta:
        db_table = 'general_location'
        verbose_name = ('Location')
        verbose_name_plural = ('Locations')
        ordering = ('location',)

    def __str__(self):
        return str(self.location)
    
    
class Spotlight(BaseModel):
    image = models.ImageField(upload_to="Spotlight/" )

    class Meta:
        db_table = 'spotlight'
        verbose_name = ('spotlight')
        verbose_name_plural = ('spotlights')
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.auto_id)
    
    
class RecentSearches(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    keys = models.CharField(max_length=200)

    class Meta:
        ordering = ('date_added',)
        verbose_name = 'recent search'
        verbose_name_plural = 'recent searches'
        

class RecentLocation(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    class Meta:
        ordering = ('date_updated',)
        verbose_name = 'recent locations'
        verbose_name_plural = 'recent locations'
        
        
class UserActivity(models.Model):
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(max_length=128)
    app = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    instance = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_activity'
        verbose_name = ('user activity')
        verbose_name_plural = ('user activities')
        ordering = ('-time',)
        
    class Admin:
        list_display = ('shop','user','time','activity_type','app')
        
    def __str__(self):
        return "%s - %s" %(self.title, self.user)
