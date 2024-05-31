# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.rank is not None:
            if instance.rank.name=='Direktor':  
                Direktor.objects.create(user=instance)
            elif instance.rank.name == 'Manager':  # Replace 'Manager' with appropriate condition
                Manager.objects.create(user=instance)
            elif instance.rank.name == 'Xodim':
                Xodim.objects.create(user=instance)
            else:
                Boshqalar.objects.create(user=instance)
        else:
            Position.objects.get_or_create(name='Admin')
            Position.objects.get_or_create(name='Direktor')
            Position.objects.get_or_create(name='Xodim')
            Position.objects.get_or_create(name='Manager')
            Admin.objects.get_or_create(user=instance)
