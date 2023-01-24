from django.urls import path, re_path
from django.conf.urls import url
from dishes import views

app_name = 'dishes'

urlpatterns = [
    re_path(r'^cuisine/autocomplete/$', views.CuisineAutoComplete.as_view(), name='autocomplete_cuisine'),
    re_path(r'^dish-category/autocomplete/$', views.DishCategoryAutoComplete.as_view(), name='autocomplete_dish_category'),
    
    re_path(r'^cuisine-create/$', views.cuisine_create, name='cuisine_create'),
    re_path(r'^cuisine-edit/(?P<pk>.*)/$', views.cuisine_edit, name='cuisine_edit'),
    re_path(r'^cuisine-delete/(?P<pk>.*)/$', views.cuisine_delete, name='cuisine_delete'),
    re_path(r'^cuisines/$', views.cuisines, name='cuisines'),
    re_path(r'^cuisine/(?P<pk>.*)/$', views.cuisine, name='cuisine'),
    
    re_path(r'^dish-category-create/$', views.dish_category_create, name='dish_category_create'),
    re_path(r'^dish-category-edit/(?P<pk>.*)/$', views.dish_category_edit, name='dish_category_edit'),
    re_path(r'^dish-category-delete/(?P<pk>.*)/$', views.dish_category_delete, name='dish_category_delete'),
    re_path(r'^dish-categories/$', views.dish_categories, name='dish_categories'),
    re_path(r'^dish-category/(?P<pk>.*)/$', views.dish_category, name='dish_category'),
    
    re_path(r'^dish-create/$', views.dish_create, name='dish_create'),
    re_path(r'^dish-edit/(?P<pk>.*)/$', views.dish_edit, name='dish_edit'),
    re_path(r'^dish-delete/(?P<pk>.*)/$', views.dish_delete, name='dish_delete'),
    re_path(r'^dishes/$', views.dishes, name='dishes'),
    re_path(r'^dish/(?P<pk>.*)/$', views.dish, name='dish'),
    
    re_path(r'^upload-dishes/$', views.upload_dishes, name='upload_dishes'),
]