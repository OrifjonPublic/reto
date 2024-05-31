from django.urls import path

from user import views


urlpatterns = [

    # lavozim
    path('create/rank/', views.PositionCreateView.as_view()),
    path('edit/rank/<int:id>/', views.PositionEditView.as_view()),
    
    # bolim
    path('create/sector/', views.SectorCreateView.as_view()),
    path('edit/sector/<int:id>/', views.SectorEditView.as_view()),    

]