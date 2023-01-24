from django.urls import path, re_path
from django.conf.urls import url
from brands import views

app_name = 'brands'

urlpatterns = [
    re_path(r'^brand-create/$', views.brand_create, name='brand_create'),
    re_path(r'^brand-edit/(?P<pk>.*)/$', views.brand_edit, name='brand_edit'),
    re_path(r'^brand-delete/(?P<pk>.*)/$', views.brand_delete, name='brand_delete'),
    re_path(r'^brands/$', views.brands, name='brands'),
    re_path(r'^brand/(?P<pk>.*)/$', views.brand, name='brand'),
    
    re_path(r'^brands/autocomplete/$', views.BrandAutoComplete.as_view(), name='autocomplete_brand'),
]