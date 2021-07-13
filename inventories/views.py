from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.admin import widgets

from .models import MaterialGroup, Material, Transaction


# Material Groups

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
    fields = ('name',)
    template_name = 'inventories/inventory_new.html'
    success_url = reverse_lazy('material_group_list')

class MaterialGroupUpdateView(UpdateView):
    model = MaterialGroup
    context_object_name = 'item'
    fields = ('name',)
    template_name = 'inventories/inventory_edit.html'
    success_url = reverse_lazy('material_group_list')

class MaterialGroupDeleteView(DeleteView):
    model = MaterialGroup
    context_object_name = 'item'
    template_name = 'inventories/inventory_delete.html'
    success_url = reverse_lazy('material_group_list')


# Materials

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


# Transactions

class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'inventories/transaction_list.html'
    ordering = ['-transaction_time']

class TransactionDetailView(DetailView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'inventories/transaction_detail.html'

class TransactionDeleteView(DeleteView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'inventories/transaction_delete.html'
    success_url = reverse_lazy('transaction_list')

class GoodsReceiptCreateView(CreateView):
    model = Transaction
    context_object_name = 'transaction'
    fields = ('material', 'transaction_time', 'gross_weight', 'tare_weight',
              'unit_price', 'notes', 'goods_receipt_note')
    template_name = 'inventories/goods_receipt_new.html'

    def get_form(self):
        form = super(GoodsReceiptCreateView, self).get_form()
        form.fields['transaction_time'].widget = widgets.AdminSplitDateTime()
        return form

    def form_valid(self, form):
        form.instance.transaction_type = Transaction.TYPE_IN
        return super().form_valid(form)

class GoodsDispatchCreateView(CreateView):
    model = Transaction
    context_object_name = 'transaction'
    fields = ('material', 'transaction_time', 'gross_weight', 'tare_weight',
              'unit_price', 'notes', 'goods_dispatch_note')
    template_name = 'inventories/goods_dispatch_new.html'

    def get_form(self):
        form = super(GoodsDispatchCreateView, self).get_form()
        form.fields['transaction_time'].widget = widgets.AdminSplitDateTime()
        return form

    def form_valid(self, form):
        form.instance.transaction_type = Transaction.TYPE_OUT
        return super().form_valid(form)   

class GoodsReceiptUpdateView(UpdateView):    
    model = Transaction
    context_object_name = 'transaction'
    fields = ('transaction_type', 'material', 'transaction_time', 'gross_weight', 'tare_weight',
              'unit_price', 'notes', 'goods_receipt_note')
    template_name = 'inventories/goods_receipt_edit.html' 

    def get_form(self):
        form = super(GoodsReceiptUpdateView, self).get_form()
        form.fields['transaction_time'].widget = widgets.AdminSplitDateTime(attrs={'required': True})
        form.fields['transaction_type'].widget.attrs['readonly'] = True
        form.fields['transaction_type'].widget.attrs['disabled'] = True
        return form

class GoodsDispatchUpdateView(UpdateView):    
    model = Transaction
    context_object_name = 'transaction'
    fields = ('transaction_type', 'material', 'transaction_time', 'gross_weight', 'tare_weight',
              'unit_price', 'notes', 'goods_dispatch_note')
    template_name = 'inventories/goods_dispatch_edit.html' 

    def get_form(self):
        form = super(GoodsDispatchUpdateView, self).get_form()
        form.fields['transaction_time'].widget = widgets.AdminSplitDateTime(attrs={'required': True})
        form.fields['transaction_type'].widget.attrs['readonly'] = True
        form.fields['transaction_type'].widget.attrs['disabled'] = True
        return form