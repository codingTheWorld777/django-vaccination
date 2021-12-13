from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ModelStock
import re

# Create your views here.]


def stockReadDosesByVaccinByCenter(request):
    results = ModelStock.getDosesByVaccinByCenter()
    return render(request, "stock/viewDoseByVaccinByCenter.html", context={'results': results, 'stockAdded': None})


def stockReadDosesByCenter(request):
    info_dict = ModelStock.getCenterAndDose()
    return render(request, "stock/viewCentreDose.html", context=info_dict)


def stockAdd(request):
    if request.method == 'GET':
        path_info = request.META['PATH_INFO']
        query_str = re.search(r'target\=[a-zA-Z0-9]*', path_info).group()
        target_value = re.split(r'target\=|\&', query_str)[1]
        target = f'stock:{target_value}'

        results = ModelStock.attributeVaccin()
        stock_dict = {'results': results, 'target': target}

        return render(request, "stock/viewStockAdd.html", context=stock_dict)


def stockAdded(request):
    if request.method == 'GET':
        centre_label = re.split(":", request.GET['centre_label'])[0].strip()
        centre_adresse = re.split(":", request.GET['centre_label'])[1].strip()
        vaccin_label = request.GET['vaccin_label']
        vaccin_add = request.GET['vaccin_add']

        stockAdded = ModelStock.addVaccin(
            centre_label, centre_adresse, vaccin_label, vaccin_add)
        results = ModelStock.getDosesByVaccinByCenter()

        return render(request, "stock/viewDoseByVaccinByCenter.html", context={'results': results, 'stockAdded': stockAdded})


# Delete stock
def stockDeleted(request):
    if request.method == 'GET':
        centre_label = re.split(":", request.GET['centre_label'])[0].strip()
        centre_adresse = re.split(":", request.GET['centre_label'])[1].strip()
        vaccin_label = request.GET['vaccin_label']
        centre_id = ModelStock.getCentreId(centre_label, centre_adresse)
        vaccin_id = ModelStock.getVaccinId(vaccin_label)

        print("INFO", centre_id, vaccin_id)

        delete_operation = ModelStock.deleteStock(centre_id, vaccin_id)
        results = ModelStock.getDosesByVaccinByCenter()
        results_dict = {'results': results, 'vaccin_label': vaccin_label, 'centre_label': centre_label,
                        'centre_adresse': centre_adresse, "delete_operation": delete_operation}

        return render(request, "stock/viewStockDeleted.html", context=results_dict)
