from django.urls import path

from user import views
from .views import (MainStatView, AllSectorStatView, 
                    OneSectorStatView, OneEmployeeStatView,
                    TaskListView, TaskDirectorListView,
                    TasksOneSectorView, TasksOneXodimByBossView, TasksOneXodimByMAnagerView)


urlpatterns = [

    # lavozim
    path('create/rank/', views.PositionCreateView.as_view()),
    path('edit/rank/<int:id>/', views.PositionEditView.as_view()),
    
    # bolim
    path('create/sector/', views.SectorCreateView.as_view()),
    path('edit/sector/<int:id>/', views.SectorEditView.as_view()),    

    # Asosiy STAT
    path('stat/main/', MainStatView.as_view()),
    
    # all Sector stat
    path('stats/sectors/', AllSectorStatView.as_view()),
    path('stat/sector/one/<int:id>/', OneSectorStatView.as_view()),
    path('stat/one/xodim/<int:id>/', OneEmployeeStatView.as_view()),

    # Task list
    path('tasks/all/list/', TaskListView.as_view()),
    path('tasks/director/', TaskDirectorListView.as_view()),
    path('tasks/one/sector/<int:id>/', TasksOneSectorView.as_view()),
    path('tasks/one/xodim/bydirector/<int:id>/', TasksOneXodimByBossView.as_view()),
    path('tasks/one/xodim/bymanager/<int:id>/', TasksOneXodimByMAnagerView.as_view()),

]

