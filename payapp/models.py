from django.db import models
from django.db.models import Model


# Create your models here.

class UserAccount(models.Model):
    username = models.CharField(max_length = 100)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    money = models.IntegerField(default=500)

    class Meta:
        db_table = 'user'

    def __str__(self):
        details = ''
        details += f'Name        : {self.username}\n'
        details += f'VisitDate   : {self.email}\n'
        details += f'Comment     : {self.money}\n'
        return details
