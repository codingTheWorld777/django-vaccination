from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import ModelVaccin
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

# All vaccines's infos
def vaccinReadAll(request):
    vaccin_info = ModelVaccin.objects.all()
    vaccin_dict = {'vaccin_info': vaccin_info}

    return render(request, 'vaccin/viewAll.html', context=vaccin_dict)

# Selection of 1 type of vaccine
def vaccinReadLabel(request):
    if request.method == 'GET':
        path_info = request.META['PATH_INFO']
        query_str = re.search(r'target\=[a-zA-Z0-9]*', path_info).group()
        target_value = re.split(r'target\=|\&', query_str)[1]
        target = f'vaccin:{target_value}'

        vaccin_info = ModelVaccin.objects.all()
        vaccin_dict = {'vaccin_info': vaccin_info, 'target': target}

        return render(request, 'vaccin/viewLabel.html', context=vaccin_dict)

# Show one vaccine's info from selection view
def vaccinReadOne(request):
    if request.method == 'GET':
        label = request.GET['label']
        vaccin_info = ModelVaccin.getOne(label)
        vaccin_dict = {'vaccin_info': vaccin_info}
        return render(request, 'vaccin/viewAll.html', context=vaccin_dict)

# Creation's vaccine interface
def vaccinCreate(request):
    return render(request, 'vaccin/viewInsert.html', context={})

# Create a new vaccine
@csrf_exempt
def vaccinCreated(request):
    if request.method == 'POST':
        label = request.POST['label'].strip()
        doses = request.POST['doses'].strip()

        condition1 = (not label) or (not doses)
        condition2 = (len(label) > 0) and (len(doses) > 0)

        if (condition1):
            info_dict = {'result': False}
        elif (condition2):
            # Add new vaccine to database (table 'vaccin')
            id = ModelVaccin.insert(strip_tags(label), strip_tags(doses))
            vaccin_info = ModelVaccin.objects.all()

            info_dict = {'result': True, 'id': id, 'label': label,
                         'doses': doses, 'vaccin_info': vaccin_info}

        return render(request, 'vaccin/viewInserted.html', context=info_dict)

# Delete a vaccine from its label
def vaccinDeleted(request):
    if request.method == 'GET':
        label = request.GET['label']
        vaccin_info = ModelVaccin.deleteLabel(label)
        vaccin_dict = {'vaccin_info': vaccin_info, 'label': label}

        return render(request, 'vaccin/viewDeleted.html', context=vaccin_dict)

# Modify the number of dose(s) page
def vaccinModifyDose(request):
    vaccin_info = ModelVaccin.getAll()

    return render(request, 'vaccin/viewModifyDose.html', context={'vaccin_info': vaccin_info})


# Update number of doses 
def vaccinUpdateDose(request):
    if (request.method == 'GET'):
        vaccin_label = request.GET['label']
        quantite = request.GET['quantite']

        ModelVaccin.updateDose(vaccin_label, quantite)
        vaccin_info = ModelVaccin.getAll()
        vaccin_dict = {'vaccin_info': vaccin_info, 'vaccin_label': vaccin_label}

        return render(request, 'vaccin/viewUpdateDose.html', context=vaccin_dict)

