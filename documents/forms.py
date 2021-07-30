from django import forms
from django.contrib.admin import widgets
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit, Row, Column
from .custom_layout_objects import TransactionFormset

from .models import GoodsReceiptNote, GoodsDispatchNote
from inventories.models import Transaction

class GoodsReceiptNoteHeaderForm(forms.ModelForm):

    # class Meta:
    #     model=GoodsReceiptNote
    #     fields=['date', 'vendor', 'notes']
    #     widgets = {
    #         'date': forms.DateInput(attrs={'type': 'date', 'required': True}),
    #         'vendor': forms.Select(attrs={'required': True}),
    #         'notes': forms.Textarea(),  
    #     }

    class Meta:
        model=GoodsReceiptNote
        fields=['date', 'vendor', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'required': True}, format=('%Y-%m-%d')),
            'vendor': forms.Select(attrs={'required': True}),
            'notes': forms.Textarea(attrs={'rows': '3', 'cols': '100'}),  
        }

    def __init__(self, *args, **kwargs):
        super(GoodsReceiptNoteHeaderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        # self.helper.form_class = 'table_inline_formset'#'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('date', css_class='form-group col-md-6 mb-0'),
                    Column('vendor', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),  
                Fieldset('Add transactions',
                    TransactionFormset('transaction_formset')
                ),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

class GoodsDispatchNoteHeaderForm(forms.ModelForm):

    class Meta:
        model=GoodsDispatchNote
        fields=['date', 'customer', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'required': True}, format=('%Y-%m-%d')),
            'customer': forms.Select(attrs={'required': True}),
            'notes': forms.Textarea(attrs={'rows': '3', 'cols': '100'}),  
        }

    def __init__(self, *args, **kwargs):
        super(GoodsDispatchNoteHeaderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        # self.helper.form_class = 'table_inline_formset'#'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('date', css_class='form-group col-md-6 mb-0'),
                    Column('customer', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),  
                Fieldset('Add transactions',
                    TransactionFormset('transaction_formset')
                ),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

class GoodsReceiptNoteTransactionsForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['material', 'transaction_time', 'gross_weight', 'tare_weight', 'unit_price', 'notes']
        widgets = {
            'material': forms.Select(attrs={'required': True}),
            'transaction_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}, format=('%Y-%m-%dT%H:%M')),                      
            'gross_weight': forms.NumberInput(attrs={'required': True}),
            'tare_weight': forms.NumberInput(attrs={'required': True}),
            'unit_price': forms.NumberInput(attrs={'required': True}),
            'notes': forms.TextInput(),  
        }

class GoodsDispatchNoteTransactionsForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['material', 'transaction_time', 'gross_weight', 'tare_weight', 'unit_price', 'notes']
        widgets = {
            'material': forms.Select(attrs={'required': True}),
            'transaction_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}, format=('%Y-%m-%dT%H:%M')),     
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