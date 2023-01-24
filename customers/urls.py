from django.urls import path, re_path
from django.conf.urls import url
from customers import views

app_name = 'customers'

urlpatterns = [
    # re_path(r'^customer-delete/(?P<pk>.*)/$', views.customer_delete, name='customer_delete'),
    re_path(r'^customers/$', views.customers, name='customers'),
    re_path(r'^customer/(?P<pk>.*)/$', views.customer, name='customer'),
    re_path(r'^revoke-customer/(?P<pk>.*)/$', views.revoke_customer, name='revoke_customer'),
    re_path(r'^grant-customer/(?P<pk>.*)/$', views.grant_customer, name='grant_customer'),
]