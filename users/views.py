from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date, time
from main.functions import get_auto_id, generate_form_errors, get_otp
from main.decorators import ajax_required
import json
from staffs.models import StaffAuth,Staff
from users.forms import LoginForm
from django.contrib.auth import login as auth_login
from users.forms import *
from django.http import JsonResponse
from django.conf import settings
import datetime
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, login, logout, authenticate


def login_enter(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            print("****************",username)
            
            user = authenticate(username=username, password=password)
            
            if not user:
                message = "Staff  with this username and password does not exist."
                
                response_data = {
                    'status': 'false',
                    'stable': 'true',
                    "redirect": 'true',
                    'redirect_url': reverse('main:index'),
                    'title': "User not exists",
                    "message": message
                }
            else:
                staff = Staff.objects.get(user__username=username)
                
                auth_process = StaffAuth.objects.create(
                    staff = staff,
                    auth_type = "10",
                    auto_id = get_auto_id(StaffAuth)
                )
                auth_process.save()
                
                auth_login(request, user)
                response_data = {

                    'status': 'success',
                    'stable': 'false',
                    "redirect": 'true',
                    "message": 'Successfully Logged in',
                    'redirect_url': reverse('main:index'),
                }

        else:

            response_data = {
                'status': 'false',
                'stable': 'false',
                'title': "Invalid Credential",
                "message": message,
                "redirect": 'false',
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        
        form = LoginForm()
        context = {
            "title": "Login",
            "form": form,
            # "url" : reverse('users:login')
        }
        return render(request, 'registration/staff_login.html', context)


def user_logout(request):
    user = request.user
    staff = Staff.objects.get(user__username=user)
    
    auth_process = StaffAuth.objects.create(
        staff = staff,
        auth_type = "20",
        auto_id = get_auto_id(StaffAuth)
    )
    auth_process.save()
    
    logout(request)
    context = {

    }
    return render(request, 'registration/staff_login.html', context)
