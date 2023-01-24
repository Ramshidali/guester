from django.conf.urls import re_path


from . import views

urlpatterns = [
    re_path(r'^spotlight/$', views.spotlight, name='spotlight'),
    re_path(r'^shop-type/$', views.shop_type, name='shop_type'),
]
