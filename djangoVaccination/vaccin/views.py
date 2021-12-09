from django.shortcuts import render
from .models import ModelVaccin

# Create your views here.
def viewAll(request):
    vaccin_info = ModelVaccin.objects.all()
    vaccin_dict = {'vaccin_info': vaccin_info}
    
    return render(request, 'vaccin/viewAll.html', context=vaccin_dict)
