from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from main.functions import get_current_role
from staffs.models import Staff
from shops.models import ShopAdmin
import json


def role_required(roles):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            current_role = get_current_role(request)
            if not current_role in roles:
                if request.is_ajax():
                    response_data = {
                        "status": "false",
                        "stable": "true",
                        "title": "Permission Denied",
                        "message": "You have no permission to do this action."
                    }
                    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                else:
                    context = {
                        "title": "Permission Denied"
                    }
                    return render(request, 'errors/403.html', context)

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def ajax_required(function):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return render(request,'error/400.html',{})
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap


def permissions_required(permissions, roles=['staff'], all_permissions=False, all_roles=False, both_check=True, super_user_ok=True, allow_self=False, model=None):
    
    def _method_wrapper(view_method):

        def _arguments_wrapper(request, *args, **kwargs):
            has_permission = False
            if request.user.is_superuser:
                has_permission = True
            elif Staff.objects.filter(is_deleted=False, user=request.user).exists():
                staff = Staff.objects.get(is_deleted=False, user=request.user)
                staff_permissions = staff.permission.all()
                for p in staff_permissions:
                    if p.code in permissions:
                        has_permission = True
            elif ShopAdmin.objects.filter(is_deleted=False, user=request.user).exists():
                shop_admin = ShopAdmin.objects.get(is_deleted=False, user=request.user)
                shop_admin_permissions = shop_admin.permission.all()
                for p in shop_admin_permissions:
                    if p.code in permissions:
                        has_permission = True

            if not has_permission:
                if request.is_ajax():
                    response_data = {}
                    response_data['status'] = 'false'
                    response_data['stable'] = 'true'
                    response_data['title'] = 'Permission Denied'
                    response_data['message'] = "You have no permission to do this action."
                    response_data['static_message'] = "true"
                    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                else:
                    context = {
                    }
                    return render(request, 'errors/403.html', context)

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper