from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register-number/$', views.register_number, name='register_number'),
    url(r'^otp-verify/$', views.verify_otp, name='verify_otp'),
    url(r'^register/$', views.register, name='register'),
    url(r'^send-otp/$', views.send_otp, name='send_otp'),
    url(r'^login-with-otp/$', views.login_with_otp, name='login_with_otp'),
    
    # url(r'^change-password/$', views.change_password, name='change_password'),
    # url(r'^login-with-password/$', views.login_with_password, name='login_with_password'),
    # url(r'^reset-password/$', views.reset_password, name='reset_password'),
    # url(r'^change-number/$', views.change_number, name='change_number'),
    # url(r'^change-number-update/$', views.change_number_update, name='change_number_update'),

    url(r'^get-profile/$', views.get_profile, name='get_profile'),
    
    url(r'^check-email/$', views.check_email, name='check_email'),
    url(r'^verify-email/$', views.verify_email, name='verify_email'),
    url(r'^update-profile/$', views.update_profile, name='update_profile'),
    url(r'^update-profile-image/$', views.update_profile_image, name='update_profile_image'),

]
