from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import MaterialGroup, Material



# ------------   Material Groups   ------------


class MaterialGroupListView(LoginRequiredMixin, ListView):
    model = MaterialGroup
    context_object_name = 'inventory_list'
    template_name = 'inventories/inventory_list.html'
    ordering = ['name']


class MaterialGroupDetailView(LoginRequiredMixin, DetailView):
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_detail.html'


class MaterialGroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventories.add_materialgroup'
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_new.html'
    fields = ('name',)
    success_url = reverse_lazy('material_group_list')


class MaterialGroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventories.change_materialgroup'
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_edit.html'
    fields = ('name',)
    success_url = reverse_lazy('material_group_list')


class MaterialGroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventories.delete_materialgroup'
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_delete.html'
    success_url = reverse_lazy('material_group_list')



# ------------   Materials   ------------


class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    context_object_name = 'inventory_list'
    template_name = 'inventories/inventory_list.html'
    ordering = ['name']


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    context_object_name = 'item'
    template_name = 'inventories/inventory_detail.html'


class MaterialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventories.add_material'
    model = Material
    fields = ('name', 'material_group',)
    template_name = 'inventories/inventory_new.html'
    success_url = reverse_lazy('material_list')


class MaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventories.change_material'
    model = Material
    context_object_name = 'item'
    fields = ('name', 'material_group',)
    template_name = 'inventories/inventory_edit.html'

class MaterialDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventories.delete_material'
    model = Material
    context_object_name = 'item'
    template_name = 'inventories/inventory_delete.html'
    success_url = reverse_lazy('material_list')