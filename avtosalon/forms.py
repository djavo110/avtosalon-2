from django.core.exceptions import ValidationError
from django import forms
from .models import *
from captcha.fields import CaptchaField

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class UserLoginForm(forms.Form):
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    password = forms.CharField(label='parol', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}))
    captcha = CaptchaField(required=False)

    class Meta:
        fields = ['username', 'password', 'captcha']
