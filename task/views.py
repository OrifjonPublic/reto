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
from .change_task import change_user_sector


# class TaskChangeByUser(APIView):
#     """
#     :parametr -> ids : [1,2,4] , id lar listi
#     """
#     def post(self, request):
#         ids = request.data.getlist('id')
#         news_sector = request.data.get('new_sector')
#         news_sector_obj=None
#         if news_sector:
#             news_sector_obj = Sector.objects.get(id=news_sector)



class TaskArchiveListView(APIView):
    """
    :parametr -> ids : [1,2,4] , id lar listi
    """
    def get(self,request):
        queryset = Task.objects.filter(is_active=False)
        serializer_class = TaskListSerializer(queryset, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)
    def post(self, request):
        ids = request.data.get('ids')
        if ids:
            t = Task.objects.get(id=ids[0])
            if t.is_active:
                t.is_active=False 
            else:
                t.is_active = True
            t.save()
            return Response({
                'message': 'Arxivlandi'
            })
        return Response({
            'message': 'Hech qanday id lar kelmadi'
        })


class TaskFinishView(APIView):
    """
    status: finished (canceled)
    """
    def post(self, request, id):
        try:
            queryset = Task.objects.get(id=id)
        except Task.DoesNotExist as e:
            raise APIException(e)
        status = request.data.get('status')
        if status:
            queryset.status = status 
            queryset.save()
        serializer = TaskListSerializer(queryset)
        return Response(data=serializer.data)
        

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
        images = request.data.getlist('images')
        texts = request.data.getlist('texts')
        audios = request.data.getlist('audios')
        serializer_class = TaskSerializer(data=request.data, context = {'request': request, 'images':images, 'audios':audios, 'texts':texts})
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


class TaskMessageGetView(APIView):
    def get(self, request, id):
        queryset = Message.objects.filter(task__id=id).exclude(sender=request.user)
        # making is_read field to True each False   
        queryset.update(is_read=True)
        queryset = Message.objects.filter(task__id=id)
        serializer_class = TaskMessagesListSerializer(queryset, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)


class CreateTaskMessagesView(ListCreateAPIView):
    serializer_class = TaskMessagesSerializer
    parser_classes = [MultiPartParser, FileUploadParser, JSONParser]

    def get(self, request):
        queries = Message.objects.all()
        serializer_class = TaskMessagesSerializer(queries, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        images = request.data.getlist('images')
        audios = request.data.getlist('audios')
        texts = request.data.getlist('texts')
        serializer = TaskMessagesSerializer(data=request.data, context = {'request': request, 'images': images, 'audios': audios, 'texts': texts})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditTaskMessageView(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = TaskMessagesSerializer
    lookup_field = 'id'