from django.urls import path, re_path
from django.conf.urls import url

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    re_path(r'^shop-dish-create/$', views.shop_dish_create, name='shop_dish_create'),
    re_path(r'^shop-dish-edit/(?P<pk>.*)/$', views.shop_dish_edit, name='shop_dish_edit'),
    re_path(r'^shop-dish-delete/(?P<pk>.*)/$', views.shop_dish_delete, name='shop_dish_delete'),
    re_path(r'^shop-dish/(?P<pk>.*)/$', views.shop_dish, name='shop_dish'),
    re_path(r'^shop-dishes/$', views.shop_dishes, name='shop_dishes'),
    
    re_path(r'^dish-image-create/(?P<pk>.*)$', views.dish_image_create, name='dish_image_create'),
    re_path(r'^dish-image-delete/(?P<pk>.*)/$', views.dish_image_delete, name='dish_image_delete'),
    
    re_path(r'^dish-offer-create/$', views.dish_offer_create, name='dish_offer_create'),
    re_path(r'^dish-offer-edit/(?P<pk>.*)/$', views.dish_offer_edit, name='dish_offer_edit'),
    re_path(r'^dish-offer-delete/(?P<pk>.*)/$', views.dish_offer_delete, name='dish_offer_delete'),
    re_path(r'^dish-offers/$', views.dish_offers, name='dish_offers'),
    
    re_path(r'^more-offer-create/$', views.more_offer_create, name='more_offer_create'),
    re_path(r'^more-offer-edit/(?P<pk>.*)/$', views.more_offer_edit, name='more_offer_edit'),
    re_path(r'^more-offer-delete/(?P<pk>.*)/$', views.more_offer_delete, name='more_offer_delete'),
    re_path(r'^more-offers/$', views.more_offers, name='more_offers'),
    
    re_path(r'^gallery-create/$', views.gallery_create, name='gallery_create'),
    re_path(r'^gallery-delete/(?P<pk>.*)/$', views.gallery_delete, name='gallery_delete'),
    re_path(r'^shop-gallery/$', views.shop_gallery, name='shop_gallery'),
    
    re_path(r'^shop-facility-create/$', views.shop_facility_create, name='shop_facility_create'),
    re_path(r'^shop-facility-edit/(?P<pk>.*)/$', views.shop_facility_edit, name='shop_facility_edit'),
    re_path(r'^shop-facility-delete/(?P<pk>.*)/$', views.shop_facility_delete, name='shop_facility_delete'),
    re_path(r'^shop-facility/(?P<pk>.*)/$', views.shop_facility, name='shop_facility'),
    re_path(r'^shop-facilities/$', views.shop_facilities, name='shop_facilities'),
    
    re_path(r'^precaution-create/$', views.precaution_create, name='precaution_create'),
    re_path(r'^precaution-edit/(?P<pk>.*)/$', views.precaution_edit, name='precaution_edit'),
    re_path(r'^precaution-delete/(?P<pk>.*)/$', views.precaution_delete, name='precaution_delete'),
    re_path(r'^precautions/$', views.precautions, name='precautions'),
    
    re_path(r'^delivery-partner-create/$', views.delivery_partner_create, name='delivery_partner_create'),
    re_path(r'^delivery-partner-edit/(?P<pk>.*)/$', views.delivery_partner_edit, name='delivery_partner_edit'),
    re_path(r'^delivery-partner-delete/(?P<pk>.*)/$', views.delivery_partner_delete, name='delivery_partner_delete'),
    re_path(r'^delivery-partners/$', views.delivery_partners, name='delivery_partners'),
    
    re_path(r'^shop-review-delete/(?P<pk>.*)/$', views.shop_review_delete, name='shop_review_delete'),
    re_path(r'^shop-reviews/$', views.shop_reviews, name='shop_reviews'),
    re_path(r'^shop-review/(?P<pk>.*)/$', views.shop_review, name='shop_review'),
    
    re_path(r'^shop-offer-create/$', views.shop_offer_create, name='shop_offer_create'),
    re_path(r'^shop-offer-edit/(?P<pk>.*)/$', views.shop_offer_edit, name='shop_offer_edit'),
    re_path(r'^shop-offer-delete/(?P<pk>.*)/$', views.shop_offer_delete, name='shop_offer_delete'),
    re_path(r'^shop-offers/$', views.shop_offers, name='shop_offers'),
    re_path(r'^shop-offer/(?P<pk>.*)/$', views.shop_offer, name='shop_offer'),
]
