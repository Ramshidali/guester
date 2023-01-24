import json
import datetime

from dal import  autocomplete

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from main.decorators import role_required, ajax_required, permissions_required
from main.functions import generate_form_errors, get_auto_id
from general.functions import get_or_create_location
from general.models import *
from general.forms import *


class BadgeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Badge.objects.none()

        items = Badge.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) | 
                                 Q(title__istartswith=self.q) 
                                )

        return items


@login_required
@permissions_required(['can_manage_facility'])
def facilities(request):
    instances = Facility.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(title__icontains=query) 
        )
        filter_data['q'] = query
    
    
    context = {
        'instances': instances,
        'page_name' : 'Facilities',
        'app_name' :'General',
        'is_facility' : True,
        'page_title' : 'Facilities',
        'filter_data' : filter_data
    }
    
    return render(request, 'dashboard/general/facilities.html', context)


@login_required
@permissions_required(['can_view_facility'])
def facility(request, pk):
    instance = Facility.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Facility',
        'app_name' :'General',
        'page_title' : 'Facility',
        'is_need_light_box' : True,
        'is_facility' : True,
    }
         
    return render(request, 'dashboard/general/facility.html', context)


@login_required
@permissions_required(['can_create_facility'])
def facility_create(request):
    if request.method == "POST":
        form = FacilityForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Facility)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="General",
                instance = data.title,
                title = "Created an Facility",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Created",
                "message" : "Facility Successfully Created.",
                "redirect" : "true",
                
                "redirect_url" : reverse('general:facility', kwargs={"pk": data.pk})
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
        form = FacilityForm()
        context = {
            "form" : form,
            'app_name' :'General',
            "page_title" : "Create Facility",
            "redirect" : True,
            'is_facility' : True,
            "url" : reverse('general:facility_create'),

        }

        return render(request, 'dashboard/general/facility_entry.html', context)
    

@login_required
@permissions_required(['can_modify_facility'])
def facility_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Facility.objects.filter(pk=pk))
        form = FacilityForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="General",
                instance = data.title,
                title = "Updated an Facility",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Updated",
                "message" : "Facility Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('general:facility', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(Facility.objects.filter(pk=pk))
        form = FacilityForm(instance=instance)
        context = {
            "form" : form,
            'app_name' :'General',
            "page_title" : "Edit Facility",
            "redirect" : True,
            "url" : reverse('general:facility_edit', kwargs={"pk":instance.pk}),
            "is_edit" :True,
            'is_facility' : True,
            "instance" : instance,

        }

        return render(request, 'dashboard/general/facility_entry.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_facility'])
def facility_delete(request, pk):
    instance = Facility.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="General",
        instance = instance.title,
        title = "Deleted an Facility",
    )
    activity.save()    

    Facility.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success",
        "title" : "Facility Deleted",
        "message" : "Facility Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('general:facilities')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_badge'])
def badges(request):
    instances = Badge.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(title__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Badges',
        'app_name' :'General',
        'page_title' : 'badges',
        'is_badge' : True,
        'filter_data' : filter_data,
    }
    
    return render(request, 'dashboard/general/badges.html', context)


@login_required
@permissions_required(['can_view_badge'])
def badge(request, pk):
    instance = Badge.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Badge',
        'app_name' :'Badges',
        'page_title' : 'Badge',
        'is_need_light_box' : True,
        'is_badge' : True,
    }
    
    return render(request, 'dashboard/general/badge.html', context)


@login_required
@permissions_required(['can_create_badge'])
def badge_create(request):
    if request.method == "POST":
        form = BadgeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Badge)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="General",
                instance = data.title,
                title = "Created an Badge",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Created",
                "message" : "Badge Successfully Created.",
                "redirect" : "true",
                
                "redirect_url" : reverse('general:badge', kwargs={"pk": data.pk})
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
        form = BadgeForm()
        context = {
            "form" : form,
            'app_name' :'Badges',
            "page_title" : "Create badge",
            "redirect" : True,
            'is_badge' : True,
            "url" : reverse('general:badge_create'),

        }

        return render(request, 'dashboard/general/badge_entry.html', context)
    

@login_required
@permissions_required(['can_modify_badge'])
def badge_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Badge.objects.filter(pk=pk))
        form = BadgeForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="General",
                instance = data.title,
                title = "Updated an Facility",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Updated",
                "message" : "Badge Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('general:badge', kwargs={"pk": instance.pk})
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
        instance = get_object_or_404(Badge.objects.filter(pk=pk))
        form = BadgeForm(instance=instance)
        context = {
            "form" : form,
            'app_name' :'Badges',
            "page_title" : "Edit badge",
            "redirect" : True,
            "url" : reverse('general:badge_edit', kwargs={"pk":instance.pk}),
            "is_edit" :True,
            'is_badge' : True,
            "instance" : instance,

        }
        
        return render(request, 'dashboard/general/badge_entry.html', context)


@login_required
@permissions_required(['can_delete_badge'])
@ajax_required
def badge_delete(request, pk):
    instance = Badge.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="General",
        instance = instance.title,
        title = "Deleted an Facility",
    )
    activity.save()
    
    Badge.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success",
        "title" : "Badge Deleted",
        "message" : "Badge Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('general:badges')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_days'])
