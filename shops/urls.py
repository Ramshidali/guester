from django.urls import path, re_path
from django.conf.urls import url
from shops import views

app_name = 'shops'

urlpatterns = [
    re_path(r'^shops-types/autocomplete/$', views.ShopTypeAutoComplete.as_view(), name='autocomplete_shop_type'),
    re_path(r'^gallery-types/autocomplete/$', views.GalleryTypeAutoComplete.as_view(), name='autocomplete_gallery_type'),
    re_path(r'^facilities/autocomplete/$', views.FacilityAutoComplete.as_view(), name='facility_autocomplete'),
    re_path(r'^delivery/autocomplete/$', views.DeliveryAutoComplete.as_view(), name='autocomplete_delivery'),
    re_path(r'^dish/autocomplete/$', views.DishAutoComplete.as_view(), name='autocomplete_dish'),
    re_path(r'^day/autocomplete/$', views.DayAutoComplete.as_view(), name='autocomplete_day'),
    re_path(r'^shop-dish/autocomplete/$', views.ShopDishAutoComplete.as_view(), name='autocomplete_shop_dish'),
    re_path(r'^shop/autocomplete/$', views.ShopAutoComplete.as_view(), name='autocomplete_shop'),
    re_path(r'^zone/autocomplete/$', views.ZoneAutoComplete.as_view(), name='zone_autocomplete'),
    re_path(r'^sub-zone/autocomplete/$', views.SubZoneAutoComplete.as_view(), name='autocomplete_sub_zone'),
    re_path(r'^shop-timing/autocomplete/$', views.ShopTimingAutoComplete.as_view(), name='autocomplete_shop_timing'),
    
    re_path(r'^upload-shops/$', views.upload_shops, name='upload_shops'),
    re_path(r'^shops/$', views.shops, name='shops'),
    re_path(r'^shop-create/$', views.shop_create, name='shop_create'),
    re_path(r'^shop-update/(?P<pk>.*)/$', views.shop_update, name='shop_update'),
    re_path(r'^shop-edit/(?P<pk>.*)/$', views.shop_edit, name='shop_edit'),
    re_path(r'^shop-verify/(?P<pk>.*)/$', views.shop_verify, name='shop_verify'),
    re_path(r'^shop-reject/(?P<pk>.*)/$', views.shop_reject, name='shop_reject'),  
    re_path(r'^shop-delete/(?P<pk>.*)/$', views.shop_delete, name='shop_delete'),
    re_path(r'^shop/(?P<pk>.*)/$', views.shop, name='shop'),
    
    re_path(r'^add-working-days/(?P<pk>.*)/$', views.add_working_days, name='add_working_days'),
    re_path(r'^edit-working-day/(?P<pk>.*)/$', views.edit_working_day, name='edit_working_day'),
    re_path(r'^delete-working-day/(?P<pk>.*)/$', views.delete_working_day, name='delete_working_day'),
    
    re_path(r'^shop-type-create/$', views.shop_type_create, name='shop_type_create'),
    re_path(r'^shop-type-edit/(?P<pk>.*)/$', views.shop_type_edit, name='shop_type_edit'),
    re_path(r'^shop-type-delete/(?P<pk>.*)/$', views.shop_type_delete, name='shop_type_delete'),
    re_path(r'^shop-types/$', views.shop_types, name='shop_types'),
    re_path(r'^shop-type/(?P<pk>.*)/$', views.shop_type, name='shop_type'),
    
    re_path(r'^shop-timing-create/$', views.shop_timing_create, name='shop_timing_create'),
    re_path(r'^shop-timing-edit/(?P<pk>.*)/$', views.shop_timing_edit, name='shop_timing_edit'),
    re_path(r'^shop-timing-delete/(?P<pk>.*)/$', views.shop_timing_delete, name='shop_timing_delete'),
    re_path(r'^shop-timings/$', views.shop_timings, name='shop_timings'),
    re_path(r'^shop-timing/(?P<pk>.*)/$', views.shop_timing, name='shop_timing'),
    
    re_path(r'^gallery-type-create/$', views.gallery_type_create, name='gallery_type_create'),
    re_path(r'^gallery-type-edit/(?P<pk>.*)/$', views.gallery_type_edit, name='gallery_type_edit'),
    re_path(r'^gallery-type-delete/(?P<pk>.*)/$', views.gallery_type_delete, name='gallery_type_delete'),
    re_path(r'^gallery-types/$', views.gallery_types, name='gallery_types'),
    re_path(r'^gallery-type/(?P<pk>.*)/$', views.gallery_type, name='gallery_type'),
    
    re_path(r'^gallery-create/(?P<pk>.*)/$', views.gallery_create, name='gallery_create'),
    re_path(r'^gallery-delete/(?P<pk>.*)/$', views.gallery_delete, name='gallery_delete'),
    re_path(r'^gallery-edit/(?P<pk>.*)/$', views.gallery_edit, name='gallery_edit'),
    
    re_path(r'^delivery-partner-create/(?P<pk>.*)$', views.delivery_partner_create, name='delivery_partner_create'),
    re_path(r'^delivery-partner-edit/(?P<pk>.*)/$', views.delivery_partner_edit, name='delivery_partner_edit'),
    re_path(r'^delivery-partner-delete/(?P<pk>.*)/$', views.delivery_partner_delete, name='delivery_partner_delete'),
    re_path(r'^delivery-partners/$', views.delivery_partners, name='delivery_partners'),
    re_path(r'^delivery-partner/(?P<pk>.*)/$', views.delivery_partner, name='delivery_partner'),
    
    re_path(r'^shop-dish-create/(?P<pk>.*)$', views.shop_dish_create, name='shop_dish_create'),
    re_path(r'^shop-dish-edit/(?P<pk>.*)/$', views.shop_dish_edit, name='shop_dish_edit'),
    re_path(r'^shop-dish-delete/(?P<pk>.*)/$', views.shop_dish_delete, name='shop_dish_delete'),
    re_path(r'^shop-dish/(?P<pk>.*)/$', views.shop_dish, name='shop_dish'),
    
    re_path(r'^dish-image-create/(?P<pk>.*)$', views.dish_image_create, name='dish_image_create'),
    re_path(r'^dish-image-delete/(?P<pk>.*)/$', views.dish_image_delete, name='dish_image_delete'),
    
    re_path(r'^dish-offer-create/(?P<pk>.*)$', views.dish_offer_create, name='dish_offer_create'),
    re_path(r'^dish-offer-edit/(?P<pk>.*)/$', views.dish_offer_edit, name='dish_offer_edit'),
    re_path(r'^dish-offer-delete/(?P<pk>.*)/$', views.dish_offer_delete, name='dish_offer_delete'),
    
    re_path(r'^precaution-create/(?P<pk>.*)$', views.precaution_create, name='precaution_create'),
    re_path(r'^precaution-edit/(?P<pk>.*)/$', views.precaution_edit, name='precaution_edit'),
    re_path(r'^precaution-delete/(?P<pk>.*)/$', views.precaution_delete, name='precaution_delete'),
    
    re_path(r'^more-offer-create/(?P<pk>.*)$', views.more_offer_create, name='more_offer_create'),
    re_path(r'^more-offer-edit/(?P<pk>.*)/$', views.more_offer_edit, name='more_offer_edit'),
    re_path(r'^more-offer-delete/(?P<pk>.*)/$', views.more_offer_delete, name='more_offer_delete'),
    
    re_path(r'^dish-create/$', views.dish_create, name='dish_create'),
    
    re_path(r'^shop-offer-create/$', views.shop_offer_create, name='shop_offer_create'),
    re_path(r'^shop-offer-edit/(?P<pk>.*)/$', views.shop_offer_edit, name='shop_offer_edit'),
    re_path(r'^shop-offer-delete/(?P<pk>.*)/$', views.shop_offer_delete, name='shop_offer_delete'),
    re_path(r'^shop-offers/$', views.shop_offers, name='shop_offers'),
    re_path(r'^shop-offer/(?P<pk>.*)/$', views.shop_offer, name='shop_offer'),
    
    re_path(r'^brand-offer-create/$', views.brand_offer_create, name='brand_offer_create'),
    re_path(r'^brand-offer-edit/(?P<pk>.*)/$', views.brand_offer_edit, name='brand_offer_edit'),
    re_path(r'^brand-offer-delete/(?P<pk>.*)/$', views.brand_offer_delete, name='brand_offer_delete'),
    re_path(r'^brand-offers/$', views.brand_offers, name='brand_offers'),
    re_path(r'^brand-offer/(?P<pk>.*)/$', views.brand_offer, name='brand_offer'),
    
    
    re_path(r'^shop-review-delete/(?P<pk>.*)/$', views.shop_review_delete, name='shop_review_delete'),
    re_path(r'^shop-reviews/$', views.shop_reviews, name='shop_reviews'),
    re_path(r'^shop-review/(?P<pk>.*)/$', views.shop_review, name='shop_review'),
    
    re_path(r'^shop-admin-create/(?P<pk>.*)$', views.shop_admin_create, name='shop_admin_create'),
    re_path(r'^set-permissions/(?P<pk>.*)/$',views.set_permissions, name='set_permissions'),
    
    re_path(r'^zone-create/$', views.zone_create, name='zone_create'),
    re_path(r'^zone-edit/(?P<pk>.*)/$', views.zone_edit, name='zone_edit'),
    re_path(r'^zone-delete/(?P<pk>.*)/$', views.zone_delete, name='zone_delete'),
    re_path(r'^zones/$', views.zones, name='zones'),
    re_path(r'^zone/(?P<pk>.*)/$', views.zone, name='zone'),
    
    re_path(r'^sub-zone-create/$', views.sub_zone_create, name='sub_zone_create'),
    re_path(r'^sub-zone-edit/(?P<pk>.*)/$', views.sub_zone_edit, name='sub_zone_edit'),
    re_path(r'^sub-zone-delete/(?P<pk>.*)/$', views.sub_zone_delete, name='sub_zone_delete'),
    re_path(r'^sub-zones/$', views.sub_zones, name='sub_zones'),
    re_path(r'^sub-zone/(?P<pk>.*)/$', views.sub_zone, name='sub_zone'),
    
    re_path(r'^shop-facility-create/(?P<pk>.*)$', views.shop_facility_create, name='shop_facility_create'),
    re_path(r'^shop-facility-edit/(?P<pk>.*)/$', views.shop_facility_edit, name='shop_facility_edit'),
    re_path(r'^shop-facility-delete/(?P<pk>.*)/$', views.shop_facility_delete, name='shop_facility_delete'),
    re_path(r'^shop-facility/(?P<pk>.*)/$', views.shop_facility, name='shop_facility'),
]