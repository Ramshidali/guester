from django.urls import path, re_path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^profile/$', views.profile, name='profile'),
]
