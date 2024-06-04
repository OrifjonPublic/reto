from django.contrib import admin
from .models import Task, Message, TaskContent


admin.site.register(Task)
admin.site.register(TaskContent)
admin.site.register(Message)
