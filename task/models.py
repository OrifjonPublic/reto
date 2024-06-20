from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import datetime
from user.models import Sector

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = (
        ('missed', 'Missed'),
        ('doing', 'Doing'),
        ('finished', 'Finished'),
        ('canceled', 'Canceled'),
    )
    PRIVACY_CHOICES = (
        ('open', 'Open'),
        ('secret', 'Secret'),
        ('grouply', 'Grouply')
    )

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_assigned_to')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_assigned_by')
    reason = models.CharField(max_length=400, blank=True, null=True)
    event = models.CharField(max_length=400, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='doing')
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    financial_help = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_changed = models.BooleanField(default=False)
    problem = models.TextField(null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return f"Task was given to {self.assigned_to.username}"

    @property
    def all_days(self):
        if self.deadline:
            return (self.deadline - self.created_at.date()).days
        return None

    @property
    def remain_days(self):
        if self.deadline:
            return (self.deadline - datetime.now().date()).days
        return None


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, related_name='old_tasks')
    new_sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, related_name='new_tasks')
    change_date = models.DateTimeField(auto_now_add=True)



class TaskContent(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    AUDIO = 'audio'
    
    CONTENT_TYPE_CHOICES = [
        (TEXT, _('Text')),
        (IMAGE, _('Image')),
        (AUDIO, _('Audio')),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='contents', verbose_name=_('Task'))
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, verbose_name=_('Content Type'))
    text = models.TextField(null=True, blank=True, verbose_name=_('Text Content'))
    image = models.ImageField(upload_to='task_images/', null=True, blank=True, verbose_name=_('Image Content'))
    audio = models.FileField(upload_to='task_audios/', null=True, blank=True, verbose_name=_('Audio Content'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.get_content_type_display()} - {self.task.id}'

    class Meta:
        verbose_name = _('Task Content')
        verbose_name_plural = _('Task Contents')


class Message(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='messages')
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='conversation_images/', null=True, blank=True)
    audio = models.FileField(upload_to='conversation_audios/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} in conversation {self.task.id}"

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')