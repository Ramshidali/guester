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


@login_required
@permissions_required(['can_view_shop_dish'])
def shop_dish(request, pk):
    instance =ShopDish.objects.get(pk=pk, is_deleted=False)
    images =ShopDishImage.objects.filter(is_deleted =False , shop_dish=instance)
    
    context = {
        'instance': instance, 
        'images' : images, 
        'page_name' : 'Shop Menu', 
        'app_name' :'Shop Dishes', 
        'page_title' : 'Shop Menu', 
        'is_need_light_box' : True, 
    }
    
    return render(request, 'dashboard/shop-dashboard/shop_dish.html', context)


@login_required
@permissions_required(['can_manage_shop_dish'])
def shop_dishes(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances =ShopDish.objects.filter(shop=shop, is_deleted=False)
    
    context = {
        'instances': instances, 
        'page_name' : 'Shop Menu', 
        'app_name' :'Shop Dishes', 
        'page_title' : 'Shop Menu', 
        'is_need_light_box' : True, 
    }
    
    return render(request, 'dashboard/shop-dashboard/shop_dishes.html', context)


@login_required
@permissions_required(['can_create_shop_dish'])
def shop_dish_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    
    if request.method == "POST":
        form = ShopDishForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            print("----------")
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(ShopDish)
            data.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Menu Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('dashboard:shop_dishes',)
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
            'app_name' :'Shop Dishes', 
            "page_title" : "Create Menu", 
            "redirect" : True, 
            "url" : reverse('dashboard:shop_dish_create'), 

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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Menu Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('dashboard:shop_dish', kwargs={"pk":instance.pk})
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
        context = {
            "form" : form, 
            'app_name' :'Shop Dishes', 
            "page_title" : "Edit Menu", 
            "redirect" : True, 
            "url" : reverse('dashboard:shop_dish_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 

        }

        return render(request, 'dashboard/shops/shop_dish_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_shop_dish'])
def shop_dish_delete(request, pk):
    ShopDish.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Menu Deleted", 
        "message" : "Menu Successfully Deleted.", 
        "redirect" : True, 
        "url" : reverse('dashboard:shop_dishes'), 
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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Added", 
                "message" : "Dish Image Successfully Added.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('dashboard:shop_dish', kwargs={"pk":shop_dish.pk})
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
            'app_name' :'Shops Dishes', 
            "page_title" : "Add Dish Image", 
            "redirect" : True, 
            "url" : reverse('dashboard:dish_image_create', kwargs={"pk":pk}), 

        }

        return render(request, 'dashboard/shops/dish_image_entry.html', context)
    

@login_required
@ajax_required
@permissions_required(['can_delete_shop_dish_image'])
def dish_image_delete(request, pk):
    ShopDishImage.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Image Deleted", 
        "message" : "Image Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_dish_offer'])
def dish_offers(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances = DishOffer.objects.filter(shop=shop, is_deleted=False)
    
    context = {
        'instances': instances, 
        'page_name' : 'Dish Offers', 
        'app_name' :'Offers', 
        'page_title' : 'Dish Offers', 
        'is_need_light_box' : True, 
    }
    
    return render(request, 'dashboard/shop-dashboard/dish_offers.html', context)


@login_required
@permissions_required(['can_create_dish_offer'])
def dish_offer_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    
    if request.method == "POST":
        form = DishOfferForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(DishOffer)
            data.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Offer Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('dashboard:dish_offers')
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
            'app_name' :'Offers', 
            "page_title" : "Create Offer", 
            "redirect" : True, 
            "url" : reverse('dashboard:dish_offer_create',), 

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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Offer Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('dashboard:dish_offers')
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
            'app_name' :'Offers', 
            "page_title" : "Edit Offer", 
            "redirect" : True, 
            "url" : reverse('dashboard:dish_offer_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 

        }

        return render(request, 'dashboard/shops/dish_offer_entry.html', context)


@login_required
@permissions_required(['can_delete_dish_offer'])
@ajax_required
def dish_offer_delete(request, pk):
    DishOffer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Offer Deleted", 
        "message" : "Offer Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def shop_gallery(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances = ShopGallery.objects.filter(shop=shop, is_deleted=False)
    
    context = {
        'instances': instances, 
        'page_name' : 'Gallery', 
        'app_name' :'Shop Gallery', 
        'page_title' : 'Gallery', 
        'is_need_light_box' : True, 
    }
    
    return render(request, 'dashboard/shop-dashboard/shop_gallery.html', context)



@login_required
@permissions_required(['can_create_shop_gallery'])
def gallery_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Gallery  Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('dashboard:shop_gallery',), 
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
        'app_name' :'Shop Gallery', 
        "page_title" : "Create Gallery", 
        "redirect" : True, 
        "url" : reverse('dashboard:gallery_create',), 
        
    }
    
    return render(request, 'dashboard/shops/gallery_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_shop_gallery'])
