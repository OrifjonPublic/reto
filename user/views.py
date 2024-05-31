from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone

from django.db.models import Q
from user.models import *
from user.serializers import *


class UserCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserEditView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class UserOwnEditView(APIView):
    serializer_class = UserProfileSerializer
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'your profile data hava been changed!'}, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors)    


class UserPasswordView(APIView):
    serializer_class = PasswordSerializer

    def post(self, request):
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(data={
                'message': 'Your password has been successfully changed! :)'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_304_NOT_MODIFIED)


class AdminPasswordView(APIView):
    serializer_class = AdminPasswordSerializer

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