from django.urls import path
from . import views
from project import settings
from django.conf.urls.static import static

urlpatterns = [
    #main
    path('', views.main, name = 'main'),
    #for patients
    path('reception/patient/', views.reception_patient, name = 'reception_patient'),
    path('reception/patient/<int:patient_pk>/doctor/', views.reception_doctor, name = 'reception_doctor'),
    path('reception/<int:pk>/datetime/', views.reception_datetime, name = 'reception_datetime'),
    path('reception/<int:pk>/info/', views.reception_info, name = 'reception_info'),
    path('personal_cabinet/', views.personal_cabinet, name = 'personal_cabinet'),
    path('personal_cabinet/appointment/<int:pk>/', views.last_appointment, name = 'last_appointment'),
]