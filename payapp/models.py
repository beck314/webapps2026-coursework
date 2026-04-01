from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Balance(models.Model):
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='money',
    )
    money = models.IntegerField(default=500)

    def __str__(self):
        return f'{self.money}'


class Exchange(models.Model):
    enter_your_username = models.CharField(max_length=50) ##could be a security issue, sending money from other accounts
    enter_destination_username = models.CharField(max_length=50)
    enter_money_to_transfer = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.enter_your_username} -> {self.enter_destination_username} -> {self.enter_money_to_transfer}'


class Notifications(models.Model):
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    user_requesting = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    amount_requested = models.IntegerField(default=0)