from django.urls import path
from patient import views

app_name = 'patient'
urlpatterns = [
    path(r'', views.patientReadAll, name='patientReadAll'),
    path(r'?action=patientReadId&target=patientReadOne', views.patientReadId, name='patientReadId'),
    path(r'?action=patientReadOne', views.patientReadOne, name='patientReadOne'),
    path(r'?action=patientCreate', views.patientCreate, name='patientCreate'),
    path(r'?action=patientCreated', views.patientCreated, name='patientCreated'),
    path(r'?action=patientReadDistinct', views.patientReadDistinct, name='patientReadDistinct'),
    path(r'?action=quantityByAdresse', views.quantityByAdresse, name='quantityByAdresse'),    
    path(r'?action=patientReadId&target=patientDeleted', views.patientReadId, name='patientDelete'),
    path(r'?action=patientDeleted', views.patientDeleted, name='patientDeleted'),
]
