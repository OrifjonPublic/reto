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
    
]