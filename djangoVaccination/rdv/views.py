from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import ModelRdv
import re

# Create your views here.

def rdvReadAll(request):
    results = ModelRdv.getAll()   
    return render(request, "rdv/viewAll.html", context={'results': results})

    
def rdvReadPatient(request):
    if request.method == 'GET':
        path_info = request.META['PATH_INFO']
        query_str = re.search(r'target\=[a-zA-Z0-9]*', path_info).group()
        target_value = re.split(r'target\=|\&', query_str)[1]
        target = f'rdv:{target_value}'

        results = ModelRdv.getPatient()
        return render(request, "rdv/viewPatient.html", context={'results': results, 'target': target})

# Voir le rendez-vous vacciné d'un patient
def rdvPropos(request):
    if request.method == 'GET':
        patientInfo = request.GET['patientInfo']
        patient_id = re.split(":", patientInfo)[0].strip()
        
        results = ModelRdv.getRdv(patient_id)                # il faut vérifier s'elle est nulle ou pas
        activeCenter = ModelRdv.getActiveDoseFromCenter()    # cela pour proposer ce qui n'a pas encore un rendez-vous
        
        numberOfDose = patient_injection = centerByVaccin = ''   # celles pour bien savoir si le patient doit vacciner encore une fois ou pas
        if len(results) > 0:
            numberOfDose =  ModelRdv.getDoseNumberOfVaccin(results[0][5]) 
            patient_injection = results[len(results) - 1][4]
            centerByVaccin = ModelRdv.getCenterByVaccin(results[0][5])

        info_dict = {"numberOfDose": numberOfDose, "patient_injection": patient_injection, "centerByVaccin": centerByVaccin,}
        print(info_dict, "INFO")
        return render(request, "rdv/viewRdvPropos.html", context=info_dict)


# Définir un rendez-vous pour le patient
def setRdv(request):
    if request.method == 'GET':
        patient_id = request.GET['patientId']
        centre_id = re.split(":", request.GET['centreInfo'])[0].strip()
        centre_label = re.split(":", request.GET['centreInfo'])[1].strip()
        centre_adresse = re.split(":", request.GET['centreInfo'])[2].strip()
        injection = int(ModelRdv.getInjection(patient_id)) + 1
        
        results = ModelRdv.setRdv(centre_id, centre_label, patient_id, injection)
        return render(request, "rdv/viewSetRdv.html", context={"results": results})
   