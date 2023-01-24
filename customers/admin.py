from django.contrib import admin
from customers.models import Customer, FavoriteFood, FavoriteRestaurant, Otp

admin.site.register(Customer)
admin.site.register(FavoriteFood)
admin.site.register(FavoriteRestaurant)
admin.site.register(Otp)
