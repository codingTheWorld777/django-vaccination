from django.urls import path
from vaccin import views

app_name = 'vaccin'
urlpatterns = [
    path(r'', views.viewAll, name='viewAll'),
]
