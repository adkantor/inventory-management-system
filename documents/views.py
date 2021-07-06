from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.admin import widgets
# from django.forms import formset_factory
from django.shortcuts import render
from django.http import HttpResponseRedirect 

from .models import GoodsReceiptNote
from inventories.models import Transaction
from .forms import GoodsReceiptNoteHeaderForm, GoodsReceiptNoteTransactionsForm, TransactionFormSet


# Goods Receipt Note

class GoodsReceiptNoteCreateView(View):
    # HeaderForm = GoodsReceiptNoteHeaderForm
    # TransactionFormSet = formset_factory(GoodsReceiptNoteTransactionsForm)

    #The Template name where we are going to display it
    template_name = "documents/goods_receipt_note_new.html"

    def get(self, request, *args, **kwargs):
        context={
            'header_form':GoodsReceiptNoteHeaderForm(),
            'transaction_formset':TransactionFormSet(
                prefix='transaction', 
                queryset=Transaction.objects.none(), 
            ),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print('>>>POST')
        print(request.POST)
        header_form=GoodsReceiptNoteHeaderForm(self.request.POST)
        transaction_formset=TransactionFormSet(self.request.POST, prefix='transaction')
        print(f'header_form valid?: {header_form.is_valid()}')
        print(f'transaction_formset valid?: {transaction_formset.is_valid()}')
        print(transaction_formset.errors)
        
        #Checking the if the form is valid
        if header_form.is_valid() and transaction_formset.is_valid():
            print('>>>POST is valid')
            # save header
            goods_receipt_note = header_form.save()
            print(goods_receipt_note.id)
            # save transactions
            for instance in transaction_formset:
                transaction = instance.save(commit=False)
                # set transaction type
                transaction.transaction_type = Transaction.TYPE_IN
                # link transaction to GRN
                transaction.goods_receipt_note = goods_receipt_note
                # save	
                transaction.save()

            return HttpResponseRedirect(reverse("goods_receipt_note_list"))

        else:
            print('>>>POST is invalid')
            context={
                'header_form':self.HeaderForm(),
                'transaction_formset':self.TransactionFormSet(prefix='transaction'),
            }
            return render(request, self.template_name, context)


class GoodsReceiptNoteListView(ListView):
    model = GoodsReceiptNote
    context_object_name = 'goods_receipt_note_list'
    template_name = 'documents/goods_receipt_note_list.html'

class GoodsReceiptNoteDetailView(DetailView):
    model = GoodsReceiptNote
    context_object_name = 'goods_receipt_note'
    template_name = 'documents/goods_receipt_note_detail.html'

# class GoodsReceiptNoteDeleteView(DeleteView):
#     model = GoodsReceiptNote
#     context_object_name = 'goods_receipt_note'
#     template_name = 'inventories/goods_receipt_note_delete.html'
#     success_url = reverse_lazy('goods_receipt_note_list')


# https://docs.djangoproject.com/en/3.2/topics/forms/formsets/
# https://www.codementor.io/@ankurrathore/handling-multiple-instances-of-django-forms-in-templates-8guz5s0pc

