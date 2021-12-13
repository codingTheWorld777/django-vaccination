from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ModelPatient
import re

# Create your views here.
def strip_tags(value):
    """Return the given HTML with all tags stripped."""
    # Note: in typical case this loop executes _strip_once once. Loop condition
    # is redundant, but helps to reduce number of executions of _strip_once.
    value = str(value)
    while '<' in value and '>' in value:
        new_value = _strip_once(value)
        if value.count('<') == new_value.count('<'):
            # _strip_once wasn't able to detect more tags.
            break
        value = new_value
    return value


# Show list of patients
def patientReadAll(request):
    patient_info = ModelPatient.getAll()
    patient_dict = {'patient_info': patient_info}

    return render(request, "patient/viewAll.html", context=patient_dict)


def patientReadId(request):
    if request.method == 'GET':
        path_info = request.META['PATH_INFO']
        query_str = re.search(r'target\=[a-zA-Z0-9]*', path_info).group()
        target_value = re.split(r'target\=|\&', query_str)[1]
        target = f'patient:{target_value}'

        patient_info = ModelPatient.getAll()
        patient_dict = {'patient_info': patient_info, 'target': target}

        return render(request, 'patient/viewId.html', context=patient_dict)
    patient_dict = {}
    return render(request, "patient/viewId.html", context=patient_dict)


def patientReadOne(request):
    if request.method == 'GET':
        patient_id = re.split(r":", request.GET['patientInfo'])[0].strip()
        patient_info = ModelPatient.getOne(patient_id)
        patient_dict = {'patient_info': patient_info}
        return render(request, "patient/viewAll.html", context=patient_dict)


# Page of patient's creation
def patientCreate(request):
    return render(request, "patient/viewInsert.html", context={})

# Page after creating a new patient
@csrf_exempt
def patientCreated(request):
    if request.method == 'POST':
        nom = request.POST['nom'].strip()
        prenom = request.POST['prenom'].strip()
        adresse = request.POST['adresse'].strip()

        condition1 = (not nom) or (not prenom) or (not adresse)
        condition2 = (len(nom) > 0) and (len(prenom) > 0) and (len(adresse) > 0)

        if (condition1):
            info_dict = {'result': False}
        elif (condition2):
            try:
                # Add new vaccine to database (table 'vaccin')
                id = ModelPatient.insert(strip_tags(nom), strip_tags(prenom), strip_tags(adresse))
                patient_info = ModelPatient.getAll()

                info_dict = {'result': True, 'id': id, 'nom': nom,
                            'prenom': prenom, 'adresse': adresse, 'patient_info': patient_info}
            except Exception:
                info_dict = {'result': False}

        return render(request, 'patient/viewInserted.html', context=info_dict)


def patientReadDistinct(request):
    adresse_info = ModelPatient.patientReadDistinct()
    return render(request, "patient/viewDistinct.html", context={'adresse_info': adresse_info, 'quantity': None})

def quantityByAdresse(request):
    info_dict = ModelPatient.getPatientQuantityByAddress()
    return render(request, "patient/viewDistinct.html", context=info_dict)

# Delete a patient
def patientDeleted(request):
    if request.method == 'GET':
        patient_id = re.split(r":", request.GET['patientInfo'])[0].strip()
        patient_nom = re.split(r":", request.GET['patientInfo'])[1].strip()
        patient_adresse = re.split(r":", request.GET['patientInfo'])[2].strip()
        # Delete a patient in the tables 'patient' and 'rendezvous'
        ModelPatient.deleteId(patient_id)

        patient_info = ModelPatient.getAll()
        patient_dict = {'patient_info': patient_info, 'id': patient_id, 'nom': patient_nom, 'adresse': patient_adresse}

        return render(request, "patient/viewDeleted.html", context=patient_dict)
