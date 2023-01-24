from registration.forms import RegistrationForm
from dal import autocomplete

from django.forms import ModelForm, Textarea, TextInput, FileInput, URLInput, Select, BooleanField, CheckboxInput, EmailInput
from django.utils.translation import ugettext_lazy as _
from django import forms

from staffs.models import *
from users.models import *


class DesignationForm(ModelForm):
    class Meta:
        model = StaffDesignation
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter designation name'}),
        }
        
        
class StaffForm(ModelForm):
    class Meta:
        model = Staff

        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'user', 'password', 'email','is_active']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'profile': FileInput(attrs={'class': 'form-control file-upload-info file-upload-default'}),
            'phone': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Contact number'}),
            'age': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Age'}),
            'address': Textarea(attrs={'class': 'required form-control ', 'rows':2,'placeholder': 'Contact address'}),
            'salary': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Salary Amount'}),
            
            'account_holder_name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Account Holder Name'}),
            'account_number': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Account Number'}),
            'bank_name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Bank Name'}),
            'bank_branch': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Bank Branch '}),
            'bank_ifsc': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'IFSC Code'}),
            'designation': autocomplete.ModelSelect2(url='staffs:autocomplete_designation',
                                              attrs={'class': 'form-control',
                                                     'data-placeholder': 'Choose Designation',
                                                     'data-minimum-input-length': 0}),
        }
        error_messages = {
            'name': {
                'required': _("Title field is required."),
            },         
        }   


class UserForm(RegistrationForm):
    username = forms.CharField(label=_("Username"),
                               max_length=254,
                               widget=forms.TextInput(
        attrs={'placeholder': 'Enter username', 'class': 'required form-control'})
    )
    email = forms.EmailField(label=_("Email"),
                             max_length=254,
                             widget=forms.TextInput(
        attrs={'placeholder': 'Enter email', 'class': 'required form-control'})
    )
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password', 'class': 'required form-control'})
                                )
    password2 = forms.CharField(label=_("Repeat Password"),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password again', 'class': 'required form-control'})
                                )

    bad_domains = ['guerrillamail.com']

    def clean_email(self):
        email_domain = self.cleaned_data['email'].split('@')[1]
        if User.objects.filter(email__iexact=self.cleaned_data['email'], is_active=True):
            raise forms.ValidationError(
                _("This email address is already in use."))
        elif email_domain in self.bad_domains:
            raise forms.ValidationError(
                _("Registration using %s email addresses is not allowed. Please supply a different email address." % email_domain))
        return self.cleaned_data['email']

    min_password_length = 6

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < self.min_password_length:
            raise forms.ValidationError(
                "Password must have at least %i characters" % self.min_password_length)
        else:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    min_username_length = 6

    def clean_username(self):
        username = self.cleaned_data['username']
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(
                _("A user with that username already exists."))
        elif len(username) < self.min_username_length:
            raise forms.ValidationError(
                "Username must have at least %i characters" % self.min_password_length)
        else:
            return self.cleaned_data['username']

        

class PasswordForm(forms.Form):
    
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password', 'class': 'required form-control'})
                                )
    password2 = forms.CharField(label=_("Repeat Password"),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password again', 'class': 'required form-control'})
                                )