import uuid
from django.db import models
from django.urls import reverse

from documents.models import GoodsReceiptNote, GoodsDispatchNote

def get_deleted_material_group():
    return MaterialGroup.objects.get_or_create(name='deleted')[0].id

def get_undefined_material_group():
    return MaterialGroup.objects.get_or_create(name='undefined')[0].id


class MaterialGroup(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('material_group_detail', args=[str(self.id)])

    def price_at(date):
        pass # TODO


class Material(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    material_group = models.ForeignKey(
            MaterialGroup,
            related_name='materials',
            on_delete=models.SET(get_deleted_material_group), 
            default=get_undefined_material_group
            )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('material_detail', args=[str(self.id)])

    def price_at(date):
        pass # TODO


class Transaction(models.Model):
    TYPE_IN = 'IN'
    TYPE_OUT = 'OUT'
    TYPE_CHOICES = [
        (TYPE_IN, 'Inbound'),
        (TYPE_OUT, 'Outbound')
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    transaction_type = models.CharField(max_length=3, choices=TYPE_CHOICES, default=TYPE_IN)
    material = models.ForeignKey(Material, related_name='transactions', on_delete=models.CASCADE)
    transaction_time = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    gross_weight = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    tare_weight = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    notes = models.TextField(max_length=255, blank=True)
    goods_receipt_note = models.ForeignKey(
        GoodsReceiptNote, 
        related_name='transactions', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)
    goods_dispatch_note = models.ForeignKey(
        GoodsDispatchNote, 
        related_name='transactions', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)

    @property
    def net_weight(self):
        return self.gross_weight - self.tare_weight

    @property
    def net_value(self):
        return self.net_weight * self.unit_price

    def __str__(self):
        return f'{self.transaction_time} | {self.transaction_type} | {self.net_weight}  |  {self.material.name} | $({self.net_value})'

    def get_absolute_url(self):
        return reverse('transaction_detail', args=[str(self.id)])