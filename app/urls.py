from django.urls import path
from . import views
from project import settings
from django.conf.urls.static import static

urlpatterns = [
    #main
    path('', views.main, name = 'main'),
    #for patients
    path('reception/', views.reception, name = 'reception'),
    path('reception/<int:id>/datetime/', views.appointment_datetime, name = 'datetime'),
    path('personal_cabinet/', views.personal_cabinet, name = 'personal_cabinet'),
    path('personal_cabinet/appointment/<int:pk>/', views.last_appointment, name = 'last_appointment'),
]