
from django.urls import path, re_path
from users import views

app_name = "users"


urlpatterns = [
    path('login/', views.login_enter, name='login'),
    path('logout/', views.user_logout, name='logout'),
]