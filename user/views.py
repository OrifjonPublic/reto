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