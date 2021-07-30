from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.admin import widgets

from .models import MaterialGroup, Material, Transaction


# ------------   Material Groups   ------------

class MaterialGroupListView(ListView):
    model = MaterialGroup
    context_object_name = 'inventory_list'
    template_name = 'inventories/inventory_list.html'
    ordering = ['name']

class MaterialGroupDetailView(DetailView):
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_detail.html'

class MaterialGroupCreateView(CreateView):
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_new.html'
    fields = ('name',)
    success_url = reverse_lazy('material_group_list')

class MaterialGroupUpdateView(UpdateView):
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_edit.html'
    fields = ('name',)
    success_url = reverse_lazy('material_group_list')

class MaterialGroupDeleteView(DeleteView):
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_delete.html'
    success_url = reverse_lazy('material_group_list')


# ------------   Materials   ------------

class MaterialListView(ListView):
    model = Material
    context_object_name = 'inventory_list'
    template_name = 'inventories/inventory_list.html'
    ordering = ['name']

class MaterialDetailView(DetailView):
    model = Material
    context_object_name = 'item'
    template_name = 'inventories/inventory_detail.html'

class MaterialCreateView(CreateView):
    model = Material
    fields = ('name', 'material_group',)
    template_name = 'inventories/inventory_new.html'

class MaterialUpdateView(UpdateView):
    model = Material
    context_object_name = 'item'
    fields = ('name', 'material_group',)
    template_name = 'inventories/inventory_edit.html'

class MaterialDeleteView(DeleteView):
    model = Material
    context_object_name = 'item'
    template_name = 'inventories/inventory_delete.html'
    success_url = reverse_lazy('material_list')