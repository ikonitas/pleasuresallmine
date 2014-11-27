# coding=utf-8

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from accounts.models import UserProfile, Address
from accounts.choice_list import SOCIAL_TITLE_CHOICES


class RegistrationForm(forms.Form):
    title = forms.ChoiceField(choices=SOCIAL_TITLE_CHOICES)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.CharField(max_length=50)
    email = forms.EmailField()
    confirm_email = forms.EmailField(
            help_text="Enter your e-mail address again to confirm")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput,
            help_text="Enter your password again to confirm")
    phone = forms.CharField(max_length=30)
    line_1 = forms.CharField(label="Address 1", max_length=50)
    line_2 = forms.CharField(label="Address 2", max_length=50, required=False)
    city = forms.CharField(label='Town/City', max_length=50)
    county = forms.CharField(max_length=50, required=False)
    postcode = forms.CharField(label="Postcode",
            max_length=10, widget=forms.TextInput(attrs={'size':40},))
    terms = forms.BooleanField(
            label=mark_safe('I agree to the website terms and conditions'),
            error_messages ={'required': 'You must agree to the website terms and conditions.'},
            )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        try:
            user = User.objects.get(email=email)
            if user is not None:
                raise forms.ValidationError('E-mail address already taken.')
        except User.DoesNotExist:
            pass

        return email

    def clean_confirm_email(self):
        email = self.cleaned_data.get('email', '').lower()
        confirm_email = self.cleaned_data.get('confirm_email', '').lower()
        if email != confirm_email:
            raise forms.ValidationError('E-mail  address are not the same.')
        return confirm_email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password', '')
        confirm_password = self.cleaned_data.get('confirm_password', '').lower()
        if password != confirm_password:
            raise forms.ValidationError('The entered passwords do not match.')
        return confirm_password


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', max_length=250)
    password = forms.CharField(max_length='', widget=forms.PasswordInput,
                                               required=False)


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'full_name', 'type', 'company_name',)


class RegistrationFormAdmin(forms.Form):
    title = forms.ChoiceField(choices=SOCIAL_TITLE_CHOICES, required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.CharField(max_length=50)
    email = forms.EmailField()
    confirm_email = forms.EmailField(
            help_text="Enter your e-mail address again to confirm")
    phone = forms.CharField(max_length=30)
    line_1 = forms.CharField(label="Address 1", max_length=50)
    line_2 = forms.CharField(label="Address 2", max_length=50, required=False)
    city = forms.CharField(label='Town/City', max_length=50)
    county = forms.CharField(max_length=50, required=False)
    postcode = forms.CharField(label="Postcode",
            max_length=10, widget=forms.TextInput(attrs={'size':40},))
    terms = forms.BooleanField(
            label=mark_safe('I agree to the website terms and conditions'),
            error_messages ={'required': 'You must agree to the website terms and conditions.'},
            )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        try:
            user = User.objects.get(email=email)
            if user is not None:
                raise forms.ValidationError('E-mail address already taken.')
        except User.DoesNotExist:
            pass

        return email