def days(request):
    instances = Days.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(day__icontains=query) 
        )
        filter_data['q'] = query
       
    context = {
        'instances': instances,
        'page_name' : 'Days',
        'app_name' :'General',
        'page_title' : 'Days',
        'is_days' : True,
        'filter_data' : filter_data
    }
    
    return render(request, 'dashboard/general/days.html', context)


@login_required
@permissions_required(['can_view_days'])
def day(request, pk):
    instance = Days.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Day',
        'app_name' :'Days',
        'page_title' : 'Day',
        'is_days' : True,
        'is_need_light_box' : True,
    }
    
    return render(request, 'dashboard/general/day.html', context)


@login_required
@permissions_required(['can_create_days'])
def day_create(request):
    if request.method == "POST":
        form = DaysForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Days)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="General",
                instance = data.day,
                title = "Created an Day",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Created",
                "message" : "Day Successfully Created.",
                "redirect" : "true",
                
                "redirect_url" : reverse('general:day', kwargs={"pk": data.pk})
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
        form = DaysForm()
        context = {
            "form" : form,
            'app_name' :'Days',
            "page_title" : "Create day",
            "redirect" : True,
            "url" : reverse('general:day_create'),
            'is_days' : True,
        }
        
        return render(request, 'dashboard/general/day_entry.html', context)
    

@login_required
@permissions_required(['can_modify_days'])
def day_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Days.objects.filter(pk=pk))
        form = DaysForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="General",
                instance = data.day,
                title = "Updated an Day",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Updated",
                "message" : "Day Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('general:day', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(Days.objects.filter(pk=pk))
        form = DaysForm(instance=instance)
        context = {
            "form" : form,
            'app_name' :'Days',
            "page_title" : "Edit day",
            "redirect" : True,
            "url" : reverse('general:day_edit', kwargs={"pk":instance.pk}),
            "is_edit" :True,
            "instance" : instance,
            'is_days' : True,
        }
        
        return render(request, 'dashboard/general/day_entry.html', context)


@login_required
@permissions_required(['can_delete_days'])
@ajax_required
def day_delete(request, pk):
    Days.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success",
        "title" : "Day Deleted",
        "message" : "Day Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('general:days')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_manage_delivery_partner'])
def delivery_partners(request):
    instances = Delivery.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Delivery Partners',
        'app_name' :'General',
        'page_title' : 'Delivery Partners',
        'filter_data' : filter_data,
        'is_dp' : True,
    }
    
    return render(request, 'dashboard/general/delivery_partners.html', context)


@login_required
@permissions_required(['can_view_delivery_partner'])
def delivery(request, pk):
    instance = Delivery.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Delivery Partner',
        'app_name' :'General',
        'page_title' : 'Delivery Partner',
        'is_need_light_box' : True,
        'is_dp' : True,
    }
    
    return render(request, 'dashboard/general/delivery.html', context)


@login_required
@permissions_required(['can_create_delivery_partner'])
def delivery_create(request):
    if request.method == "POST":
        form = DeliveryForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Delivery)
            data.save()

            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="General",
                instance = data.name,
                title = "Created an Delivery Partner",
            )
            activity.save()
            
            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Created",
                "message" : "Delivery Partner Successfully Created.",
                "redirect" : "true",
                
                "redirect_url" : reverse('general:delivery', kwargs={"pk": data.pk})
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
        form = DeliveryForm()
        context = {
            "form" : form,
            'app_name' :'General',
            "page_title" : "Create Delivery Partner",
            "redirect" : True,
            "url" : reverse('general:delivery_create'),
            'is_dp' : True,
        }
        
        return render(request, 'dashboard/general/delivery_entry.html', context)
    

@login_required
@permissions_required(['can_modify_delivery_partner'])
def delivery_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Delivery.objects.filter(pk=pk))
        form = DeliveryForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="General",
                instance = data.name,
                title = "Updated an Delivery Partner",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Updated",
                "message" : "Delivery Partner Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('general:delivery', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(Delivery.objects.filter(pk=pk))
        form = DeliveryForm(instance=instance)
        context = {
            "form" : form,
            'app_name' :'General',
            "page_title" : "Edit Delivery Partner",
            "redirect" : True,
            "url" : reverse('general:delivery_edit', kwargs={"pk":instance.pk}),
            "is_edit" :True,
            "instance" : instance,
            'is_dp' : True,
        }

        return render(request, 'dashboard/general/delivery_entry.html', context)


@login_required
@permissions_required(['can_delete_delivery_partner'])
@ajax_required
def delivery_delete(request, pk):
    instance = Delivery.objects.get(pk=pk)
    
    activity = UserActivity(
        user=request.user,
        activity_type="Delete",
        app="General",
        instance = instance.name,
        title = "Deleted an Delivery Partner",
    )
    activity.save()
    
    Delivery.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success",
        "title" : "Delivery Partner Deleted",
        "message" : "Delivery Partner Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('general:delivery_partners')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_create_location'])
