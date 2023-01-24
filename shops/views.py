import json
import datetime
import xlrd
import xlwt

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import fromstr
from django.contrib.auth.models import User, Group

from main.decorators import role_required, ajax_required, permissions_required
from main.functions import generate_form_errors, get_auto_id
from general.functions import get_or_create_location
from shops.models import *
from shops.forms import  *
from dishes.models import *
from general.models import *
from dishes.forms import DishForm
from general.forms import LocationForm
from staffs.forms import UserForm
from users.models import Permission
from main.functions import decrypt_message, encrypt_message, get_auto_id, get_otp


class ShopTypeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ShopType.objects.none()

        items = ShopType.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )

        return items
    
class ShopAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Shop.objects.none()

        items = Shop.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )

        return items
    
class GalleryTypeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ShopGalleryType.objects.none()

        items = ShopGalleryType.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )

        return items
    
    
class FacilityAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Facility.objects.none()

        items = Facility.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(title__istartswith=self.q) 
                                )

        return items
    
    
class DeliveryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Delivery.objects.none()

        items = Delivery.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )

        return items
    
    
class DishAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Dish.objects.none()

        items = Dish.objects.filter(is_deleted=False, is_verified = True)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )
        return items
    
    
class ShopDishAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ShopDish.objects.none()
        
        items = ShopDish.objects.filter(is_deleted=False)
        
        shop = self.forwarded.get('shop', None)
        if shop:
            items= items.filter(shop=shop)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(dish__istartswith=self.q) 
                                )
        return items
 
 
class DayAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Days.objects.none()

        items = Days.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                    Q(name__istartswith=self.q) 
                                )

        return items   
    
    
class ZoneAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Zone.objects.none()

        items = Zone.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(name__istartswith=self.q) 
                                )

        return items
    
    
class SubZoneAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        items = SubZone.objects.filter(is_deleted=False, )

        zone = self.forwarded.get('zone', None)

        if zone:
            items = items.filter(zone=zone)
        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) |
                                 Q(name__istartswith=self.q)
                                )

        return items
    
    
class ShopTimingAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ShopTiming.objects.none()

        items = ShopTiming.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(timing__istartswith=self.q) 
                                )

        return items



@login_required
@permissions_required(['can_upload_shops'])
def upload_shops(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        
        if request.user.is_superuser:
            is_verified = True
        else:
            is_verified = False

        if form.is_valid():
            input_excel = request.FILES['file']
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)

            dict_list = []
            keys = [str(sheet.cell(0, col_index).value) for col_index in range(sheet.ncols)]
            for row_index in range(1, sheet.nrows):
                d = {keys[col_index]: str(sheet.cell(row_index, col_index).value)
                    for col_index in range(sheet.ncols)}
                dict_list.append(d)

            is_ok = True
            message = ''
            row_count = 2
            for item in dict_list:
                name = item['Name']
                phone = item['Phone']
                email = item['Email']
                website_link = item['Website']
                owner_name = item['Owner']
                manager_name =item['Manager']
                contact_number = item['Contact number']
                
                phone = (phone).split(".")[0]

                if not Shop.objects.filter(phone=phone, is_deleted=False).exists():
                    shop = Shop.objects.create(
                       name = name, 
                       phone =phone, 
                       email = email, 
                       website_link = website_link, 
                       owner_name = owner_name, 
                       manager_name = manager_name, 
                       contact_number = (contact_number).split(".")[0], 
                       is_verified =is_verified, 
                       auto_id =  get_auto_id(Shop), 
                       date_added = datetime.datetime.now(), 
                       creator= request.user, 
                       updater=request.user, 
                    )
                    shop.save()
                    
                response_data = {
                    "status" : "success", 
                    "stable" : "false", 
                    "title" : "Successfully Uploaded", 
                    "message" : "Shops Successfully Updated.", 
                    "redirect" : "true", 
                    "redirect_url" : reverse('shops:shops')
                }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            form = FileForm()
            title = "Upload Shops"
            context = {
                "form" : form, 
                "title" : title, 

                "is_need_popup_box" : True, 
                "is_need_dropzone" : True
            }
            
            return render(request, 'dashboard/shops/upload_shops.html', context)
    else:
        form = FileForm()

        context = {
            "form" : form, 
            'page_name' : 'Upload Shops', 
            'app_name' :'Shops', 
            'page_title' : 'Upload Shops', 
            "redirect" : True, 
            "url" : reverse('shops:upload_shops'), 

            "is_need_popup_box" : True, 
            "is_need_dropzone" : True,
            'is_shop' : True,
        }
        
        return render(request, 'dashboard/shops/upload_shops.html', context)
    
    
@login_required
@permissions_required(['can_manage_shop'])
def shops(request):
    unverified_instances = Shop.objects.filter(is_deleted=False, is_verified=False, is_rejected=False).order_by("-date_added")
    rejected_instances = Shop.objects.filter(is_deleted=False, is_verified=False, is_rejected=True)
    instances = Shop.objects.filter(is_deleted=False, is_verified=True).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query) | Q(phone__icontains=query) | Q(shop_type__name__icontains=query) | Q(location__location__icontains=query)           
        )
        rejected_instances = instances.filter(
            Q(name__icontains=query) | Q(phone__icontains=query) | Q(shop_type__name__icontains=query) | Q(location__location__icontains=query)           
        )
        unverified_instances = instances.filter(
            Q(name__icontains=query) | Q(phone__icontains=query) | Q(shop_type__name__icontains=query) | Q(location__location__icontains=query)           
        )
        filter_data['q'] = query
    
    context = {
        'unverified_instances': unverified_instances, 
        'rejected_instances': rejected_instances, 
        'instances': instances, 
        'page_name' : 'Shops', 
        'app_name' :'Shops', 
        'page_title' : 'Shops', 
        'filter_data' : filter_data,
        'is_shop' : True,
    }
    
    return render(request, 'dashboard/shops/shops.html', context)


