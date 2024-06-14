# Generated by Django 4.2.7 on 2024-06-11 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_sector_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='boshqalar',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boshqalar_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='direktor',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='director_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='manager',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='xodim',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='xodim_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]