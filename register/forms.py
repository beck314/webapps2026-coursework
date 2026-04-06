from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from register.models import User_Info


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    class Meta:
      model = User
      fields = ["username", "email", "password1", "password2"]


class InfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User_Info
        fields = ["first_name", "last_name", "phone"]

