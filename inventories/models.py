import uuid
from django.db import models
from django.db.models import Q, Sum, ExpressionWrapper, F, When, Case, Window
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

    # def price_at(self, date):
    #     pass # TODO

    # def balance_at(self, date):
    #     net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    #     result = Transaction.objects.filter(
    #         Q(transaction_type=Transaction.TYPE_IN) &
    #         Q(material__material_group=self) &
    #         Q(transaction_time__lte=date)
    #     ).annotate(
    #             net_weight=net_weight_exp
    #     ).aggregate(Sum('net_weight'))
    #     cum_in_to_date = result['net_weight__sum'] or 0
        
    #     result = Transaction.objects.filter(
    #         Q(transaction_type=Transaction.TYPE_OUT) &
    #         Q(material__material_group=self) &
    #         Q(transaction_time__lte=date)
    #     ).annotate(
    #             net_weight=net_weight_exp
    #     ).aggregate(Sum('net_weight'))
    #     cum_out_to_date = result['net_weight__sum'] or 0
        
    #     return cum_in_to_date - cum_out_to_date

    # def movement_between(self, transaction_type, date_from, date_to):
    #     net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    #     result = Transaction.objects.filter(
    #         Q(transaction_type=transaction_type) &
    #         Q(material__material_group=self) &
    #         Q(transaction_time__gte=date_from) &
    #         Q(transaction_time__lte=date_to)
    #     ).annotate(
    #             net_weight=net_weight_exp
    #     ).aggregate(Sum('net_weight'))
    #     return result['net_weight__sum'] or 0  

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

    # def price_at(date):
    #     pass # TODO

    # def balance_at(self, date):
    #     net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    #     result = Transaction.objects.filter(
    #         Q(transaction_type=Transaction.TYPE_IN) &
    #         Q(material=self) &
    #         Q(transaction_time__lte=date)
    #     ).annotate(
    #             net_weight=net_weight_exp
    #     ).aggregate(Sum('net_weight'))
    #     cum_in_to_date = result['net_weight__sum'] or 0
        
    #     result = Transaction.objects.filter(
    #         Q(transaction_type=Transaction.TYPE_OUT) &
    #         Q(material=self) &
    #         Q(transaction_time__lte=date)
    #     ).annotate(
    #             net_weight=net_weight_exp
    #     ).aggregate(Sum('net_weight'))
    #     cum_out_to_date = result['net_weight__sum'] or 0
        
    #     return cum_in_to_date - cum_out_to_date

    # def movement_between(self, transaction_type, date_from, date_to):
    #     net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    #     result = Transaction.objects.filter(
    #         Q(transaction_type=transaction_type) &
    #         Q(material=self) &
    #         Q(transaction_time__gte=date_from) &
    #         Q(transaction_time__lte=date_to)
    #     ).annotate(
    #             net_weight=net_weight_exp
    #     ).aggregate(Sum('net_weight'))
    #     return result['net_weight__sum'] or 0        
        

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

    # @property
    # def net_signed_weight(self):
    #     mult = 1 if self.transaction_type == self.TYPE_IN else -1
    #     return self.net_weight * mult

    @property
    def net_value(self):
        return round(self.net_weight * self.unit_price, 2)

    # @property
    # def net_signed_value(self):
    #     mult = 1 if self.transaction_type == self.TYPE_IN else -1
    #     return self.net_value * mult

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

    # @staticmethod
    # def transactions_with_annotations(material_group=None, material=None, date_from=None, date_to=None):
    #     q = Q()
    #     if material_group is not None:
    #         q &= Q(material__material_group=material_group)
    #     if material is not None:
    #         q &= Q(material=material)
    #     if date_from is not None:
    #         q &= Q(transaction_time__gte=date_from)
    #     if date_to is not None:
    #         q &= Q(transaction_time__lte=date_to)
    #     transactions = Transaction.objects.filter(q).order_by('transaction_time')\
    #         .annotate(
    #             net_signed_weight=ExpressionWrapper((F('gross_weight') - F('tare_weight')) * Case(When(transaction_type=Transaction.TYPE_IN, then=1), When(transaction_type=Transaction.TYPE_OUT, then=-1)), output_field=models.DecimalField(max_digits=7, decimal_places=2)),
    #             net_signed_value=ExpressionWrapper(F('net_signed_weight') * F('unit_price'), output_field=models.DecimalField(max_digits=7, decimal_places=2)),
    #             balance=ExpressionWrapper(Window(Sum('net_signed_weight'), order_by=F('transaction_time').asc()), output_field=models.DecimalField(max_digits=7, decimal_places=2)),
    #     ).all()
    #     # print(transactions.values())
    #     return transactions


    def __str__(self):
        return f'{self.transaction_time} | {self.transaction_type} | {self.net_weight}  |  {self.material.name} | $({self.net_value})'

    def get_absolute_url(self):
        return reverse('transaction_detail', args=[str(self.id)])



