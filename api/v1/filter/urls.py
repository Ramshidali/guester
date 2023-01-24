from django.conf.urls import url,re_path

from . import views

urlpatterns = [
    re_path(r'^filters/$', views.get_filters, name='get_filters'),
    re_path(r'^filter-cuisine/$', views.filter_cuisine, name='filter_cuisine'),
    re_path(r'^apply-filters/$', views.apply_filter, name='apply_filter'),
    
    re_path(r'^search/$', views.search, name='search'),
    re_path(r'^save-search/$', views.save_search, name='save_search'),
    re_path(r'^get-search/$', views.get_search, name='get_search'),
    
    re_path(r'^save-location/$', views.save_location, name='save_location'),
]
