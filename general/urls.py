from django.urls import path, re_path
from django.conf.urls import url
from general import views

app_name = 'general'

urlpatterns = [
    re_path(r'^badge/autocomplete/$', views.BadgeAutoComplete.as_view(), name='autocomplete_badge'),
    
    re_path(r'^facility-create/$', views.facility_create, name='facility_create'),
    re_path(r'^facility-edit/(?P<pk>.*)/$', views.facility_edit, name='facility_edit'),
    re_path(r'^facility-delete/(?P<pk>.*)/$', views.facility_delete, name='facility_delete'),
    re_path(r'^facilities/$', views.facilities, name='facilities'),
    re_path(r'^facility/(?P<pk>.*)/$', views.facility, name='facility'),
    
    re_path(r'^badge-create/$', views.badge_create, name='badge_create'),
    re_path(r'^badge-edit/(?P<pk>.*)/$', views.badge_edit, name='badge_edit'),
    re_path(r'^badge-delete/(?P<pk>.*)/$', views.badge_delete, name='badge_delete'),
    re_path(r'^badges/$', views.badges, name='badges'),
    re_path(r'^badge/(?P<pk>.*)/$', views.badge, name='badge'),
    
    re_path(r'^day-create/$', views.day_create, name='day_create'),
    re_path(r'^day-edit/(?P<pk>.*)/$', views.day_edit, name='day_edit'),
    re_path(r'^day-delete/(?P<pk>.*)/$', views.day_delete, name='day_delete'),
    re_path(r'^days/$', views.days, name='days'),
    re_path(r'^day/(?P<pk>.*)/$', views.day, name='day'),
    
    re_path(r'^delivery-create/$', views.delivery_create, name='delivery_create'),
    re_path(r'^delivery-edit/(?P<pk>.*)/$', views.delivery_edit, name='delivery_edit'),
    re_path(r'^delivery-delete/(?P<pk>.*)/$', views.delivery_delete, name='delivery_delete'),
    re_path(r'^delivery-partners/$', views.delivery_partners, name='delivery_partners'),
    re_path(r'^delivery/(?P<pk>.*)/$', views.delivery, name='delivery'),
    
    re_path(r'^location-create/$', views.location_create, name='location_create'),
    re_path(r'^location-edit/(?P<pk>.*)/$', views.location_edit, name='location_edit'),
    re_path(r'^location-delete/(?P<pk>.*)/$', views.location_delete, name='location_delete'),
    re_path(r'^locations/$', views.locations, name='locations'),
    re_path(r'^location/(?P<pk>.*)/$', views.location, name='location'),
    
    re_path(r'^spotlight-create/$', views.spotlight_create, name='spotlight_create'),
    re_path(r'^spotlight-edit/(?P<pk>.*)/$', views.spotlight_edit, name='spotlight_edit'),
    re_path(r'^spotlight-delete/(?P<pk>.*)/$', views.spotlight_delete, name='spotlight_delete'),
    re_path(r'^spotlights/$', views.spotlights, name='spotlights'),
    re_path(r'^spotlight/(?P<pk>.*)/$', views.spotlight, name='spotlight'),
]