def balance(date, filter_by=None):
    assert isinstance(filter_by, (MaterialGroup, Material)) or filter_by is None

    net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    q_type_in = Q(transaction_type=Transaction.TYPE_IN)
    q_type_out =  Q(transaction_type=Transaction.TYPE_OUT)    
    if isinstance(filter_by, Material):
        q_filter = Q(material=filter_by)
    elif isinstance(filter_by, MaterialGroup):
        q_filter = Q(material__material_group=filter_by)
    else:
        q_filter = Q()
    q_date = Q(transaction_time__lte=date)

    result = Transaction.objects.filter(
        q_type_in & q_filter & q_date
    ).annotate(
            net_weight=net_weight_exp
    ).aggregate(Sum('net_weight'))
    cum_in_to_date = result['net_weight__sum'] or 0
    
    result = Transaction.objects.filter(
        q_type_out & q_filter & q_date
    ).annotate(
            net_weight=net_weight_exp
    ).aggregate(Sum('net_weight'))
    cum_out_to_date = result['net_weight__sum'] or 0
    
    return cum_in_to_date - cum_out_to_date

def sales_and_purchases(date_from, date_to, filter_by=None):
    assert isinstance(filter_by, (MaterialGroup, Material)) or filter_by is None

    net_value_exp = ExpressionWrapper(((F('gross_weight') - F('tare_weight')) * F('unit_price')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    q_type_in = Q(transaction_type=Transaction.TYPE_IN)
    q_type_out =  Q(transaction_type=Transaction.TYPE_OUT)   
    if isinstance(filter_by, Material):
        q_filter = Q(material=filter_by)
    elif isinstance(filter_by, MaterialGroup):
        q_filter = Q(material__material_group=filter_by)
    else:
        q_filter = Q()
    q_date_from = Q(transaction_time__gte=date_from)
    q_date_to = Q(transaction_time__lte=date_to)

    temp_result = Transaction.objects.filter(
        q_filter & q_date_from & q_date_to
    ).annotate(net_value=net_value_exp)
    
    sales = temp_result.filter(q_type_out).aggregate(Sum('net_value'))['net_value__sum'] or 0
    purchases = temp_result.filter(q_type_in).aggregate(Sum('net_value'))['net_value__sum'] or 0
    
    return (sales, -purchases)


def movement_between(transaction_type, date_from, date_to, filter_by=None):
    assert isinstance(filter_by, (MaterialGroup, Material)) or filter_by is None
    assert transaction_type in (Transaction.TYPE_IN, Transaction.TYPE_OUT)
    
    net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    q_type = Q(transaction_type=transaction_type)  
    if isinstance(filter_by, Material):
        q_filter = Q(material=filter_by)
    elif isinstance(filter_by, MaterialGroup):
        q_filter = Q(material__material_group=filter_by)
    else:
        q_filter = Q()
    q_date_from = Q(transaction_time__gte=date_from)
    q_date_to = Q(transaction_time__lte=date_to)
    
    result = Transaction.objects.filter(
        q_type & q_filter & q_date_from & q_date_to
    ).annotate(
            net_weight=net_weight_exp
    ).aggregate(Sum('net_weight'))
    return result['net_weight__sum'] or 0 


def weighted_avg_price(date, filter_by=None):
    assert isinstance(filter_by, (MaterialGroup, Material)) or filter_by is None
    
    net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    q_date_to = Q(transaction_time__lte=date)
    if isinstance(filter_by, Material):
        q_filter = Q(material=filter_by)
    elif isinstance(filter_by, MaterialGroup):
        q_filter = Q(material__material_group=filter_by)
    else:
        q_filter = Q()

    raw = Transaction.objects\
        .filter(q_filter & q_date_to)\
        .annotate(net_weight=net_weight_exp)\
        .order_by('transaction_time')\
        .values('transaction_type', 'net_weight', 'unit_price')

    b = 0   # balance
    p = 0   # price
    wap = 0 # weighted_average_price
    for transaction in raw:
        p = transaction['unit_price'] if transaction['transaction_type'] == Transaction.TYPE_IN else wap
        w = transaction['net_weight'] if transaction['transaction_type'] == Transaction.TYPE_IN else -transaction['net_weight']
        wap = (b * wap + w * p) / (b + w)
        b += w
    
    return wap


def period_weighted_avg_price(transaction_type, date_from, date_to, filter_by=None):
    assert transaction_type in (Transaction.TYPE_IN, Transaction.TYPE_OUT)
    assert isinstance(filter_by, (MaterialGroup, Material)) or filter_by is None
    
    net_weight_exp = ExpressionWrapper((F('gross_weight') - F('tare_weight')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
    q_type = Q(transaction_type=transaction_type)
    q_date_from = Q(transaction_time__gte=date_from)
    q_date_to = Q(transaction_time__lte=date_to)
    if isinstance(filter_by, Material):
        q_filter = Q(material=filter_by)
    elif isinstance(filter_by, MaterialGroup):
        q_filter = Q(material__material_group=filter_by)
    else:
        q_filter = Q()

    raw = Transaction.objects\
        .filter(q_type & q_filter & q_date_from & q_date_to)\
        .annotate(net_weight=net_weight_exp)\
        .order_by('transaction_time')\
        .values('net_weight', 'unit_price')
    try:
        wap = sum([tr['net_weight'] * tr['unit_price'] for tr in raw]) / sum([tr['net_weight'] for tr in raw])
    except ZeroDivisionError:
        wap = 0
    
    return wap