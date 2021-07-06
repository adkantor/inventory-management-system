from inventories.models import Transaction
from django import forms
from django.contrib.admin import widgets
from django.forms import formset_factory, modelformset_factory

from .models import GoodsReceiptNote
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


class GoodsReceiptNoteTransactionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """If no initial data, provide some defaults."""
        initial = kwargs.get('initial', {})
        initial['gross_weight'] = 0
        initial['tare_weight'] = 0
        initial['unit_price'] = 0
        kwargs['initial'] = initial
        super(GoodsReceiptNoteTransactionsForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Transaction
        # fields=['transaction_type', 'material', 'transaction_time', 'gross_weight', 'tare_weight', 'unit_price', 'notes']
        fields=['material', 'transaction_time', 'gross_weight', 'tare_weight', 'unit_price', 'notes']
        field_classes = {
            'transaction_time': forms.SplitDateTimeField,
        }
        widgets = {
            # 'transaction_type': forms.TextInput(attrs={'required': True, 'readonly': True, 'disabled': True, 'value': 'IN'}),
            'material': forms.Select(attrs={'required': True}),
            'transaction_time': widgets.AdminSplitDateTime(attrs={'required': True}),            
            'gross_weight': forms.NumberInput(attrs={'required': True}),
            'tare_weight': forms.NumberInput(attrs={'required': True}),
            'unit_price': forms.NumberInput(attrs={'required': True}),
            'notes': forms.TextInput(),  
        }

# TransactionFormSet = formset_factory(GoodsReceiptNoteTransactionsForm)

TransactionFormSet = modelformset_factory(Transaction, 
    form=GoodsReceiptNoteTransactionsForm,
    extra=0,
    min_num=1, 
    validate_min=True
)