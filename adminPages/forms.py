from django import forms
from django.contrib.auth.models import User

from adminPages.models import AdminUsers


class new_admin_form(forms.Form):

    class Meta:
        model = AdminUsers
        fields = "username"
