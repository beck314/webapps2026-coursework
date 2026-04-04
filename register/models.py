from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.

class User_Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_name')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def _str_(self):
        return self.first_name + " " + self.last_name  + "(" + self.phone + ")"