@login_required
@permissions_required(['can_view_shop'])
def shop(request, pk):
    instance = Shop.objects.get(pk=pk, is_deleted=False)
    facilities = ShopFacility.objects.filter(is_deleted=False, shop=instance)
    delivery_partners = ShopDelivery.objects.filter(is_deleted=False, shop=instance)
    dishes = ShopDish.objects.filter(is_deleted=False, shop=instance)
    gallery = ShopGallery.objects.filter(is_deleted=False, shop=instance)
    working_days = ShopWorkingDay.objects.filter(is_deleted=False, shop=instance)
    dish_offers = DishOffer.objects.filter(is_deleted=False , shop=instance)
    precautions = ShopSafetyPrecaution.objects.filter(is_deleted=False , shop=instance)
    shop_offers = MoreOffer.objects.filter(is_deleted=False, shop=instance)
    shop_reviews = ShopRating.objects.filter(is_deleted=False, shop = instance)
    shop_timings = ShopTiming.objects.filter(is_deleted=False, shop=instance) 
    
    try:
        shop_admin = ShopAdmin.objects.get(is_deleted=False, shop=instance)
    except :
        shop_admin= None
    
    context = {
        'instance': instance, 
        'facilities' : facilities, 
        'delivery_partners' : delivery_partners, 
        'gallery' : gallery, 
        'dishes' : dishes, 
        'dish_offers' : dish_offers, 
        'shop_offers' : shop_offers, 
        'working_days' : working_days, 
        'precautions' : precautions, 
        'shop_reviews' : shop_reviews, 
        'shop_timings' : shop_timings, 
        'shop_admin' : shop_admin, 
        'page_name' : 'Shop', 
        'app_name' :'Shops', 
        'page_title' : 'Shop', 
        'is_need_light_box' : True, 
        'is_shop' : True,
    }
    
    return render(request, 'dashboard/shops/shop.html', context)


@login_required
@permissions_required(['can_create_shop'])
def shop_create(request):
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST, request.FILES)

        if form.is_valid()  and location_form.is_valid():
            location_name = location_form.cleaned_data['location']
            latitude = location_form.cleaned_data['latitude']
            longitude = location_form.cleaned_data['longitude']
            
            location = get_or_create_location(request, location_form, location_name, latitude, longitude)
            
            data = form.save(commit=False)
            
            try:
                located = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                data.located = located
            except:
                pass
            
            shop_timing = request.POST.getlist('shop_timing')
            
            data.creator = request.user
            data.updater = request.user
            data.location = location
            data.auto_id = get_auto_id(Shop)
            data.is_updated = True
            data.save()
            
            for item in shop_timing:
                p = ShopTiming.objects.get(pk=item).pk
                data.shop_timing.add(p)
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.name,
                title = "Created an Shop",
            )
            activity.save()
            
            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Shop Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop', kwargs={"pk": data.pk})
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
        form = ShopForm()
        location_form = LocationForm()
        context = {
            "form" : form, 
            "location_form" : location_form, 
            'app_name' :'Shop', 
            "page_title" : "Create Shop", 
            "redirect" : True, 
            "url" : reverse('shops:shop_create'), 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_entry.html', context)
    

@login_required
@permissions_required(['can_modify_shop'])
def shop_update(request, pk):
    instance = get_object_or_404(Shop.objects.filter(pk=pk))
    location = instance.location
    if request.method == "POST":
        
        form = ShopForm(request.POST, request.FILES, instance=instance)
        location_form = LocationForm(request.POST, request.FILES, instance=location)
        if form.is_valid() and location_form.is_valid() :
            location_name = location_form.cleaned_data['location']
            latitude = location_form.cleaned_data['latitude']
            longitude = location_form.cleaned_data['longitude']

            location = get_or_create_location(request, location_form, location_name, latitude, longitude)
            
            data = form.save(commit=False)
            
            try:
                located = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                data.located = located
            except:
                pass
            
            shop_timing = request.POST.getlist('shop_timing')
            instance.shop_timing.clear()
            for item in shop_timing:
                p = ShopTiming.objects.get(pk=item)
                data.shop_timing.add(p)
            
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.location=location
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.name,
                title = "Updated an Shop",
            )
            activity.save()
            
            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Shop Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(Shop.objects.filter(pk=pk))
        form = ShopForm(instance=instance)
        location_form = LocationForm(instance=location)
        context = {
            "form" : form, 
            "location_form" : location_form, 
            'app_name' :'Shops', 
            "page_title" : "Update shop", 
            "redirect" : True, 
            "url" : reverse('shops:shop_update', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "is_update" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_entry.html', context)


@login_required
@permissions_required(['can_modify_shop'])
def shop_edit(request, pk):
    instance = get_object_or_404(Shop.objects.filter(pk=pk))
    location =instance.location
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES, instance=instance)
        location_form = LocationForm(request.POST, request.FILES, instance=location)
        if form.is_valid() and location_form.is_valid() :
            
            location_name = location_form.cleaned_data['location']
            latitude = location_form.cleaned_data['latitude']
            longitude = location_form.cleaned_data['longitude']

            location = get_or_create_location(request, location_form, location_name, latitude, longitude)

            data = form.save(commit=False)
            
            try:
                located = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                data.located = located
            except:
                pass
            
            shop_timing = request.POST.getlist('shop_timing')
            instance.shop_timing.clear()
            for item in shop_timing:
                p = ShopTiming.objects.get(pk=item)
                data.shop_timing.add(p)
            
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.location =location
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Edit",
                app="Shop",
                instance = data.name,
                title = "Edited an Shop",
            )
            activity.save()
            
            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Modified", 
                "message" : "Shop Successfully Modified.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(Shop.objects.filter(pk=pk))
        form = ShopForm(instance=instance)
        location_form = LocationForm(instance=location)
        context = {
            "form" : form, 
            "location_form" : location_form, 
            'app_name' :'shop', 
            "page_title" : "Edit shop", 
            "redirect" : True, 
            "url" : reverse('shops:shop_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_entry.html', context)


@ajax_required
@permissions_required(['can_delete_shop'])
def shop_delete(request, pk):
    instance = Shop.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = instance.name,
        title = "Deleted an Shop",
    )
    activity.save()
    
    Shop.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Shop Deleted", 
        "message" : "Shop Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:shops')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@ajax_required
