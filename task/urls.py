from django.urls import path

from . import views

urlpatterns = [
    
    # create task
    path('create/', views.CreateTaskView.as_view()),
    
    # edit task
    path('edit/<int:id>/', views.EditTaskView.as_view()),
    
    # create task content
    path('content/create/', views.CreateTaskContentView.as_view()),
    
    # edit task content
    path('content/edit/<int:id>/', views.EditTaskContentView.as_view()),
    
    # create task message
    path('message/create/', views.CreateTaskMessagesView.as_view()),
    
    # edit task message
    path('message/edit/<int:id>/', views.EditTaskMessageView.as_view()),
    path('message/get/<int:id>/', views.TaskMessageGetView.as_view()),

    # task finish
    path('finish/<int:id>/', views.TaskFinishView.as_view()),

    # task arxivlash
    path('arxivlash/', views.TaskArchiveListView.as_view()),
    path('arxivlash/xodim/<int:id>/', views.TaskXodimArxivListView.as_view()),
]

