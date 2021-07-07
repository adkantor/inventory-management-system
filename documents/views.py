from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect 

from .models import GoodsReceiptNote
from inventories.models import Transaction
from .forms import GoodsReceiptNoteHeaderForm, TransactionFormSet


# Goods Receipt Note

class GoodsReceiptNoteCreateView(CreateView):
    model = GoodsReceiptNote
    form_class = GoodsReceiptNoteHeaderForm
    template_name = "documents/goods_receipt_note_new.html"
    success_url = reverse_lazy("goods_receipt_note_list")

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = TransactionFormSet()

        return self.render_to_response(
            self.get_context_data(header_form=header_form, transaction_formset=transaction_formset)
        )

    def get_context_data(self, **kwargs):
        context = super(GoodsReceiptNoteCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['header_form'] = GoodsReceiptNoteHeaderForm(self.request.POST)
            context['transaction_formset'] = TransactionFormSet(self.request.POST,
                prefix='transaction', 
            )
        else:
            context['header_form'] = GoodsReceiptNoteHeaderForm()
            context['transaction_formset'] = TransactionFormSet(
                prefix='transaction', 
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = TransactionFormSet(self.request.POST, prefix='transaction')
        #Checking the if the form is valid
        if header_form.is_valid() and transaction_formset.is_valid():
            return self.form_valid(header_form, transaction_formset)
        else:
            return self.form_invalid(header_form, transaction_formset)

    def form_valid(self, header_form, transaction_formset):
        self.object = header_form.save()
        print(self.object.id)
        transaction_formset.instance = self.object
        transaction_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, header_form, transaction_formset):
        return self.render_to_response(
            self.get_context_data(
                header_form=header_form,
                transaction_formset=transaction_formset)
            )


class GoodsReceiptNoteUpdateView(UpdateView):
    model = GoodsReceiptNote
    form_class = GoodsReceiptNoteHeaderForm
    template_name = "documents/goods_receipt_note_edit.html"
    success_url = reverse_lazy("goods_receipt_note_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = TransactionFormSet()

        return self.render_to_response(
            self.get_context_data(header_form=header_form, transaction_formset=transaction_formset)
        )

    def get_context_data(self, **kwargs):
        context = super(GoodsReceiptNoteUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['header_form'] = GoodsReceiptNoteHeaderForm(self.request.POST, instance=self.object)
            context['transaction_formset'] = TransactionFormSet(self.request.POST, instance=self.object,
                    prefix='transaction', 
                )
        else:
            context['header_form'] = GoodsReceiptNoteHeaderForm(instance=self.object)
            context['transaction_formset'] = TransactionFormSet(instance=self.object,
                    prefix='transaction', 
                )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = TransactionFormSet(self.request.POST, instance=self.object, prefix='transaction')        
        #Checking the if the form is valid
        if header_form.is_valid() and transaction_formset.is_valid():
            return self.form_valid(header_form, transaction_formset)
        else:
            return self.form_invalid(header_form, transaction_formset)

    def form_valid(self, header_form, transaction_formset):
        self.object = header_form.save()
        transaction_formset.instance = self.object
        transaction_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, header_form, transaction_formset):
        return self.render_to_response(
            self.get_context_data(header_form=header_form, transaction_formset=transaction_formset)
        )


class GoodsReceiptNoteListView(ListView):
    model = GoodsReceiptNote
    context_object_name = 'goods_receipt_note_list'
    template_name = 'documents/goods_receipt_note_list.html'


class GoodsReceiptNoteDetailView(DetailView):
    model = GoodsReceiptNote
    context_object_name = 'goods_receipt_note'
    template_name = 'documents/goods_receipt_note_detail.html'


class GoodsReceiptNoteDeleteView(DeleteView):
    model = GoodsReceiptNote
    context_object_name = 'goods_receipt_note'
    template_name = 'documents/goods_receipt_note_delete.html'
    success_url = reverse_lazy('goods_receipt_note_list')


# https://docs.djangoproject.com/en/3.2/topics/forms/formsets/
# https://www.codementor.io/@ankurrathore/handling-multiple-instances-of-django-forms-in-templates-8guz5s0pc
# https://stackoverflow.com/questions/59855371/django-inlineformset-factory-in-updateview-formset-data-is-not-update

