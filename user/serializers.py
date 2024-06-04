from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import *


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name')


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'rank', 'sector', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("This username is already in use."))
        return value
    def validate_rank(self, value):
        if not Position.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(_("this Rank is not registered yet."))
        return value
    def validate_sector(self, value):
        if not Sector.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(_("This bolim is not registered yet."))
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            rank=validated_data.get('rank', None),
            sector=validated_data.get('sector', None),
        )        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.sector = validated_data.get('sector', instance.sector)

        # if 'password' in validated_data:
        #     instance.set_password(validated_data['password'])
        instance.save()
        return instance



class MyOwnSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token =  super().get_token(user)

        token['username'] = user.username
        token['rank'] = user.rank.name
        token['id'] = user.id
        if user.sector:
            token['sector'] = user.sector.id
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['rank'] = self.user.rank.name
        if self.user.sector:
            data['sector'] = self.user.sector.id
        return data


class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    shior = serializers.CharField(required=False)
    main_task = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    photo = serializers.ImageField(required=False)

    def create(self, validated_data):
        user = self.context.get('request').user
        if user.rank == settings.EMPLOYEE:
            profile = Xodim.objects.get_or_create(user=user)[0]
        elif user.rank == settings.MANAGER:
            profile = Manager.objects.get_or_create(user=user)[0]
        elif user.rank == settings.BOSS:
            profile = Direktor.objects.get_or_create(user=user)[0]
        elif user.rank == settings.ASSIST:
            profile = Admin.objects.get_or_create(user=user)[0]
        else:
            profile = Boshqalar.objects.get_or_create(user=user)[0]
        if validated_data.get('first_name'):
            user.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            user.last_name = validated_data.get('last_name')
        if validated_data.get('shior'):
            profile.shior = validated_data.get('shior')
        if validated_data.get('main_task'):
            profile.main_task = validated_data.get('main_task')
        if validated_data.get('birth_date'):
            profile.birth_date = validated_data.get('birth_date')
        if validated_data.get('photo') and validated_data.get('photo').endswith(('PNG', 'png', 'JPEG', 'jpg')):
            profile.photo = validated_data.get('photo')
        user.save()
        profile.save()
        return user
    
    def update(self, instance, validated_data):
        user = self.context.get('request').user
        if user.rank == settings.EMPLOYEE:
            profile = Xodim.objects.get_or_create(user=user)[0]
        elif user.rank == settings.MANAGER:
            profile = Manager.objects.get_or_create(user=user)[0]
        elif user.rank == settings.BOSS:
            profile = Direktor.objects.get_or_create(user=user)[0]
        elif user.rank == settings.ASSIST:
            profile = Admin.objects.get_or_create(user=user)[0]
        else:
            profile = Boshqalar.objects.get_or_create(user=user)[0]

        if validated_data.get('first_name'):
            user.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            user.last_name = validated_data.get('last_name')
        # if validated_data.get('first_name'):
        #     user.first_name = validated_data.get('first_name')
        if validated_data.get('shior'):
            profile.shior = validated_data.get('shior')
        if validated_data.get('main_task'):
            profile.main_task = validated_data.get('main_task')
        if validated_data.get('birth_date'):
            profile.birth_date = validated_data.get('birth_date')
        if validated_data.get('photo') and validated_data.get('photo').endswith(('PNG', 'png', 'JPEG', 'jpg')):
            profile.photo = validated_data.get('photo')
        
        user.save()
        profile.save()
        
        return user

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context.get('request').user
        password = attrs.get('old_password')
        if not user.check_password(password):
            raise serializers.ValidationError('old_password do not match')
        user.set_password(attrs.get('new_password'))
        user.save()
        return attrs
    

class AdminPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = attrs.get('username')
        if user:
            member = User.objects.filter(username__iexact=user)
            if member.exists() and attrs.get('password'):
                member = member.last()
                member.set_password(attrs.get('password'))
                member.save()
            else:
                return serializers.ValidationError(_('username topilmadi yoki yangi parol kiritilmadi :)'))
        return attrs
