from django.urls import path

from . import views 

urlpatterns = [
    # admin urls
    path('register/', views.UserCreateView.as_view()),
    path('register/admin/edit/<int:id>/', views.UserEditView.as_view()),
    
    # user edit
    path('edit/', views.UserOwnEditView.as_view()),
    
    # user password changes
    path('password/change/', views.UserPasswordView.as_view()),
    
    # user password change by admin
    path('password/change/by/admin/', views.AdminPasswordView.as_view()),
    
    # barcha ishchilar ro'yxati
    path('all/employees/', views.XodimListView.as_view()),
    
    # barcha manager
    path('all/managers/', views.ManagerListView.as_view()),

    # barcha xodimlar
    path('all/xodimlar/', views.XodimView.as_view()),

    path('create/notes/', views.UserNotesView.as_view()),
    path('get/one/note/<int:id>/', views.OneNoteView.as_view()),
]
