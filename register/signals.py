from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from register.models import User_Info

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Info.objects.create(user=instance)

