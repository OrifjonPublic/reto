from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


class Company(models.Model):
    image = models.ImageField(_('Logotip'), upload_to='company/', null=True, blank=True)
    name = models.CharField(_('Korxona Nomi'), max_length=300, null=True, blank=True)
    address = models.CharField(_('Korxona manzili'), max_length=300, null=True, blank=True)
    bio = models.TextField(_('Korxona haqida batafsil...'), null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class Sector(models.Model):
    name = models.CharField(_('Bolim nomi'), max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')
        # ordering = ('name')


class Position(models.Model):
    name = models.CharField(_('Lavozim turi'), max_length=250, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        # ordering = ('name')


class User(AbstractUser):
    rank = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Lavozim'))
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Bo‘lim'))

    def __str__(self) -> str:
        return self.username 

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        # ordering = ('sector')


class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='%(class)s_profile')
    shior = models.CharField(max_length=195, blank=True, null=True, verbose_name=_('Shior'))
    main_task = models.TextField(null=True, blank=True, verbose_name=_('Asosiy vazifa'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Tugilgan sana'))
    phone_number = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        verbose_name=_('Telefon raqami'),
        validators=[RegexValidator(r'^\+998\d{9}$', _('Telefon raqami noto‘g‘ri formatda'))]
    )
    photo = models.ImageField(upload_to='photos', default='photos/1.png', verbose_name=_('Rasmi'))

    class Meta:
            abstract = True


class Direktor(Profile):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='director_profile')
    class Meta:
        verbose_name = _('Direktor')
        verbose_name_plural = _('Direktorlar')
        # ordering = ('user.sector', 'user.username')

class Admin(Profile):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='admin_profile')
    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Adminlar')
        # ordering = ('user.sector', 'user.username')



class Manager(Profile):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='manager_profile')
    class Meta:
        verbose_name = _('Manager')
        verbose_name_plural = _('Managerlar')
        # ordering = ('user.sector', 'user.username')


class Xodim(Profile):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='xodim_profile')
    class Meta:
        verbose_name = _('Xodim')
        verbose_name_plural = _('Xodimlar')
        # ordering = ('user.sector', 'user.username')


class Boshqalar(Profile):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='boshqalar_profile')
    class Meta:
        verbose_name = _('Boshqalar')
        verbose_name_plural = _('Boshqalar')
        # ordering = ('user.sector', 'user.username')


class Notes(models.Model):

    STATUS = (
        ('eng muhim', 'Eng muhim'),
        ('muhim', 'Muhim'),
        ('muhim emas','Muhim emas'),
        ("o'rta","O'rta"),
        ("darajasiz", "Darajasiz"),
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='notes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    label = models.CharField(max_length=30, choices=STATUS, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.title}-{self.content}'
    class Meta:
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
        # ordering = ('-created_at',)


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     return True