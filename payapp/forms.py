from django import forms
from payapp.models import Balance, Exchange


class ExchangeForm(forms.ModelForm):

    class Meta:
      model = Exchange
      fields = ("enter_your_username", "enter_destination_username", "enter_money_to_transfer")


