from django.db import models

from main.models import BaseModel
from main.variables import phone_regex

DIETARY_TYPE =(
    ("10", "Veg"),
    ("20", "Non-veg"),
)

CUISINE_TYPE =(
    ("10", "National"),
    ("20", "International"),
)

DISH_TIMING =(
    ("30", "Breakfast"),
    ("40", "Lunch"),
    ("50", "Dinner"),
    ("60", "All"),
)


class Cuisine(BaseModel):
    name = models.CharField(max_length=128 )
    image = models.ImageField(upload_to="Dishes/", blank=True, null=True)
    type = models.CharField(max_length=128, choices=CUISINE_TYPE)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'cuisine'
        verbose_name = ('cuisine')
        verbose_name_plural = ('cuisines')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class DishCategory(BaseModel):
    name = models.CharField(max_length=128 )
    image = models.ImageField(upload_to="Dishes/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'dish_category'
        verbose_name = ('dish_category')
        verbose_name_plural = ('dish_categories')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class Dish(BaseModel):
    name = models.CharField(max_length=128 )
    image = models.ImageField(upload_to="Dishes/", blank=True, null=True )
    is_verified = models.BooleanField(default=False)
    cuisine = models.ForeignKey('dishes.Cuisine', on_delete=models.CASCADE)
    dish_category = models.ForeignKey('dishes.DishCategory', on_delete=models.CASCADE)
    dish_timing = models.CharField(max_length=128, choices=DISH_TIMING, blank=True, null=True)
    dietary_type =models.CharField(max_length=128, choices=DIETARY_TYPE)

    class Meta:
        db_table = 'dish'
        verbose_name = ('dish')
        verbose_name_plural = ('dishes')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class DishImage(BaseModel):
    image = models.ImageField(upload_to="Dishes/", )
    dish = models.ForeignKey('dishes.Dish', on_delete=models.CASCADE)

    class Meta:
        db_table = 'dish_image'
        verbose_name = ('dish_image')
        verbose_name_plural = ('dish_images')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.dish)