def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)

        if form.is_valid():

            location_name = form.cleaned_data['location']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            location = get_or_create_location(request, form, location_name, latitude, longitude)

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Created",
                "message" : "Location Successfully Created.",
                "redirect" : "true",
                "redirect_url": reverse('general:location', kwargs={'pk': location.pk})
            }
            
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

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
        form = LocationForm()

        context = {
            'page_name' : 'Create Location',
            'app_name' :'General',
            'page_title' : 'Create Location',
            "url": reverse('general:location_create'),
            "form": form,
            "redirect": True,
            'is_location' : True,
        }

        return render(request, 'dashboard/general/location_entry.html', context)
    
    
@login_required
@permissions_required(['can_view_location'])
def location(request, pk):
    instance = Location.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Location',
        'app_name' :'General',
        'page_title' : 'Location',
        'is_need_light_box' : True,
        'is_location' : True,
    }
    
    return render(request, 'dashboard/general/location.html', context)


@login_required
@permissions_required(['can_manage_location'])
def locations(request):
    instances = Location.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:
        instances = instances.filter(
            Q(location__icontains=query) 
        )
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Locations',
        'app_name' :'General',
        'page_title' : 'Locations',
        'filter_data' : filter_data,
        'is_location' : True,
    }
    
    return render(request, 'dashboard/general/locations.html', context)


@login_required
@ajax_required
@permissions_required(['can_delete_location'])
def location_delete(request, pk):
    Location.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success",
        "title" : "Location Deleted",
        "message" : "Location Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('general:locations')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@permissions_required(['can_modify_location'])
def location_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Location.objects.filter(pk=pk))
        form = LocationForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            location_name = form.cleaned_data['location']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            location = get_or_create_location(request,  form, location_name, latitude, longitude)

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Updated",
                "message" : "Location Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('general:location', kwargs={"pk": location.pk})
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
        instance = get_object_or_404(Location.objects.filter(pk=pk))
        form = LocationForm(instance=instance)
        context = {
            "form" : form,
            'app_name' :'General Name',
            "page_title" : "Edit Location ",
            "redirect" : True,
            "url" : reverse('general:location_edit', kwargs={"pk":instance.pk}),
            "is_edit" :True,
            "instance" : instance,
            'is_location' : True,
        }

        return render(request, 'dashboard/general/location_entry.html', context)


@login_required
@permissions_required(['can_manage_spotlight'])
def spotlights(request):
    instances = Spotlight.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Spotlights',
        'app_name' :'General',
        'page_title' : 'Spotlights',
        'is_spotlight' : True,
    }
    
    return render(request, 'dashboard/general/spotlights.html', context)


@login_required
@permissions_required(['can_view_spotlight'])
def spotlight(request, pk):
    instance = Spotlight.objects.get(pk=pk, is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Spotlight',
        'app_name' :'General',
        'page_title' : 'Spotlight',
        'is_need_light_box' : True,
        'is_spotlight' : True,
    }
    
    return render(request, 'dashboard/general/spotlight.html', context)


@login_required
@permissions_required(['can_create_spotlight'])
def spotlight_create(request):
    if request.method == "POST":
        form = SpotlightForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Spotlight)
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Create",
                app="General",
                instance = "Image",
                title = "Created an Spotlight",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Created",
                "message" : "Spotlight Successfully Created.",
                "redirect" : "true",
                
                "redirect_url" : reverse('general:spotlight', kwargs={"pk": data.pk})
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
        form = SpotlightForm()
        context = {
            "form" : form,
            'app_name' :'General',
            "page_title" : "Create Spotlight",
            "redirect" : True,
            "url" : reverse('general:spotlight_create'),
            'is_spotlight' : True,
        }

        return render(request, 'dashboard/general/spotlight_entry.html', context)
    

@login_required
@permissions_required(['can_modify_spotlight'])
def spotlight_edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Spotlight.objects.filter(pk=pk))
        form = SpotlightForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()
            
            activity = UserActivity(
                user=request.user,
                activity_type="Update",
                app="General",
                instance = "Image",
                title = "Updated an Spotlight",
            )
            activity.save()

            response_data = {
                "status" : "success",
                "stable" : "false",
                "title" : "Successfully Updated",
                "message" : "Spotlight Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('general:spotlight', kwargs={"pk": data.pk})
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
        instance = get_object_or_404(Spotlight.objects.filter(pk=pk))
        form = SpotlightForm(instance=instance)
        context = {
            "form" : form,
            'app_name' :'Spotlights',
            "page_title" : "Edit Spotlight",
            "redirect" : True,
            "url" : reverse('general:spotlight_edit', kwargs={"pk":instance.pk}),
            "is_edit" :True,
            "instance" : instance,
            'is_spotlight' : True,
        }

        return render(request, 'dashboard/general/spotlight_entry.html', context)


@login_required
@permissions_required(['can_delete_spotlight'])
@ajax_required
def spotlight_delete(request, pk):
    Spotlight.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "success",
        "title" : "Spotlight Deleted",
        "message" : "Spotlight Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('general:spotlights')
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')