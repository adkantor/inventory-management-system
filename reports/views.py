import datetime
import pytz

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings

from inventories.models import Transaction, MaterialGroup, Material
from reports.models import Resolution, generate_report

tz = pytz.timezone(settings.TIME_ZONE)

class TransactionsView(TemplateView):
    template_name='reports/transactions.html'

class SummaryView(TemplateView):
    template_name='reports/summary.html'


def get_material_groups(request):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 
    material_groups = MaterialGroup.serialize_all()
    return JsonResponse(material_groups, safe=False) 
    

def get_materials(request, material_group_id):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 
    # load material group filter
    if material_group_id == 'all':
        material_group = None
    else:
        try:
            material_group = MaterialGroup.objects.get(pk=material_group_id)
        except MaterialGroup.DoesNotExist:
            return JsonResponse({"error": "Material Group not found."}, status=404)
    
    materials = Material.serialize_all(material_group)
    return JsonResponse(materials, safe=False) 


def get_transactions(request):

    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    # check inputs
    data = request.GET
    # transaction type
    transaction_types = data.getlist('transaction_types')

    if transaction_types:
        if isinstance(transaction_types, list):
            if not set(transaction_types).issubset(set([Transaction.TYPE_IN, Transaction.TYPE_OUT, ''])):
                return JsonResponse({"error": "Transaction Type not found."}, status=404)
        elif transaction_types not in (Transaction.TYPE_IN, Transaction.TYPE_OUT):
            return JsonResponse({"error": "Transaction Type not found."}, status=404)
    # material group
    if data.get('material_group') is not None:
        try:
            material_group = MaterialGroup.objects.get(pk=data['material_group']) 
        except MaterialGroup.DoesNotExist:
            return JsonResponse({"error": "Material Group not found."}, status=404)
    else:
        material_group = None
    # material
    if data.get('material') is not None:
        try:
            material = Material.objects.get(pk=data['material']) 
        except Material.DoesNotExist:
            return JsonResponse({"error": "Material not found."}, status=404)
    else:
        material = None
    # start date
    if data.get('date_from') is not None:
        try:
            date_from = datetime.datetime.fromisoformat(data['date_from'])
            if date_from.tzinfo is None:
                date_from = tz.localize(date_from)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        date_from = None
    # end date
    if data.get('date_to') is not None:
        try:
            date_to = datetime.datetime.fromisoformat(data['date_to'])
            if date_to.tzinfo is None:
                date_to = tz.localize(date_to)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        date_to = None
    
    result = Transaction.serialized_filtered_transactions(
        transaction_types=transaction_types,
        material_group=material_group,
        material=material,
        date_from=date_from,
        date_to=date_to
    )

    return JsonResponse(result, safe=False) 

def get_summary(request):
    print("REQUEST RECEIVED: get_summary")
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    # check inputs
    data = request.GET

    # resolution
    if data.get('resolution') is not None:
        try:
            print(data['resolution'])
            resolution = Resolution(data['resolution'])
        except ValueError:
            return JsonResponse({"error": "Resolution not found."}, status=404)
    else:
        return JsonResponse({"error": "Resolution missing."}, status=400)
    # material group / material
    if data.get('material') is not None:
        print(data['material'])
        try:
            filter_by = Material.objects.get(pk=data['material']) 
        except Material.DoesNotExist:
            return JsonResponse({"error": "Material not found."}, status=404)
    elif data.get('material_group') is not None:
        print(data['material_group'])
        try:
            filter_by = MaterialGroup.objects.get(pk=data['material_group']) 
        except MaterialGroup.DoesNotExist:
            return JsonResponse({"error": "Material Group not found."}, status=404)
    else:
        filter_by = None

    # start date
    if data.get('date_from') is not None:
        try:
            date_from = datetime.datetime.fromisoformat(data['date_from'])
            if date_from.tzinfo is None:
                date_from = tz.localize(date_from)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        return JsonResponse({"error": "Invalid date"}, status=400)
    # end date
    if data.get('date_to') is not None:
        print(data['date_to'])
        try:
            date_to = datetime.datetime.fromisoformat(data['date_to'])
            if date_to.tzinfo is None:
                date_to = tz.localize(date_to)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        return JsonResponse({"error": "Invalid date"}, status=400)

    result = generate_report(date_from, date_to, resolution, filter_by)

    return JsonResponse(result, safe=False)