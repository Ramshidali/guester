from django.forms import ModelForm, TextInput, FileInput, Textarea
from django.utils.translation import ugettext_lazy as _
from django import forms

from brands.models import *


class BrandForm(ModelForm):
    class Meta:
        model = Brand

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'image': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'logo': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
        }
        error_messages = {
            'name': {
                'required': _("Name field is required."),
            }, 
            'logo': {
                'required': _("logo field is required."),
            }, 
            'image': {
                'required': _("image field is required."),
            },          
        }


