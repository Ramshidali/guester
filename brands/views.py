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

from general.models import UserActivity
from main.decorators import permissions_required, role_required, ajax_required
from main.functions import generate_form_errors, get_auto_id
from brands.forms import *
from brands.models import *
from main.functions import decrypt_message, encrypt_message, get_auto_id, get_otp


class BrandAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Brand.objects.none()

        items = Brand.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )

        return items


@login_required
@permissions_required(['can_manage_brand'])
def brands(request):
    instances = Brand.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(name__icontains=query)
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Brands',
        'app_name' :'Brands',
        'page_title' : 'Brands',
        'filter_data' : filter_data,
        'is_brand' : True,
    }
    
    return render(request, 'dashboard/brands/brands.html', context)


@login_required
@permissions_required(['can_view_brand'])
def brand(request,pk):
    instance = Brand.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Brand',
        'app_name' :'Brands',
        'page_title' : 'Brand',
        'is_need_light_box' : True,
        'is_brand' : True,
    }
         
    return render(request, 'dashboard/brands/brand.html', context)


@login_required
@permissions_required(['can_create_brand'])
def brand_create(request):
    if request.method == "POST":
        form = BrandForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Brand)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="General",
                instance = data.name,
                title = "Created an Brand",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Created",
                "message" : "Brand Successfully Created.",
                "redirect" : "true",
                
                "redirect_url" : reverse('brands:brand', kwargs={"pk": data.pk})
            }
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = BrandForm()
        context = {
            "form" : form,
            'app_name' :'Brands',
            "page_title" : "Create brand",
            "redirect" : True,
            "url" : reverse('brands:brand_create'),
            'is_brand' : True,
        }

        return render(request,'dashboard/brands/brand_entry.html',context)
    

@login_required
@permissions_required(['can_modify_brand'])
def brand_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Brand.objects.filter(pk=pk))
        form = BrandForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            link =reverse('brands:brand', kwargs={"pk": data.pk})
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="General",
                instance = data.name,
                title = "Update an Brand",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Updated",
                "message" : "Brand Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('brands:brand', kwargs={"pk": data.pk})
            }
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        instance = get_object_or_404(Brand.objects.filter(pk=pk))
        form = BrandForm(instance=instance)
        
        context = {
            "form" : form,
            'app_name' :'Brands',
            "page_title" : "Edit brand",
            "redirect" : True,
            "url" : reverse('brands:brand_edit',kwargs={"pk":instance.pk}),
            "is_edit" :True,
            "instance" : instance,
            'is_brand' : True,
        }

        return render(request,'dashboard/brands/brand_entry.html',context)


@login_required
@ajax_required
@permissions_required(['can_delete_brand'])
def brand_delete(request, pk):
    instance = Brand.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="General",
        instance = instance.name,
        title = "Deleted an Brand",
    )
    activity.save()
    
    Brand.objects.filter(pk=pk).update(is_deleted=True)
    
    response_data = {
        "status" : "success",
        "title" : "Brand Deleted",
        "message" : "Brand Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('brands:brands')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

