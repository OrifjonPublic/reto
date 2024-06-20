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
            'assigned_by': {'read_only': True},
            'reason': {'required': False, 'default': ''},
            'event': {'required': False, 'default': ''},
            'status': {'required': False, 'default': 'doing'},
            'privacy': {'required': False, 'default': 'open'},
            'financial_help': {'required': False},
            'problem': {'required': False, 'default': ''}
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')

    def validate(self, data):
        if self.request and not self.request._authenticate:
            raise serializers.ValidationError('user must be log in :)')
        if self.request.user == data.get('assigned_to'):
            raise serializers.ValidationError('Bir kishi bir vaqtda topshiriq beruvchi va bajaruvchi bola olmaydi')
        return data
    
    def create(self, validated_data):
        if not validated_data.get('assigned_to'):
            raise serializers.ValidationError('Bajaruvchi kiritilmagan')
        if not self.context.get('request').user.username:
            raise serializers.ValidationError('Topshiriq beruvchi kiritilmagan')
        user = self.request.user
        print('---------------')
        print(self)
        user = self.context.get('request').user
        task = Task.objects.create(assigned_by=user,**validated_data)
        images = self.context.get('images')
        # audios = self.getlist('audios')
        # if images:
            # images = decrease(images)
        for i in images:
            print('rasmlar otdi :)')   
            print(i)
            # if i[-3:] in ('PNG', 'png', 'JPEG', 'jpg', 'jpeg', 'Jpeg', 'Png', 'JPG'):
            #     raise serializers.ValidationError('Rasm yuklashda xatolik. Faqat PNG va Jpeg rasmlar yuklang') 
            TaskContent.objects.create(task = task, content_type='image', image=i)
        audios = self.context.get('audios')
        for i in audios:    
            # if i[-3:] in ('mp3', 'mp4', 'doc'):
            #     raise serializers.ValidationError('Audio yuklashda xatolik.') 
            TaskContent.objects.create(task = task, content_type='audio', audio=i)
        texts = self.context.get('texts')
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


class TaskMessagesListSerializer(serializers.ModelSerializer):
    ism = serializers.CharField(source='sender.first_name')
    familiya = serializers.CharField(source='sender.last_name')
    photo = serializers.ImageField(source='sender.photo.url')
    class Meta:
        model = Message
        fields = ['id', 'task', 'sender', 'ism', 'familiya', 'photo','image', 'audio', 'text', 'created_at', 'is_read']


class TaskMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['task', 'sender']
        extra_kwargs = {
            'sender': {'read_only': True},
           
        }
    def create(self, validated_data):
        user = self.context.get('request').user
        images = self.context.get('images')
        audios = self.context.get('audios')
        texts = self.context.get('texts')
        a = None        
        if images:
            for i in images:
                a = Message.objects.create(
                    task=validated_data.get('task'),
                    sender=user,
                    image = i
                    )
        if audios:
            for i in audios:
                a = Message.objects.create(
                    task=validated_data.get('task'),
                    sender=user,
                    audio = i
                    )
        if texts:
            for i in texts:
                a = Message.objects.create(
                    task=validated_data.get('task'),
                    sender=user,
                    text = i
                    )
        return a




# LIST
    
    # Task

class TaskListContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskContent
        fields = ['text', 'image', 'audio',]

class TaskListSerializer(serializers.ModelSerializer):
    # contents = TaskContentSerializer(many=True, read_only=True)
    assigned_by = serializers.CharField(source='assigned_by.username', read_only=True)
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_by_id = serializers.CharField(source='assigned_by.id', read_only=True)
    assigned_to_id = serializers.CharField(source='assigned_to.id', read_only=True)
    sector = serializers.CharField(source='assigned_to.sector.name', read_only=True)
    photo = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    number_unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'assigned_to_id', 'assigned_to', 'photo', 'assigned_by_id','assigned_by', 'reason', 'event', 'deadline', 
            'status', 'privacy', 'created_at', 'updated_at', 'financial_help', 
            'is_active', 'is_changed', 'problem', 'all_days', 'remain_days',
            'sector', 'text', 'image', 'audio', 'number_unread_messages'
        ]
    def get_photo(self, obj):
        # Assuming 'sender' is a generic relation to Director, Manager, Xodim
        # if hasattr(obj.assigned_to, 'manager_profile'):  # Assuming 'user' is the related_name in Director, Manager, Xodim
        #     return obj.assigned_to.manager_profile.photo.url if obj.assigned_to.manager_profile.photo else None
        # elif hasattr(obj.assigned_to, 'xodim_profile'):  # Assuming 'user' is the related_name in Director, Manager, Xodim
        #     return obj.assigned_to.xodim_profile.photo.url if obj.assigned_to.xodim_profile.photo else None
        # elif hasattr(obj.assigned_to, 'director_profile'):  # Assuming 'user' is the related_name in Director, Manager, Xodim
        #     return obj.assigned_to.director_profile.photo.url if obj.assigned_to.director_profile.photo else None
        # elif hasattr(obj.assigned_to, 'admin_profile'):  # Assuming 'user' is the related_name in Director, Manager, Xodim
        #     return obj.assigned_to.admin_profile.photo.url if obj.assigned_to.admin_profile.photo else None
        # else:
        #     return obj.assigned_to.boshqalar_profile.photo.url if obj.assigned_to.boshqalar_profile.photo else None
        if obj.assigned_to.photo:
            return obj.assigned_to.photo.url
        return None
    def get_audio(self, obj):
        audio = []
        if obj.contents.filter(content_type='audio').exists():
            for i in obj.contents.filter(content_type='audio'):
                audio.append(i.audio.url)
        return audio
    def get_image(self, obj):
        image = []
        if obj.contents.filter(content_type='image').exists():
            for i in obj.contents.filter(content_type='image'):
                image.append(i.image.url)
        return image
    def get_text(self, obj):
        text = []
        if obj.contents.filter(content_type='text').exists():
            for i in obj.contents.filter(content_type='text'):
                text.append(i.text)
        return text 
    
    def get_number_unread_messages(self, obj):
        return Message.objects.filter(task=obj, is_read=False).count()