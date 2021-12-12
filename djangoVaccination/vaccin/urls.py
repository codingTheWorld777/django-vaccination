from django.urls import path
from vaccin import views

app_name = 'vaccin'
urlpatterns = [
    path(r'', views.vaccinReadAll, name='vaccinReadAll'),
    path(r'?action=vaccinReadLabel&target=vaccinReadOne', views.vaccinReadLabel, name='vaccinReadLabel'),
    path(r'?action=vaccinReadOne', views.vaccinReadOne, name='vaccinReadOne'),
    path(r'?action=vaccinCreate', views.vaccinCreate, name='vaccinCreate'),
    path(r'?action=vaccinCreated', views.vaccinCreated, name='vaccinCreated'),
    path(r'?action=vaccinReadLabel&target=vaccinDeleted', views.vaccinReadLabel, name='vaccinDelete'),
    path(r'?action=vaccinDeleted', views.vaccinDeleted, name="vaccinDeleted"),
    path(r'?action=vaccinModifyDose', views.vaccinModifyDose, name="vaccinModifyDose"),
    path(r'?action=vaccinUpdateDose', views.vaccinUpdateDose, name="vaccinUpdateDose"),
]
