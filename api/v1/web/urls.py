from django.conf.urls import url
from django.urls import path,re_path,include

from . import views

urlpatterns = [
    re_path(r'^categories/$', views.categories_view, name='categories_view'),
]
