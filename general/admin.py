from django.contrib import admin

from general.models import Location, UserActivity

# Register your models here.
admin.site.register(Location)
admin.site.register(UserActivity)