from django import forms
from payapp.models import Balance, Exchange


class ExchangeForm(forms.ModelForm):
    enter_your_username = forms.HiddenInput()

    class Meta:
      model = Exchange
      fields = ("enter_destination_username", "enter_money_to_transfer")


