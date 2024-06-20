from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from django.conf import settings
from task.serializers import TaskListSerializer
from task.models import Task
from task.statistika import (all_stats_main, all_sector, 
                        one_sector_stat, one_employee_stat, 
                        one_sector_employees, all_employees_stat_)
from user.serializers import CompanySerializer
from user.models import Company


class LogoView(APIView):
    def get(self, request):
        logos = Company.objects.all()
        ser = CompanySerializer(logos, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MainStatView(APIView):
    def get(self, request):
        queryset = all_stats_main()
        return Response(data=queryset, status=status.HTTP_200_OK)

class AllSectorStatView(APIView):
    def get(self, request):
        queryset = all_sector()
        return Response(data=queryset, status=status.HTTP_200_OK)

class AllEmployeesStatView(APIView):
    def get(self, request):
        queryset = all_employees_stat_()
        return Response(data=queryset, status=status.HTTP_200_OK)


class OneSectorStatView(APIView):
    def get(self, request, id):
        queryset = one_sector_stat(id)
        return Response(data=queryset, status=status.HTTP_200_OK)

class OneSectorEmployeeStatView(APIView):
    def get(self, request, id):
        queryset = one_sector_employees(id)
        return Response(data=queryset, status=status.HTTP_200_OK)


class OneEmployeeStatView(APIView):
    def get(self, request, id):
        queryset = one_employee_stat(id)
        return Response(data=queryset, status=status.HTTP_200_OK)


# LIST views
class TaskListView(ListAPIView):
    queryset = Task.objects.filter(is_active=True).exclude(Q(assigned_by__rank__name=settings.MANAGER) | Q(assigned_by__isnull=True))
    serializer_class = TaskListSerializer


class TaskDirectorListView(ListAPIView):
    queryset = Task.objects.filter(is_active=True).filter(Q(assigned_by__rank__name=settings.BOSS) | Q(assigned_by__isnull=True))
    serializer_class = TaskListSerializer


class TasksByManagerListView(APIView):
    def get(self, request):
        queryset = Task.objects.filter(is_active=True).filter(assigned_by=request.user).filter(assigned_by__rank__name=settings.MANAGER)
        serializer_class = TaskListSerializer(queryset, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)


class TasksOneSectorView(APIView):
    def get(self, request, id):
        queryset = Task.objects.filter(is_active=True).filter(assigned_to__sector__id=id)
        serializer_class = TaskListSerializer(queryset, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)

class TasksOneXodimByBossView(APIView):
    def get(self, request, id):
        queryset = Task.objects.filter(is_active=True).filter(assigned_to__id=id).exclude(assigned_by__rank__name=settings.MANAGER)
        serializer_class = TaskListSerializer(queryset, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)


class TasksOneXodimByMAnagerView(APIView):
    def get(self, request, id):
        queryset = Task.objects.filter(is_active=True).filter(assigned_to__id=id).filter(assigned_by__rank__name=settings.MANAGER)
        serializer_class = TaskListSerializer(queryset, many=True)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)
