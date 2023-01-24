import json
import datetime

from dal import autocomplete

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from main.decorators import role_required, ajax_required, permissions_required
from main.functions import generate_form_errors, get_auto_id
from staffs.models import *
from main.functions import decrypt_message, encrypt_message, get_auto_id, get_otp
from staffs.forms import *
from staffs.permissions import  get_available_permissions, get_allowed_permissions
from general.models import UserActivity

class DesignationAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return StaffDesignation.objects.none()

        items = StaffDesignation.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )

        return items


@login_required
@permissions_required(['can_create_staff_designation'])
def designation_create(request):
    if request.method == 'POST':
        form = DesignationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(StaffDesignation)
            data.creator = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.name,
                title = "Created an Designation",
            )
            activity.save()

            response_data = {
                "status": "success", 
                "stable": "false", 
                "title": "Successfully Created", 
                "message": "Designation created successfully.", 
                "redirect": "true", 
                "redirect_url": reverse('staffs:set_permissions', kwargs={'pk': data.pk})
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false", 
                "title": "Failed", 
                "message": message, 
            }
            
        return JsonResponse(response_data)

    form = DesignationForm()
    context = {
        'form': form, 
        'page_name': 'Create Designation', 
        'app_name': 'Staffs', 
        'page_title': 'Create Designation', 
        'redirect': 'true', 
        "redirect_url": reverse('staffs:designations'), 
        'is_designation' : True,
    }
    
    return render(request, 'dashboard/staffs/designation_entry.html', context)


@login_required
@permissions_required(['can_manage_staff_designation'])
def designations(request):
    instances = StaffDesignation.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(name__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Designations', 
        'app_name' :'Staffs', 
        'page_title' : 'Designations', 
        'filter_data' : filter_data,
        'is_designation' : True,
    }
    
    return render(request, 'dashboard/staffs/designations.html', context)


@login_required
@permissions_required(['can_view_staff_designation'])
def designation(request, pk):
    instance = StaffDesignation.objects.get(pk=pk, is_deleted=False)
    permissions = instance.permission.all()
    
    general_permissions = permissions.filter(app="general")
    dish_permissions = permissions.filter(app="dishes")
    brand_permissions = permissions.filter(app="brands")
    shop_permissions = permissions.filter(app="shops")
    staff_permissions = permissions.filter(app="staffs")
    user_permissions = permissions.filter(app="users")
    
    context = {
        'permissions' : permissions, 
        'instance': instance, 
        'page_name' : 'Designation', 
        'app_name' :'Staffs', 
        'page_title' : 'Designation', 
        'is_need_light_box' : True, 
        "general_permissions": general_permissions, 
        "brand_permissions": brand_permissions, 
        "dish_permissions": dish_permissions, 
        "shop_permissions": shop_permissions, 
        "staff_permissions": staff_permissions, 
        "user_permissions": user_permissions, 
        'is_designation' : True,
    }
         
    return render(request, 'dashboard/staffs/designation.html', context)


@login_required
@permissions_required(['can_modify_staff_designation'])
def designation_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(StaffDesignation.objects.filter(pk=pk))
        form = DesignationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.name,
                title = "Updated an Designation",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Designation Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('staffs:designation', kwargs={"pk": data.pk})
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status" : "false", 
                "stable" : "true", 
                "title" : "Form validation error", 
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        instance = get_object_or_404(StaffDesignation.objects.filter(pk=pk))
        form = DesignationForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Staffs', 
            "page_title" : "Edit Designation", 
            "redirect" : True, 
            "url" : reverse('staffs:designation_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_designation' : True,
        }

        return render(request, 'dashboard/staffs/designation_entry.html', context)


@login_required
@permissions_required(['can_delete_staff_designation'])
@ajax_required
def designation_delete(request, pk):
    data = StaffDesignation.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.name,
        title = "Deleted an Designation",
    )
    activity.save()
    
    StaffDesignation.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Designation Deleted", 
        "message" : "Designation Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('staffs:designations')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_set_permissions'])