@permissions_required(['can_verify_shop'])
def shop_verify(request, pk):
    data= Shop.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Verify",
        app="Shop",
        instance = data.name,
        title = "Verified an Shop",
    )
    activity.save()
    
    Shop.objects.filter(pk=pk).update(is_verified=True, is_rejected=False)

    response_data = {
        "status" : "success", 
        "title" : "Shop Verified", 
        "message" : "Shop Successfully Verified.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:shops')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def update_facilities(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Shop.objects.filter(pk=pk))
        form = ShopForm(request.POST, request.FILES, instance=instance)
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
                title = "Updated an Facility",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Modified", 
                "message" : "Shop Successfully Modified.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(Shop.objects.filter(pk=pk))
        form = ShopForm()
        context = {
            "form" : form, 
            'app_name' :'shop', 
            "page_title" : "Edit shop", 
            "redirect" : True, 
            "url" : reverse('shops:shop_update', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

    return render(request, 'dashboard/shops/update_facilities.html', context)


@login_required
@permissions_required(['can_reject_shop'])
def shop_reject(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Shop.objects.filter(pk=pk))
        form = ShopRejectionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.is_rejected = True
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Reject",
                app="Shop",
                instance = data.name,
                title = "Rejected an Shop",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Rejected", 
                "message" : "Shop Successfully Rejected.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shops')
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
        instance = get_object_or_404(Shop.objects.filter(pk=pk))
        form = ShopRejectionForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Rejected shop", 
            "redirect" : True, 
            "url" : reverse('shops:shop_reject', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "is_update" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_reject.html', context)


@login_required
@permissions_required(['can_manage_shop_type'])
def shop_types(request):
    instances=ShopType.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Shop Type', 
        'app_name' :'Shops', 
        'page_title' : 'Shop Type', 
        'filter_data' : filter_data,
        'is_shop_type' : True,
    }
    
    return render(request, 'dashboard/shops/shop_types.html', context)


@login_required
@permissions_required(['can_view_shop_type'])
def shop_type(request, pk):
    instance = ShopType.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Shop Type', 
        'app_name' :'Shops', 
        'page_title' : 'Shop Type', 
        'is_need_light_box' : True, 
        'is_shop_type' : True,
    }
         
    return render(request, 'dashboard/shops/shop_type.html', context)


@login_required
@permissions_required(['can_create_shop_type'])
def shop_type_create(request):
    if request.method == "POST":
        form = ShopTypeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ShopType)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.name,
                title = "Created an Shop Type",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Shop type Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop_type', kwargs={"pk": data.pk})
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
        form = ShopTypeForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Shop type", 
            "redirect" : True, 
            "url" : reverse('shops:shop_type_create'), 
            'is_shop_type' : True,
        }

        return render(request, 'dashboard/shops/shop_type_entry.html', context)
    

@login_required
@permissions_required(['can_modify_shop_type'])
def shop_type_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopType.objects.filter(pk=pk))
        form = ShopTypeForm(request.POST, request.FILES, instance=instance)
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
                title = "Updated an Shop Type",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Shop type Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop_type', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(ShopType.objects.filter(pk=pk))
        form = ShopTypeForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Shop type", 
            "redirect" : True, 
            "url" : reverse('shops:shop_type_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop_type' : True,
        }

        return render(request, 'dashboard/shops/shop_type_entry.html', context)


@login_required
@permissions_required(['can_delete_shop_type'])
@ajax_required
def shop_type_delete(request, pk):
    data = ShopType.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.name,
        title = "Deleted an Shop Type",
    )
    activity.save()
    
    ShopType.objects.filter(pk=pk).update(is_deleted=True)
    
    response_data = {
        "status" : "success", 
        "title" : "Shop Type Deleted", 
        "message" : "Shop Type Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:shop_types')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_gallery_type'])
def gallery_types(request):
    instances = ShopGalleryType.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(name__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Gallery Type', 
        'app_name' :'Shops', 
        'page_title' : 'Gallery Type', 
        'filter_data' : filter_data,
        'is_gt' : True,
    }
    
    return render(request, 'dashboard/shops/gallery_types.html', context)


@login_required
@permissions_required(['can_view_gallery_type'])
def gallery_type(request, pk):
    instance = ShopGalleryType.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Gallery Type', 
        'app_name' :'Shops', 
        'page_title' : 'Gallery Type', 
        'is_need_light_box' : True, 
        'is_gt' : True,
    }
         
    return render(request, 'dashboard/shops/gallery_type.html', context)


@login_required
@permissions_required(['can_create_gallery_type'])
def gallery_type_create(request):
    if request.method == "POST":
        form = GalleryTypeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ShopGalleryType)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.name,
                title = "Created an Gallery Type",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Gallery type Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:gallery_types')
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
        form = GalleryTypeForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Gallery type", 
            "redirect" : True, 
            "url" : reverse('shops:gallery_type_create'), 
            'is_gt' : True,
        }

        return render(request, 'dashboard/shops/gallery_type_entry.html', context)
    

@login_required
@permissions_required(['can_modify_gallery_type'])
def gallery_type_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopGalleryType.objects.filter(pk=pk))
        form = GalleryTypeForm(request.POST, request.FILES, instance=instance)
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
                title = "Updated an Shop Type",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Gallery type Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:gallery_types')
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
        instance = get_object_or_404(ShopGalleryType.objects.filter(pk=pk))
        form = GalleryTypeForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Gallery type", 
            "redirect" : True, 
            "url" : reverse('shops:gallery_type_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_gt' : True,
        }

        return render(request, 'dashboard/shops/gallery_type_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_gallery_type'])
def gallery_type_delete(request, pk):
    data = ShopGalleryType.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.name,
        title = "Deleted an Gallery Type",
    )
    activity.save()
    ShopGalleryType.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Gallery Type Deleted", 
        "message" : "Gallery Type Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:gallery_types')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_create_shop_gallery'])
def gallery_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk))
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        print(form)

        if form.is_valid():
            data = form.save(commit=False)
            data.shop =shop
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ShopGallery)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.file_type,
                title = "Created an Gallery",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Gallery  Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop', kwargs={"pk":pk}), 
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
        form = GalleryForm()
    
    context = {
        "form" : form, 
        'app_name' :'Shops', 
        "page_title" : "Create Gallery", 
        "redirect" : True, 
        "url" : reverse('shops:gallery_create', kwargs={"pk":pk}), 
        'is_shop' : True,
    }
    
    return render(request, 'dashboard/shops/gallery_entry.html', context)


