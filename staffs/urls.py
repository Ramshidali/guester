from django.urls import path, re_path
from django.conf.urls import url

from staffs import views

app_name = 'staffs'

urlpatterns = [
    re_path(r'^designation-create/$', views.designation_create, name='designation_create'),
    re_path(r'^designation-edit/(?P<pk>.*)/$', views.designation_edit, name='designation_edit'),
    re_path(r'^designation-delete/(?P<pk>.*)/$', views.designation_delete, name='designation_delete'),
    re_path(r'^designations/$', views.designations, name='designations'),
    re_path(r'^designation/(?P<pk>.*)/$', views.designation, name='designation'),
    
    re_path(r'^designations/autocomplete/$', views.DesignationAutoComplete.as_view(), name='autocomplete_designation'),
    
    re_path(r'^set-permissions/(?P<pk>.*)/$',views.set_permissions, name='set_permissions'),
    re_path(r'^update-permissions/(?P<pk>.*)/$',views.update_permissions, name='update_permissions'),
    re_path(r'^update-password/(?P<pk>.*)/$',views.update_password, name='update_password'),
    
    
    re_path(r'^staff-create/$', views.staff_create, name='staff_create'),
    re_path(r'^staff-edit/(?P<pk>.*)/$', views.staff_edit, name='staff_edit'),
    re_path(r'^staff-delete/(?P<pk>.*)/$', views.staff_delete, name='staff_delete'),
    re_path(r'^staffs/$', views.staffs, name='staffs'),
    re_path(r'^staff/(?P<pk>.*)/$', views.staff, name='staff'),
    
    re_path(r'^activities/(?P<pk>.*)/$', views.activities, name='activities'),
    re_path(r'^activity/(?P<pk>.*)/$', views.activity, name='activity'),
    
    re_path(r'^revoke-staff/(?P<pk>.*)/$', views.revoke_staff, name='revoke_staff'),
    re_path(r'^grant-staff/(?P<pk>.*)/$', views.grant_staff, name='grant_staff'),
]