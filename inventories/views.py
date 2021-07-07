from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.admin import widgets

from .models import MaterialGroup, Material, Transaction


# Material Groups

class MaterialGroupListView(ListView):
    model = MaterialGroup
    context_object_name = 'material_group_list'
    template_name = 'inventories/material_group_list.html'

class MaterialGroupDetailView(DetailView):
    model = MaterialGroup
    context_object_name = 'material_group'
    template_name = 'inventories/material_group_detail.html'

class MaterialGroupCreateView(CreateView):
    model = MaterialGroup
    fields = ('name',)
    template_name = 'inventories/material_group_new.html'

class MaterialGroupUpdateView(UpdateView):
    model = MaterialGroup
    context_object_name = 'material_group'
    fields = ('name',)
    template_name = 'inventories/material_group_edit.html'

class MaterialGroupDeleteView(DeleteView):
    model = MaterialGroup
    context_object_name = 'material_group'
    template_name = 'inventories/material_group_delete.html'
    success_url = reverse_lazy('material_group_list')


# Materials

class MaterialListView(ListView):
    model = Material
    context_object_name = 'material_list'
    template_name = 'inventories/material_list.html'

class MaterialDetailView(DetailView):
    model = Material
    context_object_name = 'material'
    template_name = 'inventories/material_detail.html'

class MaterialCreateView(CreateView):
    model = Material
    fields = ('name', 'material_group',)
    template_name = 'inventories/material_new.html'

class MaterialUpdateView(UpdateView):
    model = Material
    context_object_name = 'material'
    fields = ('name', 'material_group',)
    template_name = 'inventories/material_edit.html'

class MaterialDeleteView(DeleteView):
    model = Material
    context_object_name = 'material'
    template_name = 'inventories/material_delete.html'
    success_url = reverse_lazy('material_list')


# Transactions

class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'inventories/transaction_list.html'

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