@login_required
@permissions_required(['can_create_shop_gallery'])
def gallery_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopGallery.objects.filter(pk=pk))
        form = GalleryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.file_type,
                title = "Updated  Shop Gallery",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Gallery Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(ShopGallery.objects.filter(pk=pk))
        form = GalleryForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Gallery ", 
            "redirect" : True, 
            "url" : reverse('shops:gallery_edit', kwargs={"pk":instance.pk}), 
            "is_gallery_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/gallery_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_shop_gallery'])
def gallery_delete(request, pk):
    data = ShopGallery.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.file_type,
        title = "Deleted an Gallery",
    )
    
    activity.save()
    ShopGallery.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Gallery Image Deleted", 
        "message" : "Gallery Image Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_shop_delivery_partner'])
def delivery_partners(request):
    instances = ShopDelivery.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances, 
        'page_name' : 'Delivery Partner', 
        'app_name' :'Shops', 
        'page_title' : 'Delivery Partner', 
        'is_shop' : True,
    }
    
    return render(request, 'dashboard/shops/delivery_partners.html', context)


@login_required
@permissions_required(['can_view_shop_delivery_partner'])
def delivery_partner(request, pk):
    instance =ShopDelivery.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Delivery Partner', 
        'app_name' :'Shops', 
        'page_title' : 'Delivery Partner', 
        'is_need_light_box' : True, 
        'is_shop' : True,
    }
         
    return render(request, 'dashboard/shops/delivery_partner.html', context)


@login_required
@permissions_required(['can_create_shop_delivery_partner'])
def delivery_partner_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    
    if request.method == "POST":
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            print("----------")
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(ShopDelivery)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.shop,
                title = "Created an Delivery Partner",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Delivery Partner Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop', kwargs={"pk":shop.pk})
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
        form = PartnerForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Delivery Partner", 
            "redirect" : True, 
            "url" : reverse('shops:delivery_partner_create', kwargs={"pk":pk}), 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/delivery_partner_entry.html', context)
    

@login_required
@permissions_required(['can_modify_shop_delivery_partner'])
def delivery_partner_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopDelivery.objects.filter(pk=pk))
        form = PartnerForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.shop,
                title = "Updated an Delivery Partner",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Delivery Partner Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(ShopDelivery.objects.filter(pk=pk))
        form = PartnerForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Delivery Partner", 
            "redirect" : True, 
            "url" : reverse('shops:delivery_partner_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/delivery_partner_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_shop_delivery_partner'])
def delivery_partner_delete(request, pk):
    ShopDelivery.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Delivery Partner Deleted", 
        "message" : "Delivery Partner Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:shops')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    
@login_required
@permissions_required(['can_view_shop_dish'])
def shop_dish(request, pk):
    instance =ShopDish.objects.get(pk=pk, is_deleted=False)
    images =ShopDishImage.objects.filter(is_deleted =False , shop_dish=instance)
    
    context = {
        'instance': instance, 
        'images' : images, 
        'page_name' : 'Menu', 
        'app_name' :'Shops', 
        'page_title' : 'Menu', 
        'is_need_light_box' : True, 
        'is_shop' : True,
    }
    
    return render(request, 'dashboard/shops/shop_dish.html', context)


@login_required
@permissions_required(['can_create_shop_dish'])
def shop_dish_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    
    if request.method == "POST":
        form = ShopDishForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(ShopDish)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.dish,
                title = "Created an Dish in Shop",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Menu Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop', kwargs={"pk":shop.pk})
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
        form = ShopDishForm()
        dish_form = DishForm()
        context = {
            "form" : form, 
            "dish_form" : dish_form, 
            'app_name' :'Shops', 
            "page_title" : "Create Menu", 
            "redirect" : True, 
            "url" : reverse('shops:shop_dish_create', kwargs={"pk":pk}), 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_dish_entry.html', context)
    

@login_required
@permissions_required(['can_modify_shop_dish'])
def shop_dish_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopDish.objects.filter(pk=pk))
        form = ShopDishForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.dish,
                title = "Updated an Dish in Shop",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Menu Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(ShopDish.objects.filter(pk=pk))
        form = ShopDishForm(instance=instance)
        dish_form = DishForm()
        
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "dish_form" : dish_form, 
            "page_title" : "Edit Menu", 
            "redirect" : True, 
            "url" : reverse('shops:shop_dish_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_dish_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_shop_dish'])
def shop_dish_delete(request, pk):
    data = ShopDish.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.dish,
        title = "Deleted an Dish in Shop",
    )
    activity.save()
    
    ShopDish.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Menu Deleted", 
        "message" : "Menu Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    
@login_required
@permissions_required(['can_create_shop_dish_image'])
def dish_image_create(request, pk):
    shop_dish = get_object_or_404(ShopDish.objects.filter(pk=pk, is_deleted=False))
    
    if request.method == "POST":
        form = DishImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop_dish = shop_dish
            data.auto_id = get_auto_id(ShopDishImage)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.shop_dish,
                title = "Created an ShopDish Image",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Added", 
                "message" : "Dish Image Successfully Added.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop_dish', kwargs={"pk":shop_dish.pk})
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
        form = DishImageForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Add Dish Image", 
            "redirect" : True, 
            "url" : reverse('shops:dish_image_create', kwargs={"pk":pk}), 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/dish_image_entry.html', context)
    

@login_required
@ajax_required
@permissions_required(['can_delete_shop_dish_image'])
def dish_image_delete(request, pk):
    data = ShopDishImage.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.shop_dish,
        title = "Deleted an ShopDish Image",
    )
    activity.save()
    
    ShopDishImage.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Image Deleted", 
        "message" : "Image Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_create_dish_offer'])
