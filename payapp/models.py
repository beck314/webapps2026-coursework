from asyncio.windows_events import NULL

from django.contrib.auth.models import User
from django.db import models
from enum import Enum


Event_Type = (
    ('_r', 'request'),
    ('ar', 'accepted request'),
    ('rr', 'rejected_request'),
    ('sp', 'sent_payment'),
    ('rp', 'received_payment')
)


class Balance(models.Model):
    user = models.ForeignKey(
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
    user_sending_notif = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender'
    )
    user_receiving_notif = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver'
    )
    amount_requested = models.IntegerField(default=0)


class Transactions(models.Model):
    user_sending_transaction = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='individual'
    )
    user_receiving_transaction = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='other'
    )
    event_type = models.CharField(max_length=2, choices=Event_Type, default='')
    amount = models.IntegerField(default=NULL)