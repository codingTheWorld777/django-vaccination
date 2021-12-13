from django.urls import path
from stock import views

app_name = 'stock'
urlpatterns = [
    path(r'?action=stockReadDosesByVaccinByCenter', views.stockReadDosesByVaccinByCenter, name='stockReadDosesByVaccinByCenter'),
    path(r'?action=stockReadDosesByCenter', views.stockReadDosesByCenter, name='stockReadDosesByCenter'),
    path(r'?action=stockAdd&target=stockAdded', views.stockAdd, name='stockAdd'),
    path(r'?action=stockAdded', views.stockAdded, name='stockAdded'),
    path(r'?action=stockAdd&target=stockDeleted', views.stockAdd, name='stockDelete'),
    path(r'?action=stockDeleted', views.stockDeleted, name='stockDeleted'),
]
