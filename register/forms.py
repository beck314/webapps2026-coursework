from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    fields = ["username", "firstName", "lastName", "email", "password1", "password2"]
    email = forms.EmailField()

    class Meta:
      model = User
      fields = ["username", "firstName", "lastName", "email", "password1", "password2"]

class LoginForm(forms.Form):
    fields = ["username", "password"]
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
      model = User
      fields = ["username", "password"]