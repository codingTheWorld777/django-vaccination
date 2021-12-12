from django.urls import path
from centre import views

app_name = 'centre'
urlpatterns = [
    path(r'', views.centreReadAll, name='centreReadAll'),
]
