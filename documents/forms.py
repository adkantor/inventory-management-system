from django import forms
from django.contrib.admin import widgets
from django.forms import inlineformset_factory

from .models import GoodsReceiptNote, GoodsDispatchNote
from inventories.models import Transaction

class GoodsReceiptNoteHeaderForm(forms.ModelForm):

    class Meta:
        model=GoodsReceiptNote
        fields=['date', 'vendor', 'notes']
        widgets = {
            'date': widgets.AdminDateWidget(attrs={'required': True}),
            'vendor': forms.Select(attrs={'required': True}),
            'notes': forms.Textarea(),  
        }

class GoodsDispatchNoteHeaderForm(forms.ModelForm):

    class Meta:
        model=GoodsDispatchNote
        fields=['date', 'customer', 'notes']
        widgets = {
            'date': widgets.AdminDateWidget(attrs={'required': True}),
            'customer': forms.Select(attrs={'required': True}),
            'notes': forms.Textarea(),  
        }

class GoodsReceiptNoteTransactionsForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['material', 'transaction_time', 'gross_weight', 'tare_weight', 'unit_price', 'notes']
        field_classes = {
            'transaction_time': forms.SplitDateTimeField,
        }
        widgets = {
            'material': forms.Select(attrs={'required': True}),
            'transaction_time': widgets.AdminSplitDateTime(attrs={'required': True}),            
            'gross_weight': forms.NumberInput(attrs={'required': True}),
            'tare_weight': forms.NumberInput(attrs={'required': True}),
            'unit_price': forms.NumberInput(attrs={'required': True}),
            'notes': forms.TextInput(),  
        }

class GoodsDispatchNoteTransactionsForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['material', 'transaction_time', 'gross_weight', 'tare_weight', 'unit_price', 'notes']
        field_classes = {
            'transaction_time': forms.SplitDateTimeField,
        }
        widgets = {
            'material': forms.Select(attrs={'required': True}),
            'transaction_time': widgets.AdminSplitDateTime(attrs={'required': True}),            
            'gross_weight': forms.NumberInput(attrs={'required': True}),
            'tare_weight': forms.NumberInput(attrs={'required': True}),
            'unit_price': forms.NumberInput(attrs={'required': True}),
            'notes': forms.TextInput(),  
        }

GoodsReceiptTransactionFormSet = inlineformset_factory(GoodsReceiptNote, Transaction, 
    form=GoodsReceiptNoteTransactionsForm,
    extra=0,
    min_num=1, 
    validate_min=True
)

GoodsDispatchTransactionFormSet = inlineformset_factory(GoodsDispatchNote, Transaction, 
    form=GoodsDispatchNoteTransactionsForm,
    extra=0,
    min_num=1, 
    validate_min=True
)