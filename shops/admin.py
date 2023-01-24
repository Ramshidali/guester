from django.contrib import admin
from shops.models import *
# Register your models here.

admin.site.register(Shop)
admin.site.register(ShopType)
admin.site.register(ShopGallery)
admin.site.register(ShopDelivery)
admin.site.register(ShopWorkingDay)
admin.site.register(ShopSafetyPrecaution)
admin.site.register(DishOffer)
admin.site.register(MoreOffer)
admin.site.register(ShopOffer)
admin.site.register(ShopRating)
admin.site.register(ShopDish)
admin.site.register(ShopDishImage)
admin.site.register(BrandOffer)
admin.site.register(ShopStory)
admin.site.register(Zone)

class ShopAdminAdmin(admin.ModelAdmin):
    list_display = ['user','shop']
admin.site.register(ShopAdmin, ShopAdminAdmin)
