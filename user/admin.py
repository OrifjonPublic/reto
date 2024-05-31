from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Position)
admin.site.register(Sector)

admin.site.register(Direktor)
admin.site.register(Admin)
admin.site.register(Manager)
admin.site.register(Xodim)