def set_permissions(request, pk):
    instance = get_object_or_404(StaffDesignation.objects.filter(pk=pk, is_deleted=False))

    if request.method == 'POST':
        permissions = request.POST.getlist('permission')
        instance.permission.clear()

        for item in permissions:
            p = Permission.objects.get(pk=item)
            instance.permission.add(p)

        response_data = {
            "status": "success", 
            "stable": "false", 
            "title": "Successfully Updated", 
            "message": "Permissions Updated successfully.", 
            "redirect": "true", 
            "redirect_url": reverse('staffs:designation', kwargs={'pk': instance.pk})
        }
        
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        array_p = list(instance.permission.all().values_list('pk', flat=True))

        permissions = Permission.objects.all()
        general_permissions = permissions.filter(app="general")
        dish_permissions = permissions.filter(app="dishes")
        brand_permissions = permissions.filter(app="brands")
        shop_permissions = permissions.filter(app="shops")
        staff_permissions = permissions.filter(app="staffs")
        user_permissions = permissions.filter(app="users")

        context = {
            "is_edit": True, 
            "array_p": array_p, 
            "instance": instance, 
            'page_name': 'Designation Permission', 
            'app_name': 'Staffs', 
            'page_title': 'Designation Permission', 
            "url": reverse('staffs:set_permissions', kwargs={'pk': instance.pk}), 
            "general_permissions": general_permissions, 
            "brand_permissions": brand_permissions, 
            "dish_permissions": dish_permissions, 
            "shop_permissions": shop_permissions, 
            "staff_permissions": staff_permissions, 
            "user_permissions": user_permissions, 
        }
        
        return render(request, 'dashboard/staffs/set_permissions.html', context)


@login_required
@permissions_required(['can_create_staff'])
def staff_create(request):
    
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)
        
        if form.is_valid() and user_form.is_valid():
            auto_id = get_auto_id(Staff)
            data = form.save(commit=False)
            data.password =user_form.cleaned_data["password1"]
            
            group, created=Group.objects.get_or_create(name="staff")
            user_data = user_form.save()
            user_data.groups.add(group)
            
            instance = user_data
            data.creator = request.user
            
            data.updater = request.user
            data.auto_id = auto_id
            data.user = user_data
            data.is_active = True
            
            data.email = user_data.email
            data.save()
            data.permission.set(data.designation.permission.all())
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.name,
                title = "Created an Staff",
            )
            activity.save()

            response_data = {
                "status": "success", 
                "stable" : "false", 
                "title": "Successfully Created", 
                "message": "Staff created successfully.", 
                "redirect": "true", 
                "redirect_url": reverse('staffs:staff', kwargs={'pk': data.pk})
            }
        else:
            message = generate_form_errors(form, formset=False)
            message += generate_form_errors(user_form, formset=False)
            response_data = {
                "status": "false", 
                "stable": "true", 
                "title": "Form validation error", 
                "message": str(message)
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = StaffForm()
        user_form = UserForm()

        context = {
            "form": form, 
            "user_form": user_form, 
            'page_name': 'Create Staff', 
            'app_name' :'Staffs', 
            'title': 'Create Staff', 
            'page_title': 'Create Staff', 
            'is_staff' : True,
        }
        
        return render(request, 'dashboard/staffs/staff_entry.html', context)


@login_required
@permissions_required(['can_manage_staff'])
def staffs(request):
    instances = Staff.objects.filter(is_deleted=False, is_active=True).order_by("-date_added")
    revoked_instances = Staff.objects.filter(is_deleted=False, is_active=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query) |
            Q(designation__name__icontains=query) |
            Q(phone__icontains=query) 
        )
        filter_data['q'] = query
    
    
    context = {
        'instances': instances, 
        'revoked_instances': revoked_instances, 
        'page_name' : 'Staffs', 
        'app_name' :'Staffs', 
        'page_title' : 'Staffs', 
        'filter_data' : filter_data,
        'is_staff' : True,
    }
    
    return render(request, 'dashboard/staffs/staffs.html', context)


