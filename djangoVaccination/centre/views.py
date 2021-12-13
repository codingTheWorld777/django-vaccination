from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import ModelCentre
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

# All vaccination's center
def centreReadAll(request):
    centre_info = ModelCentre.getAll()
    centre_dict = {'centre_info': centre_info}

    return render(request, 'centre/viewAll.html', context=centre_dict)


# Name of vaccination's center
def centreReadLabel(request):
    if request.method == 'GET':
        path_info = request.META['PATH_INFO']
        query_str = re.search(r'target\=[a-zA-Z0-9]*', path_info).group()
        target_value = re.split(r'target\=|\&', query_str)[1]
        target = f'centre:{target_value}'

        centre_info = ModelCentre.objects.all()
        centre_dict = {'centre_info': centre_info, 'target': target}

        return render(request, 'centre/viewLabel.html', context=centre_dict)


# Get 1 center
def centreReadOne(request):
   if request.method == 'GET':
        centre_id = re.split(r":", request.GET['label'])[0].strip()
        centre_label = re.split(r":", request.GET['label'])[1].strip()
        centre_adresse = re.split(r":", request.GET['label'])[2].strip()
        centre_info = ModelCentre.getOne(centre_id)
        centre_dict = {'centre_info': centre_info}

        return render(request, 'centre/viewAll.html', context=centre_dict)

# Vaccination's center creation page
def centreCreate(request):
    return render(request, "centre/viewInsert.html", context={})

# Page of vaccination's center after adding a new center
@csrf_exempt
def centreCreated(request):
    if request.method == "POST":
        label = request.POST['label'].strip()
        adresse = request.POST['adresse'].strip()

        condition1 = (not label) or (not adresse)
        condition2 = (len(label) > 0) and (len(adresse) > 0)

        if (condition1):
            info_dict = {'result': False}
        elif (condition2):
            try:
                # Add new center to database (table 'centre')
                id = ModelCentre.insert(strip_tags(label), strip_tags(adresse))
                centre_info = ModelCentre.getAll()

                info_dict = {'result': True, 'id': id, 'label': label,
                            'adresse': adresse, 'centre_info': centre_info}
            except Exception:
                info_dict = {'result': False}

        return render(request, "centre/viewInserted.html", context=info_dict)

    
# Delete a center from its label
def centreDeleted(request):
    if request.method == 'GET':
        centre_id = re.split(r":", request.GET['label'])[0].strip()
        centre_label = re.split(r":", request.GET['label'])[1].strip()
        centre_adresse = re.split(r":", request.GET['label'])[2].strip()

        # Delete command
        ModelCentre.deleteId(centre_id)

        centre_info = ModelCentre.getAll()
        centre_dict = {'centre_info': centre_info, 'id': centre_id, 'label': centre_label, 'adresse': centre_adresse}

        return render(request, 'centre/viewDeleted.html', context=centre_dict)