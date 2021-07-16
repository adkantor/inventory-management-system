import uuid
from django.db import models
from django.db.models import Q
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

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name
        }

    @staticmethod
    def serialize_all():
        return [material_group.serialize() for material_group in MaterialGroup.objects.order_by('name').all()]


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

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'material_group_id': str(self.material_group.id)
        }

    @staticmethod
    def serialize_all(material_group):
        if material_group:
            return [material.serialize() for material in Material.objects.filter(material_group=material_group).order_by('name').all()]
        else:
            return [material.serialize() for material in Material.objects.order_by('name').all()]


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
        return round(self.net_weight * self.unit_price, 2)

    @property
    def partner_name(self):
        if self.goods_receipt_note:
            return self.goods_receipt_note.vendor_name
        elif self.goods_dispatch_note:
            return self.goods_dispatch_note.customer_name
        return None

    def serialize(self):
        return {
            'id': str(self.id),
            'transaction_type': self.transaction_type,
            'material_group': self.material.material_group.name,
            'material': self.material.name,
            'transaction_time': self.transaction_time.strftime('%Y-%m-%d %H:%M'),
            'created_time': self.created_time,
            'last_modified': self.last_modified,
            'gross_weight': self.gross_weight,
            'tare_weight': self.tare_weight,
            'net_weight': self.net_weight,
            'unit_price': self.unit_price,
            'net_value': self.net_value,
            'notes': self.notes,
            'goods_receipt_note': str(self.goods_receipt_note.id) if self.goods_receipt_note else None,
            'goods_dispatch_note': str(self.goods_dispatch_note.id) if self.goods_dispatch_note else None,
            'partner': self.partner_name
        }

    @staticmethod
    def serialized_filtered_transactions(transaction_types=None, material_group=None, material=None,
                                         date_from=None, date_to=None):
        q = Q()
        if transaction_types is not None:
            if isinstance(transaction_types, list):
                q_sub = Q()
                for transaction_type in transaction_types:
                    q_sub |= Q(transaction_type=transaction_type)
                q &= q_sub
            else:
                q &= Q(transaction_type=transaction_types)
        if material_group is not None:
            q &= Q(material__material_group=material_group)
        if material is not None:
            q &= Q(material=material)
        if date_from is not None:
            q &= Q(transaction_time__gte=date_from)
        if date_to is not None:
            q &= Q(transaction_time__lte=date_to)

        transactions = Transaction.objects.filter(q).order_by('-transaction_time').all()
        return [transaction.serialize() for transaction in transactions]

    def __str__(self):
        return f'{self.transaction_time} | {self.transaction_type} | {self.net_weight}  |  {self.material.name} | $({self.net_value})'

    def get_absolute_url(self):
        return reverse('transaction_detail', args=[str(self.id)])