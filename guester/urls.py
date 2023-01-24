from django.conf.urls import url
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve
from main import views as general_views
from guester import settings
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Guester API",
      default_version='v1.0.0',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('',include(('main.urls'),namespace='main')),
    path('',general_views.app,name='app'),
    path('api-auth/', include('rest_framework.urls')),

    path('app/shops/',include(('shops.urls'),namespace='shops')),
    path('app/dishes/',include(('dishes.urls'),namespace='dishes')),
    path('app/general/',include(('general.urls'),namespace='general')),
    path('app/staffs/',include(('staffs.urls'),namespace='staffs')),
    path('app/customers/',include(('customers.urls'),namespace='customers')),
    path('app/brands/',include(('brands.urls'),namespace='brands')),
    path('app/dashboard/',include(('dashboard.urls'),namespace='dashboard')),
    path('app/users/',include(('users.urls'),namespace='users')),

    re_path('api/v1/auth/', include(('api.v1.authentication.urls', 'authentication'), namespace='api_v1_authentication')),
    re_path('api/v1/register/',include(('api.v1.registrations.urls', 'registrations'), namespace='api_v1_registrations')),
    re_path('api/v1/users/',include(('api.v1.users.urls', 'users'), namespace='api_v1_users')),
    re_path('api/v1/general/',include(('api.v1.general.urls', 'general'), namespace='api_v1_general')),
    re_path('api/v1/shop/',include(('api.v1.shop.urls', 'shop'), namespace='api_v1_shop')),
    re_path('api/v1/dish/',include(('api.v1.dish.urls', 'dish'), namespace='api_v1_dish')),
    re_path('api/v1/offers/',include(('api.v1.offers.urls', 'offers'), namespace='api_v1_offers')),
    re_path('api/v1/filter/',include(('api.v1.filter.urls', 'filter'), namespace='api_v1_filter')),
    re_path('api/v1/web/',include(('api.v1.web.urls', 'web'), namespace='api_v1_web')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]

handler404 = 'guester.views.page_not_found_view'
# handler500 = 'guester.views.my_custom_error_view'
handler403 = 'guester.views.permission_denied_view'
