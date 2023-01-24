from dal import autocomplete

from django.forms import ModelForm, Textarea, TextInput, FileInput, URLInput, Select, BooleanField, CheckboxInput
from django.utils.translation import ugettext_lazy as _
from django import forms

from dishes.models import *


class CuisineForm(ModelForm):
    class Meta:
        model = Cuisine

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'type' : Select(attrs={'class':'form-select',}),
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {
            'name': {
                'required': _("name field is required."),
            }, 
            'type': {
                'required': _("type field is required."),
            },          
        }
        
        
class CategoryForm(ModelForm):
    class Meta:
        model = DishCategory

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            
        }
        
               
class DishForm(ModelForm):
    class Meta:
        model = Dish

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'cuisine': autocomplete.ModelSelect2(url='dishes:autocomplete_cuisine', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Cuisine', 'data-minimum-input-length': 0}),
            'dish_category': autocomplete.ModelSelect2(url='dishes:autocomplete_dish_category', attrs={'class': 'form-control',
                                        'data-placeholder': 'Choose Dish Category', 'data-minimum-input-length': 0}),
            'dish_timing' : Select(attrs={'class':'form-select',}),
            'dietary_type' : Select(attrs={'class':'form-select',}),
        }
        error_messages = {
            'name': {
                'required': _("name field is required."),
            }, 
            'cuisine': {
                'required': _("cuisine field is required."),
            },
            'dish_category': {
                'required': _("dish_category field is required."),
            },          
            'dietary_type': {
                'required': _("dietary_type field is required."),
            },
        }