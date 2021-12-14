from django.urls import path
from rdv import views

app_name = 'rdv'
urlpatterns = [
    path(r'?action=rdvReadPatient&target=rdvPropos', views.rdvReadPatient, name='rdvReadPatient'),
    path(r'?action=rdvPropos', views.rdvPropos, name='rdvPropos'),
    path(r'?action=rdvReadAll', views.rdvReadAll, name='rdvReadAll'),
]