def dish_offer_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    
    if request.method == "POST":
        form = DishOfferForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(DishOffer)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.offer,
                title = "Created an Dish Offer",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Offer Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop', kwargs={"pk":shop.pk})
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
        form = DishOfferForm(initial={'shop':shop})
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Offer", 
            "redirect" : True, 
            "url" : reverse('shops:dish_offer_create', kwargs={"pk":pk}), 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/dish_offer_entry.html', context)
    

@login_required
@permissions_required(['can_modify_dish_offer'])
def dish_offer_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(DishOffer.objects.filter(pk=pk))
        form = DishOfferForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.offer,
                title = "Updated an Dish Offer",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Offer Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(DishOffer.objects.filter(pk=pk))
        form = DishOfferForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Offer", 
            "redirect" : True, 
            "url" : reverse('shops:dish_offer_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/dish_offer_entry.html', context)


@login_required
@permissions_required(['can_delete_dish_offer'])
@ajax_required
def dish_offer_delete(request, pk):
    data = DishOffer.objects.get(pk=pk)
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.offer,
        title = "Deleted an Dish Offer",
    )
    activity.save()
    DishOffer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Offer Deleted", 
        "message" : "Offer Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

  
@login_required
@permissions_required(['can_create_shop_safety'])
def precaution_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    PrecautionFormset = formset_factory(PrecautionForm, extra=2)

    if request.method == "POST":
        precaution_formset = PrecautionFormset(request.POST, request.FILES, prefix="precaution_formset")
        if precaution_formset.is_valid():
            creator = request.user
            updater = request.user

            for item in precaution_formset:
                auto_id = get_auto_id(ShopSafetyPrecaution)
                
                title = item.cleaned_data['title']
                ShopSafetyPrecaution.objects.create(
                    shop=shop, 
                    title=title, 
                    creator=creator, 
                    updater=updater, 
                    auto_id=auto_id, 
                )
                
                activity = UserActivity(
                    user=request.user,
                    activity_type="Create",
                    app="Shop",
                    instance = title,
                    title = "Created an Precaution",
                    )
                activity.save()

            return JsonResponse({
                "status": "success", 
                'stable': "false", 
                'title': 'Successfully Created', 
                'message': 'Precaution Successfully Created', 
                "redirect": 'true', 
                "redirect_url": reverse('shops:shop', kwargs={"pk": shop.pk})
            })
        else:

            message = generate_form_errors(precaution_formset, formset=True)

            response_data = {
                "status" : "false", 
                "stable" : "true", 
                "title" : "Form validation error", 
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        precaution_formset = PrecautionFormset(prefix="precaution_formset")
        context = {
            "precaution_formset": precaution_formset, 
            "title": "Create Precaution", 
            "redirect": True, 
            'app_name' :'Shops', 
            "page_title" : "Create Precaution", 
            "url": reverse("shops:precaution_create", kwargs={"pk": pk}), 
            "pk": pk, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/precaution_entry.html', context)
    

@login_required
@permissions_required(['can_modify_shop_safety'])
def precaution_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopSafetyPrecaution.objects.filter(pk=pk))
        form = PrecautionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.title,
                title = "Updated an Precaution",
                )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Precaution Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(ShopSafetyPrecaution.objects.filter(pk=pk))
        form = PrecautionForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Precaution", 
            "redirect" : True, 
            "url" : reverse('shops:precaution_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/precaution_edit.html', context)


@login_required
@permissions_required(['can_delete_shop_safety'])
@ajax_required
def precaution_delete(request, pk):
    data = ShopSafetyPrecaution.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Update",
        app="Shop",
        instance = data.title,
        title = "Updated an Precaution",
        )
    activity.save()
    
    ShopSafetyPrecaution.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Precaution Deleted", 
        "message" : "Precaution Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

      
@login_required
@permissions_required(['can_create_shop_working_day'])
def add_working_days(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    DayFormset = formset_factory(WorkingDayForm, extra=7)

    if request.method == "POST":
        day_formset = DayFormset(request.POST, request.FILES, prefix="day_formset")
        if day_formset.is_valid():
            creator = request.user
            updater = request.user

            for item in day_formset:
                auto_id = get_auto_id(ShopWorkingDay)
                
                start_time = item.cleaned_data['start_time']
                end_time = item.cleaned_data['end_time']
                day = item.cleaned_data['day']
                ShopWorkingDay.objects.create(
                    shop=shop, 
                    start_time=start_time, 
                    end_time=end_time, 
                    day=day, 
                    creator=creator, 
                    updater=updater, 
                    auto_id=auto_id, 
                )
                
                activity = UserActivity(
                    user=request.user,
                    activity_type="Create",
                    app="Shop",
                    instance = day,
                    title = "Created  Shop Working Time",
                )
                activity.save()
                

            return JsonResponse({
                "status": "success", 
                'stable': "false", 
                'title': 'Successfully Added', 
                'message': 'Working Days Successfully Added', 
                "redirect": 'true', 
                "redirect_url": reverse('shops:shop', kwargs={"pk": shop.pk})
            })
        else:

            message = generate_form_errors(day_formset, formset=True)

            response_data = {
                "status" : "false", 
                "stable" : "true", 
                "title" : "Form validation error", 
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        day_formset = DayFormset(prefix="day_formset")
        context = {
            "day_formset": day_formset, 
            "title": "Add Working Days", 
            "redirect": True, 
            'app_name' :'Shops', 
            "page_title" : "Add Working Days & Time", 
            "url": reverse("shops:add_working_days", kwargs={"pk": pk}), 
            "pk": pk, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/working_day_entry.html', context)
    
    
@login_required
@permissions_required(['can_modify_shop_working_day'])
def edit_working_day(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopWorkingDay.objects.filter(pk=pk))
        form = WorkingDayForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.start_time= start_time
            data.end_time = end_time
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.day,
                title = "Updated  Shop Working Time",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Working day Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(ShopWorkingDay.objects.filter(pk=pk))
        form = WorkingDayForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Working Day & Time", 
            "redirect" : True, 
            "url" : reverse('shops:edit_working_day', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/working_day_edit.html', context)
    
    
@ajax_required
@permissions_required(['can_delete_shop_working_day'])
def delete_working_day(request, pk):
    ShopWorkingDay.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Successfully Deleted", 
        "message" : "Working Day & Time Successfully Deleted.", 
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_create_more_offer'])
def more_offer_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    if request.method == "POST":
        form = MoreOfferForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(MoreOffer)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.title,
                title = "Created an Offer",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Shop Offer Successfully Created.", 
                "redirect" : "true", 
                "redirect_url": reverse('shops:shop', kwargs={"pk": shop.pk})
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
        form = MoreOfferForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Shop Offer", 
            "redirect" : True, 
            "url" : reverse('shops:more_offer_create', kwargs={"pk": pk}), 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/more_offer_entry.html', context)
    

@login_required
@permissions_required(['can_modify_more_offer'])
def more_offer_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(MoreOffer.objects.filter(pk=pk))
        form = MoreOfferForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.title,
                title = "Updated an Dish Offer",
            )
            activity.save()
            
            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Shop Offer Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(MoreOffer.objects.filter(pk=pk))
        form = MoreOfferForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Shop Offer", 
            "redirect" : True, 
            "url" : reverse('shops:more_offer_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/more_offer_entry.html', context)


@login_required
@permissions_required(['can_delete_more_offer'])
@ajax_required
def more_offer_delete(request, pk):
    data = MoreOffer.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.title,
        title = "Deleted an Offer",
    )
    activity.save()
    
    MoreOffer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Shop Offer Deleted", 
        "message" : "Shop Offer Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_create_dish'])
def dish_create(request):
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Dish)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.name,
                title = "Created an Dish",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Dish  Successfully Created.", 
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
        form = DishForm()
        context = {
            "form" : form, 
            'app_name' :'Dishes', 
            "page_title" : "Create Dish", 
            "redirect" : True, 
            "url" : reverse('dishes:dish_create'), 

        }

        return render(request, 'dashboard/dishes/dish_entry.html', context)
    

@login_required
@permissions_required(['can_manage_shop_offer'])
def shop_offers(request):
    instances=ShopOffer.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(shop__name__icontains=query) |
            Q(title__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Shop Offer', 
        'app_name' :'Shops', 
        'page_title' : 'Shop Offer', 
        'filter_data' : filter_data,
        'is_shop_offer' : True,
    }
    
    return render(request, 'dashboard/shops/shop_offers.html', context)


@login_required
@permissions_required(['can_view_shop_offer'])
def shop_offer(request, pk):
    instance = ShopOffer.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Shop Offer', 
        'app_name' :'Shops', 
        'page_title' : 'Shop Offer', 
        'is_need_light_box' : True, 
        'is_shop_offer' : True,
    }
         
    return render(request, 'dashboard/shops/shop_offer.html', context)


