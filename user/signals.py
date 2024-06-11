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
            if instance.rank.name=='direktor':  
                Direktor.objects.create(user=instance)
            elif instance.rank.name == 'manager':  # Replace 'Manager' with appropriate condition
                Manager.objects.create(user=instance)
            elif instance.rank.name == 'xodim':
                Xodim.objects.create(user=instance)
            else:
                Boshqalar.objects.create(user=instance)
        else:
            admin = Position.objects.get_or_create(name='Admin')
            Position.objects.get_or_create(name='Direktor')
            Position.objects.get_or_create(name='Xodim')
            Position.objects.get_or_create(name='Manager')
            admin_user = Admin.objects.get_or_create(user=instance)
            admin_user.rank = admin
            admin_user.save()
