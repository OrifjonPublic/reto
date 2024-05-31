from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

from user.example import decrease


User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateField(input_formats=['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'])
    
    class Meta:
        model = Task
        fields = [
            'id', 'assigned_to','assigned_by', 'reason', 'event', 'deadline',
            'status', 'privacy', 'financial_help', 'problem'    ]
        extra_kwargs = {
            'assigned_by': {'read_only': True}}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')

    def validate(self, data):
        if self.request and not self.request._authenticate:
            raise serializers.ValidationError('Must be logged in')
        return data
    

    def create(self, validated_data):
        user = self.request.user
        task = Task.objects.create(assigned_by=user,**validated_data)
        images = validated_data.getlist('images')
        for i in images:    
            TaskContent.objects.create(task = task, content_type='image', image=i)
        audios = validated_data.getlist('audios')
        for i in audios:    
            TaskContent.objects.create(task = task, content_type='audio', audio=i)
        texts = validated_data.getlist('texts')
        for i in texts:    
            TaskContent.objects.create(task = task, content_type='text', text=i)
        return task

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class TaskContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskContent 
        fields = ['task', 'audio', 'image', 'text']
        extra_kwargs = {
            'audio': {'read_only': True},
            'image': {'read_only': True},
            'text': {"read_only": True}, 
        }
    
    def create(self, validated_data):
        audios = validated_data.getlist('audio')
        texts = validated_data.getlist('text')
        images = validated_data.getlist('image')
        
        if audios:
            for i in audios:
                TaskContent.objects.create(
                    task=validated_data.get('task'),
                    content_type='audio',
                    audio = i
                    )
        if texts:
            for i in texts:
                TaskContent.objects.create(
                    task=validated_data.get('task'),
                    content_type='text',
                    text = i
                    )
        if images:
            for i in images:
                a = TaskContent.objects.create(
                    task=validated_data.get('task'),
                    content_type='image',
                    image = i
                    )
        
        return a


class TaskMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['task', 'sender']
        extra_kwargs = {
            'sender': {'read_only': True},
           
        }
    def create(self, validated_data):
        user = self.context.get('request').user
        audios = validated_data.getlist('audio')
        texts = validated_data.getlist('text')
        images = validated_data.getlist('image')
        
        if audios:
            for i in audios:
                Message.objects.create(
                    task=validated_data.get('task'),
                    sender=user,
                    audio = i
                    )
        if texts:
            for i in texts:
                Message.objects.create(
                    task=validated_data.get('task'),
                    sender=user,
                    text = i
                    )
        if images:
            for i in images:
                a = Message.objects.create(
                    task=validated_data.get('task'),
                    sender=user,
                    image = i
                    )
        
        return a