@login_required
@permissions_required(['can_create_shop_offer'])
def shop_offer_create(request):
    if request.method == "POST":
        form = ShopOfferForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ShopOffer)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.title,
                title = "Created an Shop Offer",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Shop Offer Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop_offer', kwargs={"pk": data.pk})
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
        form = ShopOfferForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Shop Offer", 
            "redirect" : True, 
            "url" : reverse('shops:shop_offer_create'), 
            'is_shop_offer' : True,
        }

        return render(request, 'dashboard/shops/shop_offer_entry.html', context)
    

@login_required
@permissions_required(['can_edit_shop_offer'])
def shop_offer_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopOffer.objects.filter(pk=pk))
        form = ShopOfferForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.title,
                title = "Updated an Shop Offer",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Shop Offer Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop_offer', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(ShopOffer.objects.filter(pk=pk))
        form = ShopOfferForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Shop Offer", 
            "redirect" : True, 
            "url" : reverse('shops:shop_offer_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop_offer' : True,
        }

        return render(request, 'dashboard/shops/shop_offer_entry.html', context)


@login_required
@permissions_required(['can_delete_shop_offer'])
@ajax_required
def shop_offer_delete(request, pk):
    data = ShopOffer.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.title,
        title = "Deleted an Shop Offer",
    )
    activity.save()
            
            
    ShopOffer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Shop Offer Deleted", 
        "message" : "Shop Offer Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:shop_offers')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_brand_offer'])
def brand_offers(request):
    instances=BrandOffer.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(brand__name__icontains=query) |
            Q(title__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Brand Offer', 
        'app_name' :'Shops', 
        'page_title' : 'Brand Offer', 
        'filter_data' : filter_data,
        'is_brand_offer' : True,
    }
    
    return render(request, 'dashboard/shops/brand_offers.html', context)


@login_required
@permissions_required(['can_view_brand_offer'])
def brand_offer(request, pk):
    instance = BrandOffer.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Brand Offer', 
        'app_name' :'Shops', 
        'page_title' : 'Brand Offer', 
        'is_need_light_box' : True, 
        'is_brand_offer' : True,
    }
    
    return render(request, 'dashboard/shops/brand_offer.html', context)


@login_required
@permissions_required(['can_create_brand_offer'])
def brand_offer_create(request):
    if request.method == "POST":
        form = BrandOfferForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(BrandOffer)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.title,
                title = "Created an Brand Offer",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Brand Offer Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:brand_offer', kwargs={"pk": data.pk})
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
        form = BrandOfferForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Brand Offer", 
            "redirect" : True, 
            "url" : reverse('shops:brand_offer_create'), 
            'is_brand_offer' : True,
        }

        return render(request, 'dashboard/shops/brand_offer_entry.html', context)
    

@login_required
@permissions_required(['can_modify_brand_offer'])
def brand_offer_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(BrandOffer.objects.filter(pk=pk))
        form = BrandOfferForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.title,
                title = "Updated an Brand Offer",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Brand Offer Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:brand_offer', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(BrandOffer.objects.filter(pk=pk))
        form = BrandOfferForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Brand Offer", 
            "redirect" : True, 
            "url" : reverse('shops:brand_offer_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_brand_offer' : True,
        }

        return render(request, 'dashboard/shops/brand_offer_entry.html', context)


@login_required
@permissions_required(['can_delete_brand_offer'])
@ajax_required
def brand_offer_delete(request, pk):
    data = BrandOffer.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.title,
        title = "Deleted an Brand Offer",
    )
    activity.save()
    
    BrandOffer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Brand Offer Deleted", 
        "message" : "Brand Offer Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:brand_offers')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_shop_review'])
