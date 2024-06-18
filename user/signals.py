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
            if instance.rank.name=='director':  
                Direktor.objects.create(user=instance)
            elif instance.rank.name == 'manager':  # Replace 'Manager' with appropriate condition
                Manager.objects.create(user=instance)
            elif instance.rank.name == 'xodim':
                Xodim.objects.create(user=instance)
            elif instance.rank.name == 'admin':
                Admin.objects.create(user=instance)
            else:
                Boshqalar.objects.create(user=instance)
        else:
            admin = Position.objects.get_or_create(name='admin')[0]
            Position.objects.get_or_create(name='director')
            Position.objects.get_or_create(name='xodim')
            Position.objects.get_or_create(name='manager')
            admin_user = Admin.objects.get_or_create(user=instance)[0]
            instance.rank = admin
            instance.save()
            admin_user.save()