@login_required
@permissions_required(['can_view_staff'])
def staff(request, pk):
    instance = Staff.objects.get(pk=pk, is_deleted=False)
    activities = UserActivity.objects.filter(is_deleted=False,user = instance.user)
    permissions = instance.permission.all()
    
    general_permissions = permissions.filter(app="general")
    dish_permissions = permissions.filter(app="dishes")
    brand_permissions = permissions.filter(app="brands")
    shop_permissions = permissions.filter(app="shops")
    staff_permissions = permissions.filter(app="staffs")
    user_permissions = permissions.filter(app="users")
    
    context = {
        'permissions' : permissions, 
        'instance': instance, 
        'activities': activities,
        'page_name' : 'Staff', 
        'app_name' :'Staffs', 
        'page_title' : 'Staff', 
        'is_need_light_box' : True, 
        "general_permissions": general_permissions, 
        "brand_permissions": brand_permissions, 
        "dish_permissions": dish_permissions, 
        "shop_permissions": shop_permissions, 
        "staff_permissions": staff_permissions, 
        "user_permissions": user_permissions, 
        'is_staff' : True,
    }
         
    return render(request, 'dashboard/staffs/staff.html', context)


@login_required
@permissions_required(['can_modify_staff'])
def staff_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Staff.objects.filter(pk=pk))
        email =instance.email
        form = StaffForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.name,
                title = "Updated an Staff",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Staff Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('staffs:staff', kwargs={"pk": data.pk})
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status" : "false", 
                "stable" : "true", 
                "title" : "Form validation error", 
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        instance = get_object_or_404(Staff.objects.filter(pk=pk))
        form = StaffForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Staffs', 
            "page_title" : "Edit staff", 
            "redirect" : True, 
            "url" : reverse('staffs:staff_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_staff' : True,
        }

        return render(request, 'dashboard/staffs/staff_entry.html', context)


@login_required
@permissions_required(['can_update_permissions'])
def update_permissions(request, pk):
    instance = get_object_or_404(Staff.objects.filter(pk=pk, is_deleted=False))

    if request.method == 'POST':
        permissions = request.POST.getlist('permission')
        instance.permission.clear()

        for item in permissions:
            p = Permission.objects.get(pk=item)
            instance.permission.add(p)

        response_data = {
            "status": "success", 
            "stable": "false", 
            "title": "Successfully Updated", 
            "message": "Permissions Updated successfully.", 
            "redirect": "true", 
            "redirect_url": reverse('staffs:staff', kwargs={'pk': instance.pk})
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        array_p = list(instance.permission.all().values_list('pk', flat=True))

        permissions = Permission.objects.all()
        general_permissions = permissions.filter(app="general")
        dish_permissions = permissions.filter(app="dishes")
        brand_permissions = permissions.filter(app="brands")
        shop_permissions = permissions.filter(app="shops")
        staff_permissions = permissions.filter(app="staffs")
        user_permissions = permissions.filter(app="users")
        
        context = {
            "is_edit": True, 
            "array_p": array_p, 
            "instance": instance, 
            'page_name': 'Staff Permission', 
            'app_name': 'Staffs', 
            'page_title': 'Staff Permission', 
            "url": reverse('staffs:update_permissions', kwargs={'pk': instance.pk}), 
            "general_permissions": general_permissions, 
            "brand_permissions": brand_permissions, 
            "dish_permissions": dish_permissions, 
            "shop_permissions": shop_permissions, 
            "staff_permissions": staff_permissions, 
            "user_permissions": user_permissions, 
        }
        
        return render(request, 'dashboard/staffs/set_permissions.html', context)


@login_required
@permissions_required(['can_delete_staff'])
@ajax_required
def staff_delete(request, pk):
    data = Staff.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.name,
        title = "Deleted an Staff",
    )
    activity.save()
    
    Staff.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Successfully Deleted", 
        "message" : "Staff Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('staffs:staffs')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@permissions_required(['can_update_password'])
