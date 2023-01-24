from xmlrpc.client import DateTime
from dal import autocomplete

from django.forms import ModelForm, Textarea, TextInput, FileInput, URLInput, Select, BooleanField, CheckboxInput, EmailInput, HiddenInput, DateTimeInput
from django.utils.translation import ugettext_lazy as _
from django.forms import formset_factory
from django import forms

from shops.models import *
from general.models import *


class FileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control file-upload-info file-upload-default', 'id' : 'input-file-now'}))


class ShopForm(ModelForm):
    class Meta:
        model = Shop

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'user', 'rating', 'rejected_reason', 'location']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'phone': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Phone No'}),
            'email': EmailInput(attrs={'class': 'required email form-control ', 'placeholder': 'Shop Email'}),
            'website_link': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Shop Website Link'}),
            'address': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Shop Location'}),
            'average_cost_for_two': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Average Cost for two'}),
            'logo': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),

            'owner_name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Owner Name'}),
            'manager_name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Manager Name'}),
            'contact_number': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Contact number'}),
            'brand': autocomplete.ModelSelect2(url='brands:autocomplete_brand', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Brand', 'data-minimum-input-length': 0}),
            'badge': autocomplete.ModelSelect2(url='general:autocomplete_badge', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Badge', 'data-minimum-input-length': 0}),
            'shop_type': autocomplete.ModelSelect2(url='shops:autocomplete_shop_type', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Type', 'data-minimum-input-length': 0}),
            'zone': autocomplete.ModelSelect2(url='shops:zone_autocomplete', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Zone', 'data-minimum-input-length': 0}),
            'sub_zone': autocomplete.ModelSelect2(url='shops:autocomplete_sub_zone',forward=['zone'], attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Sub Zone', 'data-minimum-input-length': 0}),
            'shop_timing': autocomplete.ModelSelect2Multiple(url='shops:autocomplete_shop_timing', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Shop Timings', 'data-minimum-input-length': 0}),

        }
        error_messages = {
            'name': {
                'required': _("Title field is required."),
            },
        }


class ShopRejectionForm(ModelForm):
    class Meta:
        model = Shop
        
        fields = ['rejected_reason']
        widgets = {
            'rejected_reason': Textarea(attrs={'class': 'required form-control ', 'rows':3, 'placeholder': ''}),

        }
        error_messages = {
            'rejected_reason': {
                'required': _("This field is required."),
            },
        }


class ShopTypeForm(ModelForm):
    class Meta:
        model = ShopType

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'icon': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {
            'name': {
                'required': _("Name field is required."),
            },
            'icon': {
                'required': _("icon field is required."),
            },
            'image': {
                'required': _("image field is required."),
            },
        }


class ShopTimingForm(ModelForm):
    class Meta:
        model = ShopTiming

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'timing': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Add Timing'}),
        }
        error_messages = {
            'timing': {
                'required': _("timing field is required."),
            },
        }


class GalleryTypeForm(ModelForm):
    class Meta:
        model = ShopGalleryType

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
        }
        error_messages = {

        }


class GalleryForm(ModelForm):
    class Meta:
        model = ShopGallery

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop']
        widgets = {
            'file': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'thumbnail': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'file_type':  Select(attrs={'class':'form-select',}),
            'gallery_type': autocomplete.ModelSelect2(url='shops:autocomplete_gallery_type', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Gallery Type', 'data-minimum-input-length': 0}),
        }
        error_messages = {

        }


class PartnerForm(ModelForm):
    class Meta:
        model = ShopDelivery

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop']
        widgets = {
            'shop_link': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Delivery Partner Link'}),
            'delivery_partner': autocomplete.ModelSelect2(url='shops:autocomplete_delivery', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Delivery Partner', 'data-minimum-input-length': 0}),
        }
        error_messages = {

        }


class ShopDishForm(ModelForm):
    class Meta:
        model = ShopDish

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop']
        widgets = {
            'price': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Price'}),
            'featured_image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'dish': autocomplete.ModelSelect2(url='shops:autocomplete_dish', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Dish', 'data-minimum-input-length': 0}),
            'description': Textarea(attrs={'class': 'required form-control ', 'rows':3, 'placeholder': ''}),
        }
        error_messages = {

        }


class DishImageForm(ModelForm):
    class Meta:
        model = ShopDishImage

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop_dish']
        widgets = {
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {

        }


class DishOfferForm(ModelForm):
    class Meta:
        model = DishOffer

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'shop' : HiddenInput(),
            'offer_type': Select(attrs={'class': 'required form-control ', 'data-placeholder': 'Choose Dish'}),
            'offer': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Offer Here'}),
            'shop_dish': autocomplete.ModelSelect2(url='shops:autocomplete_shop_dish', forward=['shop', ],attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Dish', 'data-minimum-input-length': 0}),
            'start_date' : DateTimeInput(attrs={'class': 'required form-control ', 'type':'datetime-local', 'placeholder': 'Start Date'}),
            'end_date' : DateTimeInput(attrs={'class': 'required form-control ', 'type':'datetime-local', 'placeholder': 'End Date'}),
        }
        error_messages = {

        }


class PrecautionForm(ModelForm):
    class Meta:
        model = ShopSafetyPrecaution

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control ','required':'required', 'placeholder': 'Add Precaution'}),
        }
        error_messages = {

        }


class WorkingDayForm(ModelForm):

    start_time = forms.TimeField(label='From', label_suffix=" : ",
                             required=True, disabled=False, input_formats=["%H:%M"],
                             widget=forms.TimeInput(attrs={'class': 'form-control','type': 'time','required':'required'}),
                             error_messages={'required': "This field is required."})

    end_time = forms.TimeField(label='To', label_suffix=" : ",
                             required=True, disabled=False, input_formats=["%H:%M"],
                             widget=forms.TimeInput(attrs={'class': 'form-control','type': 'time','required':'required'}),
                             error_messages={'required': "This field is required."})
    class Meta:
        model = ShopWorkingDay

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop', 'start_time', 'end_time']
        widgets = {
            'day': autocomplete.ModelSelect2(url='shops:autocomplete_day', attrs={'class': 'form-control','required':'required',
                                        'data-placeholder': 'Choose Day', 'data-minimum-input-length': 0}),

        }
        error_messages = {

        }


class MoreOfferForm(ModelForm):
    class Meta:
        model = MoreOffer

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop']
        widgets = {
            'title': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Offer Title'}),
            'description': Textarea(attrs={'class': 'required form-control ','rows':3, 'placeholder': 'Offer Description Here'}),
            'icon': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {

        }


class ShopOfferForm(ModelForm):

    class Meta:
        model = ShopOffer

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'title': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Offer Title'}),
            'shop': autocomplete.ModelSelect2(url='shops:autocomplete_shop', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Shop', 'data-minimum-input-length': 0}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'start_date' : DateTimeInput(attrs={'class': 'required form-control ', 'type':'datetime-local', 'placeholder': 'Start Date'}),
            'end_date' : DateTimeInput(attrs={'class': 'required form-control ', 'type':'datetime-local', 'placeholder': 'End Date'}),
        }
        error_messages = {

        }


class BrandOfferForm(ModelForm):
    class Meta:
        model = BrandOffer

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'title': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Offer Title'}),
            'brand': autocomplete.ModelSelect2(url='brands:autocomplete_brand', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Brand', 'data-minimum-input-length': 0}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'start_date' : DateTimeInput(attrs={'class': 'required form-control ', 'type':'datetime-local', 'placeholder': 'Start Date'}),
            'end_date' : DateTimeInput(attrs={'class': 'required form-control ', 'type':'datetime-local', 'placeholder': 'End Date'}),
        }
        error_messages = {

        }


class ZoneForm(ModelForm):
    class Meta:
        model = Zone

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'zone': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Zone'}),
        }
        error_messages = {
            'zone': {
                'required': _("Zone Name required."),
            },
        }


class SubZoneForm(ModelForm):
    class Meta:
        model = SubZone

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Sub Zone'}),
            'zone': autocomplete.ModelSelect2(url='shops:zone_autocomplete', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Zone', 'data-minimum-input-length': 0}),
        }
        error_messages = {
            'name': {
                'required': _("Zone Name required."),
            },
        }


class ShopFacilityForm(ModelForm):
    class Meta:
        model = ShopFacility

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'shop']
        widgets = {
            'description': Textarea(attrs={'class': 'required form-control ', 'rows':2, 'placeholder': 'Facility Description....'}),
            'facility': autocomplete.ModelSelect2(url='shops:facility_autocomplete',
                                          attrs={ 'class': 'required form-control ', 'data-placeholder': 'Select Facilities', 'data-minimum-input-length': 0},),
            'image_1': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'image_2': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'image_3': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),

        }
        error_messages = {
            'description': {
                'required': _("This field is required."),
            },
        }