from django.conf.urls import url, re_path

from . import views

urlpatterns = [
    re_path(r'^brands/$', views.brands, name='brands'),
    re_path(r'^restaurants/$', views.restaurents, name='restaurants'),
    re_path(r'^restaurant-offers/$', views.restaurant_offers, name='restaurant_offers'),

    re_path(r'^dish/$', views.dish, name='dish'),
    re_path(r'^dish-list/$', views.dish_list, name='dish_list'),
    re_path(r'^dish-category/$', views.dish_category, name='dish_category'),

    re_path(r'^shop-view/$', views.shop_view, name='shop_view'),
    re_path(r'^shops-list/$', views.shops_list, name='shops_list'),
    re_path(r'^shop-dishes/$', views.shop_dishes_view, name='shop_dish'),
    re_path(r'^shop-offers/$', views.shop_offers, name='shop_offers'),
    re_path(r'^shop-stories/$', views.shop_stories, name='shop_stories'),

    re_path(r'^shop-gallery/$', views.shop_gallery_view, name='shop_gallery'),
    re_path(r'^shop-gallery-types/$', views.shop_gallery_types, name='shop_gallery_types'),

    re_path(r'^shop-facility/$', views.shop_facility_view, name='shop_stories'),
    re_path(r'^shop-cuisines/$', views.shop_cuisines, name='shop_cuisines'),
    re_path(r'^shop-map-view/$', views.shop_map_view, name='shop_map_view'),
    re_path(r'^shop-delivery-partner/$', views.shop_delivery_partners, name='shop_delivery_partners'),

    re_path(r'^shop-reviews/$', views.shop_rating, name='shop_reviews'),
    re_path(r'^post-shop-review/$', views.post_review, name='post_review'),

    re_path(r'^profile/$', views.profile_view, name='profile'),
    re_path(r'^app-feedback/$', views.app_feedback, name='app_feedback'),


    re_path(r'^favorite/$', views.favorite, name='favorite'),
    re_path(r'^favorite-food/$', views.favorite_food_view, name='favorite_food'),
    re_path(r'^check-favorite/$', views.check_favorite, name='check_favorite'),
    re_path(r'^favorite-restaurant/$', views.favorite_restaurant_view, name='favorite_restaurant'),
]