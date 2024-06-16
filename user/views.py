from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Q
from user.models import *
from user.serializers import *


class XodimListView(APIView):
    def get(self,request):
        queryset = User.objects.all()
        serializer_class = UserListSerializer(queryset, many=True)
        return Response(data=serializer_class.data)


class ManagerListView(APIView):
    def get(self,request):
        queryset = User.objects.filter(rank__name=settings.MANAGER)
        serializer_class = UserListSerializer(queryset, many=True)
        return Response(data=serializer_class.data)


class XodimView(APIView):
    def get(self,request):
        queryset = User.objects.filter(rank__name=settings.EMPLOYEE)
        serializer_class = UserListSerializer(queryset, many=True)
        return Response(data=serializer_class.data)


class UserCreateView(APIView):
    def get(self,request):
        queryset = User.objects.all()
        serializer_class = UserSerializer(queryset, many=True)
        return Response(serializer_class.data)
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.errors)

class UserEditView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class UserOwnEditView(APIView):
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
    operation_description="change password ...",
    request_body=UserProfileSerializer,
    responses={201: UserProfileSerializer, 400: "Bad Request"}
    )
    def get(self, request):
        # user = User.objects.filter(id=request.user.id)
        user = request.user
        if user.rank.name == settings.EMPLOYEE:
            x = Xodim.objects.get(user=user)
        elif user.rank.name == settings.MANAGER:
            x = Manager.objects.get(user=user)
        elif user.rank.name == settings.BOSS:
            x = Direktor.objects.get(user=user)
        elif user.rank.name == settings.ASSIST:
            x = Admin.objects.get(user=user)
        else:
            x = Boshqalar.objects.get(user=user)
        d = {
            'first_name': x.user.first_name,
            'last_name': x.user.last_name,
            'photo': x.user.photo.url,
            'username': x.user.username,
            'rank': x.user.rank.name,
            'id': x.user.id,
            'shior': x.shior,
            'main_task': x.main_task,
            'birth_date': x.birth_date,
            'phone_number': x.phone_number,
        }
        return Response(data=d)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'your profile data hava been changed!'}, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors)    


class UserPasswordView(APIView):
    serializer_class = PasswordSerializer

    @swagger_auto_schema(
    operation_description="change password ...",
    request_body=PasswordSerializer,
    responses={201: PasswordSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        print(request.user)
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(data={
                'message': 'Your password has been successfully changed! :)'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


class AdminPasswordView(APIView):
    serializer_class = AdminPasswordSerializer

    @swagger_auto_schema(
    operation_description="change password ...",
    request_body=AdminPasswordSerializer,
    responses={201: AdminPasswordSerializer, 400: "Bad Request"}
    )
    def post(self,request):
        serializer = AdminPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response(data={'message': "Your forgotten has been password changed"})
        return Response(data={'message': 'Your data is not valid'})


class PositionCreateView(ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionEditView(RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    lookup_field = 'id'


class SectorCreateView(ListCreateAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class SectorEditView(RetrieveUpdateDestroyAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    lookup_field = 'id'