def shop_reviews(request):
    instances=ShopRating.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(shop__name__icontains=query) |
            Q(customer__name__icontains=query)
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Shop Review', 
        'app_name' :'Reviews', 
        'page_title' : 'Shop Review', 
        'filter_data' : filter_data,
        'is_review' : True,
    }
    
    return render(request, 'dashboard/shops/shop_reviews.html', context)


@login_required
@permissions_required(['can_view_shop_review'])
def shop_review(request, pk):
    instance = ShopRating.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Shop Review', 
        'app_name' :'Reviews', 
        'page_title' : 'Shop Review', 
        'is_need_light_box' : True, 
        'is_review' : True,
    }
         
    return render(request, 'dashboard/shops/shop_review.html', context)

@login_required
@permissions_required(['can_delete_shop_review'])
@ajax_required
def shop_review_delete(request, pk):
    data = ShopRating.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.customer,
        title = "Deleted an Shop Offer",
    )
    activity.save()
    
    ShopRating.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Shop Review Deleted", 
        "message" : "Shop Review Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:shop_reviews')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_create_shop_admin'])
def shop_admin_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid() :
            data = form.save(commit=False)
            password =form.cleaned_data["password1"]
            
            instance = data
            data.save()
            
            group, created=Group.objects.get_or_create(name="shop_admin")
            data.groups.add(group) 
            data.save()
            
            ShopAdmin.objects.create(
                shop=shop, 
                password=password, 
                user = instance, 
                auto_id = get_auto_id(ShopAdmin), 
                creator = request.user, 
                updater = request.user
            )
            data.save()
            
            response_data = {
                "status": "success", 
                "stable" : "false", 
                "title": "Successfully Created", 
                "message": "Shop Admin created successfully.", 
                "redirect": "true", 
                "redirect_url": reverse('shops:shop', kwargs={'pk': pk})
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false", 
                "stable": "true", 
                "title": "Form validation error", 
                "message": str(message)
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form =  UserForm()

        context = {
            "form": form, 
            'page_name': 'Create Shop Admin', 
            'app_name' :'Staffs', 
            'title': 'Create Shop Admin', 
            'page_title': 'Create Shop Admin', 
        }
        
        return render(request, 'dashboard/shops/shop_admin_entry.html', context)
    

@login_required
@permissions_required(['can_set_permissions'])
def set_permissions(request, pk):
    instance = get_object_or_404(ShopAdmin.objects.filter(pk=pk, is_deleted=False))
    user = instance.user

    if request.method == 'POST':
        permissions = request.POST.getlist('permission')
        instance.permission.clear()
        user.user_permissions.set(permissions)

        for item in permissions:
            p = Permission.objects.get(pk=item)
            instance.permission.add(p)

        response_data = {
            "status": "success", 
            "stable": "false", 
            "title": "Successfully Updated", 
            "message": "Permissions Updated successfully.", 
            "redirect": "true", 
            "redirect_url": reverse('shops:shop', kwargs={'pk': instance.shop.pk})
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
            'page_name': 'Shop Admin Permission', 
            'app_name': 'Shops', 
            'page_title': 'Shop Admin Permission', 
            "url": reverse('shops:set_permissions', kwargs={'pk': instance.pk}), 
            "general_permissions": general_permissions, 
            "brand_permissions": brand_permissions, 
            "dish_permissions": dish_permissions, 
            "shop_permissions": shop_permissions, 
            "staff_permissions": staff_permissions, 
            "user_permissions": user_permissions, 
        }
        
        return render(request, 'dashboard/staffs/set_permissions.html', context)
    
    
@login_required
@permissions_required(['can_manage_zone'])
def zones(request):
    instances = Zone.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(zone__icontains=query)
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Zones', 
        'app_name' :'shops', 
        'page_title' : 'Zones', 
        'filter_data' : filter_data,
        'is_zone' : True,
    }
    
    return render(request, 'dashboard/shops/zones.html', context)


@login_required
@permissions_required(['can_create_zone'])
def zone_create(request):
    if request.method == "POST":
        form = ZoneForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Zone)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.zone,
                title = "Created an Zone",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Zone Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:zones')
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
        form = ZoneForm()
        context = {
            "form" : form, 
            'app_name' :'Zones', 
            "page_title" : "Create zone", 
            "redirect" : True, 
            "url" : reverse('shops:zone_create'), 
            'is_zone' : True,
        }

        return render(request, 'dashboard/shops/zone_entry.html', context)
    

@login_required
@permissions_required(['can_modify_zone'])
def zone_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Zone.objects.filter(pk=pk))
        form = ZoneForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.zone,
                title = "Updated an Zone",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Zone Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:zones', )
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
        instance = get_object_or_404(Zone.objects.filter(pk=pk))
        form = ZoneForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Zones', 
            "page_title" : "Edit zone", 
            "redirect" : True, 
            "url" : reverse('shops:zone_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_zone' : True,
        }

        return render(request, 'dashboard/shops/zone_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_zone'])
def zone_delete(request, pk):
    data = Zone.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.zone,
        title = "Deleted an Zone",
    )
    activity.save()

    Zone.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Zone Deleted", 
        "message" : "Zone Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:zones')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_sub_zone'])
def sub_zones(request):
    instances = SubZone.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(zone__icontains=query)
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'sub_zones', 
        'app_name' :'shops', 
        'page_title' : 'sub_zones', 
        'filter_data' : filter_data,
        'is_sub_zone' : True,
    }
    
    return render(request, 'dashboard/shops/sub_zones.html', context)


@login_required
@permissions_required(['can_create_sub_zone'])
def sub_zone_create(request):
    if request.method == "POST":
        form = SubZoneForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(SubZone)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.name,
                title = "Created an Sub zone",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "SubZone Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:sub_zones')
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
        form = SubZoneForm()
        context = {
            "form" : form, 
            'app_name' :'shops', 
            "page_title" : "Create zone", 
            "redirect" : True, 
            "url" : reverse('shops:sub_zone_create'), 
            'is_sub_zone' : True,
        }

        return render(request, 'dashboard/shops/sub_zone_entry.html', context)
    

