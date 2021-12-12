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