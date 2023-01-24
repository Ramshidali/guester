
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput, Textarea, Select, HiddenInput, FileInput, EmailInput
from users import models
from users.models import *


class LoginForm(forms.Form):
    
    username = forms.CharField(
        label=_("Username"),
        max_length=254,
        widget=TextInput(
            attrs={
                'placeholder': 'Enter username',
                'class': 'required user-input form-control'
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter password',
                'class': 'required form-control'
            }
        )
    )