@login_required
@permissions_required(['can_modify_sub_zone'])
def sub_zone_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(SubZone.objects.filter(pk=pk))
        form = SubZoneForm(request.POST, request.FILES, instance=instance)
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
                title = "Updated an Sub zone",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Sub Zone Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:sub_zones', )
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
        instance = get_object_or_404(SubZone.objects.filter(pk=pk))
        form = SubZoneForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'shops', 
            "page_title" : "Edit Sub zone", 
            "redirect" : True, 
            "url" : reverse('shops:sub_zone_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_sub_zone' : True,
        }

        return render(request, 'dashboard/shops/sub_zone_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_sub_zone'])
def sub_zone_delete(request, pk):
    data = SubZone.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.name,
        title = "Deleted an Sub zone",
    )
    activity.save()
        
    SubZone.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Sub Zone Deleted", 
        "message" : "Sub Zone Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:sub_zones')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@permissions_required(['can_create_zone'])
def zone(request, pk):
    instance = Zone.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Zone', 
        'app_name' :'Shops', 
        'page_title' : 'Zone', 
        'is_need_light_box' : True, 
        'is_zone' : True,
    }
    
    return render(request, 'dashboard/shops/zone.html', context)


@login_required
@permissions_required(['can_create_sub_zone'])
def sub_zone(request, pk):
    instance = SubZone.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Sub Zone', 
        'app_name' :'Shops', 
        'page_title' : 'Sub Zone', 
        'is_need_light_box' : True, 
        'is_sub_zone' : True,
    }
    
    return render(request, 'dashboard/shops/sub_zone.html', context)


@login_required
@permissions_required(['can_create_shop_facility'])
def shop_facility_create(request, pk):
    shop = get_object_or_404(Shop.objects.filter(pk=pk, is_deleted=False))
    
    if request.method == "POST":
        form = ShopFacilityForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(ShopFacility)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.facility,
                title = "Created an Facility on shop ",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Added", 
                "message" : "Facility Successfully Added.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop', kwargs={"pk":shop.pk})
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
        form = ShopFacilityForm(initial={'shop':shop})
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Shop Facility", 
            "redirect" : True, 
            "url" : reverse('shops:shop_facility_create', kwargs={"pk":pk}), 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_facility_entry.html', context)
    

@login_required
@permissions_required(['can_modify_shop_facility'])
def shop_facility_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopFacility.objects.filter(pk=pk))
        form = ShopFacilityForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.facility,
                title = "Updated an Facility on shop ",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Shop Facility Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop', kwargs={"pk":instance.shop.pk})
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
        instance = get_object_or_404(ShopFacility.objects.filter(pk=pk))
        form = ShopFacilityForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Shop Facility", 
            "redirect" : True, 
            "url" : reverse('shops:shop_facility_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop' : True,
        }

        return render(request, 'dashboard/shops/shop_facility_entry.html', context)


@login_required
@permissions_required(['can_delete_shop_facility'])
@ajax_required
def shop_facility_delete(request, pk):
    data = ShopFacility.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.facility,
        title = "Deleted an Facility on shop ",
    )
    activity.save()
    
    ShopFacility.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Shop Facility Deleted", 
        "message" : "Shop Facility Successfully Deleted.", 
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

  
@login_required
@permissions_required(['can_view_shop_facility'])
def shop_facility(request, pk):
    instance =ShopFacility.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Shop Facility', 
        'app_name' :'Shops', 
        'page_title' : 'Menu', 
        'is_need_light_box' : True,
        'is_shop' : True, 
    }
    
    return render(request, 'dashboard/shops/shop_facility.html', context)


@login_required
# @permissions_required(['can_manage_shop_type'])
def shop_timings(request):
    instances=ShopTiming.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(timing__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances, 
        'page_name' : 'Shop Timings', 
        'app_name' :'Shops', 
        'page_title' : 'Shop Timings', 
        'filter_data' : filter_data,
        'is_shop_timing' : True,
    }
    
    return render(request, 'dashboard/shops/shop_timings.html', context)


@login_required
# @permissions_required(['can_view_shop_timing'])
def shop_timing(request, pk):
    instance = ShopTiming.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance, 
        'page_name' : 'Shop timing', 
        'app_name' :'Shops', 
        'page_title' : 'Shop timing', 
        'is_need_light_box' : True, 
        'is_shop_timing' : True,
    }
         
    return render(request, 'dashboard/shops/shop_timing.html', context)


@login_required
# @permissions_required(['can_create_shop_timing'])
def shop_timing_create(request):
    if request.method == "POST":
        form = ShopTimingForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ShopTiming)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="Shop",
                instance = data.timing,
                title = "Created an Shop Timing ",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Shop timing Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('shops:shop_timing', kwargs={"pk": data.pk})
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
        form = ShopTimingForm()
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Create Shop timing", 
            "redirect" : True, 
            "url" : reverse('shops:shop_timing_create'), 
            'is_shop_timing' : True,
        }

        return render(request, 'dashboard/shops/shop_timing_entry.html', context)
    

@login_required
# @permissions_required(['can_modify_shop_timing'])
def shop_timing_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(ShopTiming.objects.filter(pk=pk))
        form = ShopTimingForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="Shop",
                instance = data.timing,
                title = "Updated an Shop Timing ",
            )
            activity.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Shop timing Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('shops:shop_timing', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(ShopTiming.objects.filter(pk=pk))
        form = ShopTimingForm(instance=instance)
        context = {
            "form" : form, 
            'app_name' :'Shops', 
            "page_title" : "Edit Shop timing", 
            "redirect" : True, 
            "url" : reverse('shops:shop_timing_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 
            'is_shop_timing' : True,
        }

        return render(request, 'dashboard/shops/shop_timing_entry.html', context)


@login_required
# @permissions_required(['can_delete_shop_timing'])
@ajax_required
def shop_timing_delete(request, pk):
    data = ShopTiming.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="Shop",
        instance = data.timing,
        title = "Deleted an Shop Timing ",
    )
    activity.save()

    ShopTiming.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Shop timing Deleted", 
        "message" : "Shop timing Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('shops:shop_timings')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


