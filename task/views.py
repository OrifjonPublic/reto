from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from .serializers import *


class CreateTaskView(APIView):
    serializer_class = TaskSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request):
        queryset = Task.objects.all()
        serializer_class = TaskSerializer(queryset, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new task",
        request_body=TaskSerializer,
        responses={201: TaskSerializer, 400: "Bad Request"}
    )
    def post(self,request):
        serializer_class = TaskSerializer(data=request.data, context = {'request': request})
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(data=serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)



class EditTaskView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'
    

class CreateTaskContentView(ListCreateAPIView):
    queryset = TaskContent.objects.all()
    serializer_class = TaskContentSerializer
    parser_classes = [MultiPartParser, FileUploadParser, JSONParser]    

class EditTaskContentView(RetrieveUpdateDestroyAPIView):
    queryset = TaskContent.objects.all()
    serializer_class = TaskContentSerializer
    lookup_field = 'id'


class CreateTaskMessagesView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = TaskMessagesSerializer
    parser_classes = [MultiPartParser, FileUploadParser, JSONParser]
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        serializer = TaskMessagesSerializer(context={'request': self.request})
        return super().get_serializer(*args, **kwargs)


class EditTaskMessageView(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = TaskMessagesSerializer
    lookup_field = 'id'