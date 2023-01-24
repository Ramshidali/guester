from django.contrib import admin

from dishes.models import Cuisine, Dish, DishImage

# Register your models here.
admin.site.register(Dish)
admin.site.register(DishImage)
admin.site.register(Cuisine)