from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

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
        fields = ('id', 'username', 'rank', 'sector', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("This username is already in use."))
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

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
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
        profile = Profile.objects.get(user=user)
        if validated_data.get('first_name'):
            user.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            user.first_name = validated_data.get('last_name')
        if validated_data.get('shior'):
            profile.first_name = validated_data.get('shior')
        if validated_data.get('main_task'):
            profile.main_task = validated_data.get('main_task')
        if validated_data.get('birth_date'):
            profile.birth_date = validated_data.get('birth_date')
        if validated_data.get('photo'):
            profile.photo = validated_data.get('photo')
        user.save()
        profile.save()
        return user
    
    def update(self, instance, validated_data):
        user = self.context.get('request').user
        profile = Profile.objects.get(user=user)

        if validated_data.get('first_name'):
            user.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            user.last_name = validated_data.get('last_name')
        if validated_data.get('first_name'):
            user.first_name = validated_data.get('first_name')
        if validated_data.get('shior'):
            profile.first_name = validated_data.get('shior')
        if validated_data.get('main_task'):
            profile.main_task = validated_data.get('main_task')
        if validated_data.get('birth_date'):
            profile.birth_date = validated_data.get('birth_date')
        if validated_data.get('photo'):
            profile.photo = validated_data.get('photo')
        
        user.save()
        profile.save()
        
        return user

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = attrs.get('request').user
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
            member = User.objects.filter(user__iexact=user).last()
            if member.exists() and attrs.get('password'):
                member.set_password(attrs.get('password'))
                member.save()
            else:
                return serializers.ValidationError(_('username topilmadi yoki yangi parol kiritilmadi :)'))
        return attrs
