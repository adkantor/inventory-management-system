from django.views.generic import ListView, DetailView
from .models import MaterialGroup, Material, Transaction


class MaterialGroupListView(ListView):
    model = MaterialGroup
    context_object_name = 'material_group_list'
    template_name = 'inventories/material_group_list.html'

class MaterialGroupDetailView(DetailView):
    model = MaterialGroup
    context_object_name = 'material_group'
    template_name = 'inventories/material_group_detail.html'

class MaterialListView(ListView):
    model = Material
    context_object_name = 'material_list'
    template_name = 'inventories/material_list.html'

class MaterialDetailView(DetailView):
    model = Material
    context_object_name = 'material'
    template_name = 'inventories/material_detail.html'

class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'inventories/transaction_list.html'

class TransactionDetailView(DetailView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'inventories/transaction_detail.html'