def update_password(request , pk):
    instance = get_object_or_404(Staff.objects.filter(pk=pk, is_deleted=False))
    form = PasswordForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 =  form.cleaned_data['password2']
            
            if password1 == password2:
                
                user_name =request.user
                user =User.objects.get(username=user_name)
                Staff.objects.filter(email = user.email).update(password =password1)
                user.set_password(password1)
                user.save()
                
                response_data = {
                    "status": "success", 
                    "stable": "false", 
                    "title": "Successfully Updated", 
                    "message": "Password Updated successfully.", 
                }
                
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                response_data = {
                    "status": "error", 
                    "stable": "true", 
                    "title": "Password Mismatch", 
                    "message": "Enter Same Password.", 
                }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status" : "false", 
                "stable" : "true", 
                "title" : "Form validation error", 
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = PasswordForm()
        context = {
            'form' : form, 
            "instance": instance, 
            "url": reverse('main:profile'), 
        }
        
        return render(request, 'dashboard/profile.html', context)
    
    
@login_required
@permissions_required(['can_revoke_staff'])
def revoke_staff(request, pk):
    instance = get_object_or_404(Staff.objects.filter(pk=pk, is_deleted=False))

    User.objects.filter(pk=instance.user.pk).update(is_active=False)
    Staff.objects.filter(pk=pk).update(is_active=False)

    response_data = {
        "status" : "success", 
        "title" : "Successfully Revoked", 
        "message" : "Access  Successfully Revoked.", 
        "redirect" : "true", 
        "redirect_url" : reverse('staffs:staffs')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_grant_staff'])
def grant_staff(request, pk):
    instance = get_object_or_404(Staff.objects.filter(pk=pk, is_deleted=False))

    User.objects.filter(pk=instance.user.pk).update(is_active=True)
    Staff.objects.filter(pk=pk).update(is_active=True)

    response_data = {
        "status" : "success", 
        "title" : "Successfully Granted", 
        "message" : "Access  Successfully Granted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('staffs:staffs')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
# @permissions_required(['can_manage_staff_activities'])
def activities(request,pk):
    title = "Activities"
    staff = Staff.objects.get(pk=pk, is_deleted=False)
    instances = UserActivity.objects.filter(is_deleted=False, user=staff.user).order_by("-time")
    
    filter_data = {}
    query = request.GET.get("q")
    
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    on_date = request.GET.get('date')
    
    if query:
        instances = instances.filter(
            Q(app__icontains=query) |
            Q(title__icontains=query) |
            Q(instance__icontains=query) |
            Q(activity_type__icontains=query) 
        )
        filter_data['q'] = query
        
    if from_date and to_date:
        f_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        t_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        instances = instances.filter(time__date__range=[f_date, t_date])
        title = 'Activities (from %s to %s)' % (
            str(f_date), str(t_date))

        filter_data['from_date'] = from_date
        filter_data['to_date'] = to_date

    if on_date:
        o_date = datetime.datetime.strptime(on_date, '%Y-%m-%d').date()
        instances = instances.filter(time__date=on_date)
        title = 'Activities (On %s)' % (str(o_date))
        filter_data['on_date'] = on_date
    
    context = {
        'staff' : staff,
        'instances': instances, 
        'page_name' : 'Staff Activities', 
        'app_name' :'Staffs', 
        'page_title' : 'Staff Activities', 
        'filter_data' : filter_data,
        'pk' : pk,
        'title' : title,
        'from_date': from_date,
        'to_date': to_date,
        'on_date': on_date,
        'is_staff' : True,
    }
    
    return render(request, 'dashboard/staffs/staff_activities.html', context)


@login_required
# @permissions_required(['can_view_staff'])
def activity(request, pk):
    instance = UserActivity.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'activities': activities,
        'page_name' : 'Staff Activity', 
        'app_name' :'Staffs', 
        'page_title' : 'Staff Activity', 
        'is_need_light_box' : True, 
        'is_staff' : True,
    }
         
    return render(request, 'dashboard/staffs/staff_activity.html', context)
