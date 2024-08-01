from django.http import JsonResponse
from django.shortcuts import render

from medicine.models import MedicineUseInClinic, TakeMedicine


# Create your views here.


def autocomplete(request):
    query = request.GET.get('query', '')
    if query:
        medicines = MedicineUseInClinic.objects.filter(medicine_name__icontains=query)
        methods = TakeMedicine.objects.filter(Method_taken__icontains=query)

        medicine_results = [{'id': medicine.medicine_id, 'name': medicine.medicine_name} for medicine in medicines]
        method_results = [{'id': method.Take_id, 'method': method.Method_taken} for method in methods]

        results = {
            'medicines': medicine_results,
            'methods': method_results
        }
    else:
        results = {
            'medicines': [],
            'methods': []
        }
    return JsonResponse(results)