def gallery_delete(request, pk):
    ShopGallery.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Gallery Image Deleted", 
        "message" : "Gallery Image Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_more_offer'])
def more_offers(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances = MoreOffer.objects.filter(shop=shop, is_deleted=False)
    
    context = {
        'instances': instances, 
        'page_name' : 'More Offers', 
        'app_name' :'Offers', 
        'page_title' : 'More Offers', 
        'is_need_light_box' : True, 
    }
    
    return render(request, 'dashboard/shop-dashboard/more_offers.html', context)


@login_required
@permissions_required(['can_create_more_offer'])
def more_offer_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    if request.method == "POST":
        form = MoreOfferForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(MoreOffer)
            data.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Offer Successfully Created.", 
                "redirect" : "true", 
                "redirect_url": reverse('dashboard:more_offers')
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
            'app_name' :'Offers', 
            "page_title" : "Create Offer", 
            "redirect" : True, 
            "url" : reverse('dashboard:more_offer_create'), 

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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Offer Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('dashboard:more_offers')
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
            'app_name' :'Offer', 
            "page_title" : "Edit Offer", 
            "redirect" : True, 
            "url" : reverse('dashboard:more_offer_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 

        }

        return render(request, 'dashboard/shops/more_offer_entry.html', context)


@login_required
@permissions_required(['can_delete_more_offer'])
@ajax_required
def more_offer_delete(request, pk):
    MoreOffer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Offer Deleted", 
        "message" : "Offer Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_shop_facility'])
def shop_facilities(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances = ShopFacility.objects.filter(shop=shop, is_deleted=False)
    
    context = {
        'instances': instances, 
        'page_name' : 'More Offers', 
        'app_name' :'Offers', 
        'page_title' : 'More Offers', 
        'is_need_light_box' : True, 
    }
    
    return render(request, 'dashboard/shop-dashboard/shop_facilities.html', context)


@login_required
@permissions_required(['can_create_shop_facility'])
def shop_facility_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    
    if request.method == "POST":
        form = ShopFacilityForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.shop = shop
            data.auto_id = get_auto_id(ShopFacility)
            data.save()

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Added", 
                "message" : "Facility Successfully Added.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('dashboard:shop_facility', kwargs={"pk":data.pk})
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
            'app_name' :'Facilities', 
            "page_title" : "Create Shop Facility", 
            "redirect" : True, 
            "url" : reverse('dashboard:shop_facility_create'), 

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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Shop Facility Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('dashboard:shop_facility', kwargs={"pk":data.pk})
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
            "url" : reverse('dashboard:shop_facility_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 

        }

        return render(request, 'dashboard/shops/shop_facility_entry.html', context)


@login_required
@permissions_required(['can_delete_shop_facility'])
@ajax_required
def shop_facility_delete(request, pk):
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
    }
    
    return render(request, 'dashboard/shops/shop_facility.html', context)


@login_required
@permissions_required(['can_manage_shop_safety'])
def precautions(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances = ShopSafetyPrecaution.objects.filter(shop=shop, is_deleted=False)
    
    context = {
        'instances': instances, 
        'page_name' : 'Precautions', 
        'app_name' :'Extras', 
        'page_title' : 'Precautions', 
        'is_need_light_box' : True, 
    }
    
    return render(request, 'dashboard/shop-dashboard/precautions.html', context)


@login_required
@permissions_required(['can_create_shop_safety'])
def precaution_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
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

            return JsonResponse({
                "status": "success", 
                'stable': "false", 
                'title': 'Successfully Created', 
                'message': 'Precaution Successfully Created', 
                "redirect": 'true', 
                "redirect_url": reverse('dashboard:precautions')
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
            "url": reverse("dashboard:precaution_create"), 
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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Precaution Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('dashboard:precautions')
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
            "url" : reverse('dashboard:precaution_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 

        }

        return render(request, 'dashboard/shops/precaution_edit.html', context)


@login_required
@permissions_required(['can_delete_shop_safety'])
@ajax_required
def precaution_delete(request, pk):
    ShopSafetyPrecaution.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Precaution Deleted", 
        "message" : "Precaution Successfully Deleted.", 
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

     
@login_required
@permissions_required(['can_manage_shop_delivery_partner'])
def delivery_partners(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances=ShopDelivery.objects.filter(shop=shop, is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances, 
        'page_name' : 'Delivery Partner', 
        'app_name' :'Shops', 
        'page_title' : 'Delivery Partner', 
    }
    
    return render(request, 'dashboard/shop-dashboard/delivery_partners.html', context)


@login_required
@permissions_required(['can_create_shop_delivery_partner'])
def delivery_partner_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    
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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Created", 
                "message" : "Delivery Partner Successfully Created.", 
                "redirect" : "true", 
                
                "redirect_url" : reverse('dashboard:delivery_partners')
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
            "url" : reverse('dashboard:delivery_partner_create'), 

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

            response_data = {
                "status" : "success", 
                "stable" : "false", 
                "title" : "Successfully Updated", 
                "message" : "Delivery Partner Successfully Updated.", 
                "redirect" : "true", 
                "redirect_url" : reverse('dashboard:delivery_partners')
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
            "url" : reverse('dashboard:delivery_partner_edit', kwargs={"pk":instance.pk}), 
            "is_edit" :True, 
            "instance" : instance, 

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
@permissions_required(['can_manage_shop_review'])
def shop_reviews(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances=ShopRating.objects.filter(shop=shop,is_deleted=False).order_by("-date_added")
    
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
        'filter_data' : filter_data
    }
    
    return render(request, 'dashboard/shop-dashboard/shop_reviews.html', context)


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
    }
         
    return render(request, 'dashboard/shops/shop_review.html', context)


@login_required
@permissions_required(['can_delete_shop_review'])
@ajax_required
def shop_review_delete(request, pk):
    ShopRating.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success", 
        "title" : "Shop Review Deleted", 
        "message" : "Shop Review Successfully Deleted.", 
        "redirect" : "true", 
        "redirect_url" : reverse('dashboard:shop_reviews')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_shop_offer'])
def shop_offers(request):
    shop = ShopAdmin.objects.get(user=request.user).shop
    instances=ShopOffer.objects.filter(shop=shop, is_deleted=False).order_by("-date_added")
    
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
        'filter_data' : filter_data
    }
    
    return render(request, 'dashboard/shop-dashboard/shop_offers.html', context)


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
    }
         
    return render(request, 'dashboard/shop-dashboard/shop_offer.html', context)


@login_required
@permissions_required(['can_create_shop_offer'])
def shop_offer_create(request):
    shop = ShopAdmin.objects.get(user=request.user).shop 
    if request.method == "POST":
        form = ShopOfferForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.shop = shop
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
                
                "redirect_url" : reverse('dashboard:shop_offer', kwargs={"pk": data.pk})
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
            "url" : reverse('dashboard:shop_offer_create'), 

        }

        return render(request, 'dashboard/shop-dashboard/shop_offer_entry.html', context)
    

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
                "redirect_url" : reverse('dashboard:shop_offer', kwargs={"pk": data.pk})
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

        }

        return render(request, 'dashboard/shop-dashboard/shop_offer_entry.html', context)


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
        "redirect_url" : reverse('dashboard:shop_offers')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

