from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect 

from .models import GoodsReceiptNote, GoodsDispatchNote
from inventories.models import Transaction
from .forms import (
    GoodsReceiptNoteHeaderForm, GoodsDispatchNoteHeaderForm, 
    GoodsReceiptTransactionFormSet, GoodsDispatchTransactionFormSet
)


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
        transaction_formset = GoodsReceiptTransactionFormSet()

        return self.render_to_response(
            self.get_context_data(header_form=header_form, transaction_formset=transaction_formset)
        )

    def get_context_data(self, **kwargs):
        context = super(GoodsReceiptNoteCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['header_form'] = GoodsReceiptNoteHeaderForm(self.request.POST)
            context['transaction_formset'] = GoodsReceiptTransactionFormSet(self.request.POST,
                prefix='transaction', 
            )
        else:
            context['header_form'] = GoodsReceiptNoteHeaderForm()
            context['transaction_formset'] = GoodsReceiptTransactionFormSet(
                prefix='transaction', 
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = GoodsReceiptTransactionFormSet(self.request.POST, prefix='transaction')
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

        for instance in transaction_formset:
            # set transaction type
            transaction = instance.save(commit=False)            
            transaction.transaction_type = Transaction.TYPE_IN
            transaction.save()

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
        transaction_formset = GoodsReceiptTransactionFormSet()

        return self.render_to_response(
            self.get_context_data(header_form=header_form, transaction_formset=transaction_formset)
        )

    def get_context_data(self, **kwargs):
        context = super(GoodsReceiptNoteUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['header_form'] = GoodsReceiptNoteHeaderForm(self.request.POST, instance=self.object)
            context['transaction_formset'] = GoodsReceiptTransactionFormSet(self.request.POST, instance=self.object,
                    prefix='transaction', 
                )
        else:
            context['header_form'] = GoodsReceiptNoteHeaderForm(instance=self.object)
            context['transaction_formset'] = GoodsReceiptTransactionFormSet(instance=self.object,
                    prefix='transaction', 
                )
        return context

    def post(self, request, *args, **kwargs):
        print('POST')
        self.object = self.get_object()
        print(self.object)
        print(self.request)
        print(self.request.POST)
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = GoodsReceiptTransactionFormSet(self.request.POST, instance=self.object, prefix='transaction')     
        print(transaction_formset.errors)   
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


# Goods Receipt Note

class GoodsDispatchNoteCreateView(CreateView):
    model = GoodsDispatchNote
    form_class = GoodsDispatchNoteHeaderForm
    template_name = "documents/goods_dispatch_note_new.html"
    success_url = reverse_lazy("goods_dispatch_note_list")

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = GoodsDispatchTransactionFormSet()

        return self.render_to_response(
            self.get_context_data(header_form=header_form, transaction_formset=transaction_formset)
        )

    def get_context_data(self, **kwargs):
        context = super(GoodsDispatchNoteCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['header_form'] = GoodsDispatchNoteHeaderForm(self.request.POST)
            context['transaction_formset'] = GoodsDispatchTransactionFormSet(self.request.POST,
                prefix='transaction', 
            )
        else:
            context['header_form'] = GoodsDispatchNoteHeaderForm()
            context['transaction_formset'] = GoodsDispatchTransactionFormSet(
                prefix='transaction', 
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = GoodsDispatchTransactionFormSet(self.request.POST, prefix='transaction')
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

        for instance in transaction_formset:
            # set transaction type
            transaction = instance.save(commit=False)            
            transaction.transaction_type = Transaction.TYPE_OUT
            transaction.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, header_form, transaction_formset):
        return self.render_to_response(
            self.get_context_data(
                header_form=header_form,
                transaction_formset=transaction_formset)
            )


class GoodsDispatchNoteUpdateView(UpdateView):
    model = GoodsDispatchNote
    form_class = GoodsDispatchNoteHeaderForm
    template_name = "documents/goods_dispatch_note_edit.html"
    success_url = reverse_lazy("goods_dispatch_note_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = GoodsDispatchTransactionFormSet()

        return self.render_to_response(
            self.get_context_data(header_form=header_form, transaction_formset=transaction_formset)
        )

    def get_context_data(self, **kwargs):
        context = super(GoodsDispatchNoteUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['header_form'] = GoodsDispatchNoteHeaderForm(self.request.POST, instance=self.object)
            context['transaction_formset'] = GoodsDispatchTransactionFormSet(self.request.POST, instance=self.object,
                    prefix='transaction', 
                )
        else:
            context['header_form'] = GoodsDispatchNoteHeaderForm(instance=self.object)
            context['transaction_formset'] = GoodsDispatchTransactionFormSet(instance=self.object,
                    prefix='transaction', 
                )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        header_form = self.get_form(form_class)
        transaction_formset = GoodsDispatchTransactionFormSet(self.request.POST, instance=self.object, prefix='transaction')        
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


class GoodsDispatchNoteListView(ListView):
    model = GoodsDispatchNote
    context_object_name = 'goods_dispatch_note_list'
    template_name = 'documents/goods_dispatch_note_list.html'


class GoodsDispatchNoteDetailView(DetailView):
    model = GoodsDispatchNote
    context_object_name = 'goods_dispatch_note'
    template_name = 'documents/goods_dispatch_note_detail.html'


class GoodsDispatchNoteDeleteView(DeleteView):
    model = GoodsDispatchNote
    context_object_name = 'goods_dispatch_note'
    template_name = 'documents/goods_dispatch_note_delete.html'
    success_url = reverse_lazy('goods_dispatch_note_list')

# https://docs.djangoproject.com/en/3.2/topics/forms/formsets/
# https://www.codementor.io/@ankurrathore/handling-multiple-instances-of-django-forms-in-templates-8guz5s0pc
# https://stackoverflow.com/questions/59855371/django-inlineformset-factory-in-updateview-formset-data-is-not-update

