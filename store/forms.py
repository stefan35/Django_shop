from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    psc = forms.CharField(max_length=20)
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2', 'address', 'city', 'psc', 'country']

