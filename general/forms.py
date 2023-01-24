from django.forms import ModelForm, TextInput, FileInput, Textarea
from django.utils.translation import ugettext_lazy as _
from django import forms

from general.models import *


class FacilityForm(ModelForm):
    class Meta:
        model = Facility

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'title': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Title'}),
            'icon': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {
            'title': {
                'required': _("Title field is required."),
            }, 
            'icon': {
                'required': _("Icon field is required."),
            },          
        }


class BadgeForm(ModelForm):
    class Meta:
        model = Badge

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'title': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Title'}),
            'icon': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'description': Textarea(attrs={'class': 'required form-control ', 'placeholder': 'Description'}),
        }
        error_messages = {
            'title': {
                'required': _("Title field is required."),
            }, 
            'icon': {
                'required': _("Icon field is required."),
            }, 
            'description': {
                'required': _("Description field is required."),
            },          
        }
        
        
class DaysForm(ModelForm):
    class Meta:
        model = Days

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'day': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Enter Day Here'}),
        }
        error_messages = {
            'day': {
                'required': _("Day field is required."),
            }, 
                      
        }
        
        
class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'logo': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {
            'name': {
                'required': _("Name field is required."),
            }, 
            'logo': {
                'required': _("logo field is required."),
            },          
        }
        
        
class LocationForm(forms.ModelForm):
    
    class Meta:
        model = Location
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'location': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Location'}),
            'latitude': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Latitude'}),
            'longitude': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Longitude'}),
        }


class SpotlightForm(ModelForm):
    class Meta:
        model = Spotlight

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {
            'image': {
                'required': _("Icon field is required."),
            }, 
        }