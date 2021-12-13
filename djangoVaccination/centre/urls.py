from django.urls import path
from centre import views

app_name = 'centre'
urlpatterns = [
    path(r'', views.centreReadAll, name='centreReadAll'),
    path(r'?action=centreReadLabel&target=centreReadOne', views.centreReadLabel, name='centreReadLabel'),
    path(r'?action=centreReadOne', views.centreReadOne, name='centreReadOne'),
    path(r'?action=centreCreate', views.centreCreate, name='centreCreate'),
    path(r'?action=centreCreated', views.centreCreated, name='centreCreated'),
    path(r'?action=centreReadLabel&target=centreDeleted', views.centreReadLabel, name='centreDelete'),
    path(r'?action=centreDeleted', views.centreDeleted, name='centreDeleted'),
]
