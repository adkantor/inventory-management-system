import datetime
import uuid
from io import BytesIO
import pytz

from django.conf import settings
from django.core.files import File
from django.db import models
from django.urls import reverse
from django.db.models.expressions import F, ExpressionWrapper
from django.db.models.aggregates import Sum

from partners.models import Vendor, Customer
from .render import Render

tz = pytz.timezone(settings.TIME_ZONE)


def get_deleted_vendor():
    return Vendor.objects.get_or_create(name='deleted')[0].id

def get_deleted_customer():
    return Customer.objects.get_or_create(name='deleted')[0].id


class GoodsReceiptNote(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    grn = models.CharField(max_length=14, blank=True) # format: GRNyyyy/xxxxxx
    date = models.DateField()
    print_date = models.DateTimeField(blank=True, null=True)
    vendor = models.ForeignKey(
            Vendor,
            related_name='goods_receipt_notes',
            on_delete=models.SET(get_deleted_vendor),
            )
    notes = models.TextField(max_length=255, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    pdf = models.FileField(upload_to='goods_receipt_notes/', null=True, blank=True)

    @property
    def vendor_name(self):
        return self.vendor.name if self.vendor else None  

    @property
    def total_net_value(self):
        net_value_exp = ExpressionWrapper(((F('gross_weight') - F('tare_weight')) * F('unit_price')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
        temp_result = self.transactions.all().annotate(net_value=net_value_exp)       
        result = temp_result.aggregate(Sum('net_value'))['net_value__sum'] or 0       
        return round(result, 2)


    @staticmethod
    def get_last_grn(year):
        year_string = str(year)
        return GoodsReceiptNote.objects.filter(grn__startswith=f'GRN{year_string}').order_by('grn').last()

    @staticmethod
    def get_next_grn(year, last_grn):
        suffix = int(last_grn.grn[8:]) + 1 if last_grn else 1
        return f'GRN{str(year)}/{str(suffix).zfill(6)}'

    def save(self, *args, **kwargs):
        if not self.grn:
            # update grn -> get next unique id
            current_year = datetime.date.today().year
            last_grn = GoodsReceiptNote.get_last_grn(current_year)
            next_grn = GoodsReceiptNote.get_next_grn(current_year, last_grn)
            self.grn = next_grn
        super(GoodsReceiptNote, self).save(*args, **kwargs)

    def generate_pdf(self):
        context = {'goods_movement_note': self}
        # we have to add print date before generating pdf so that it appear on the pdf
        self.print_date = tz.localize(datetime.datetime.now())
        self.save()
        # generate pdf file
        pdf = Render.render('documents/goods_receipt_note_pdf.html', context)
        filename = f'{str(self.id)}.pdf'
        self.pdf.save(filename, File(BytesIO(pdf.content)))

    def serialize(self):
        return {
            'id': str(self.id),
            'grn': self.grn,
            'date': self.date.strftime('%Y-%m-%d'),
            'print_date': self.print_date.strftime('%Y-%m-%d %H:%M'),
            'vendor': self.vendor.name,
            'notes': self.notes,
            'pdf_url': self.pdf.url
        }

    def __str__(self):
        return f'{self.grn} | {self.date} | {self.vendor}'

    def get_absolute_url(self):
        return reverse('goods_receipt_note_detail', args=[str(self.id)])


class GoodsDispatchNote(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    gdn = models.CharField(max_length=14, blank=True) # format: GDNyyyy/xxxxxx
    date = models.DateField()
    print_date = models.DateTimeField(blank=True, null=True)
    customer = models.ForeignKey(
            Customer,
            related_name='goods_dispatch_notes',
            on_delete=models.SET(get_deleted_customer),
            )
    notes = models.TextField(max_length=255, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    pdf = models.FileField(upload_to='goods_dispatch_notes/', null=True, blank=True)

    @property
    def customer_name(self):
        return self.customer.name if self.customer else None     

    @property
    def total_net_value(self):
        net_value_exp = ExpressionWrapper(((F('gross_weight') - F('tare_weight')) * F('unit_price')), output_field=models.DecimalField(max_digits=7, decimal_places=2))
        temp_result = self.transactions.all().annotate(net_value=net_value_exp)
        result = temp_result.aggregate(Sum('net_value'))['net_value__sum'] or 0       
        return round(result, 2)

    @staticmethod
    def get_last_gdn(year):
        year_string = str(year)
        return GoodsDispatchNote.objects.filter(gdn__startswith=f'GDN{year_string}').order_by('gdn').last()

    @staticmethod
    def get_next_gdn(year, last_gdn):
        suffix = int(last_gdn.gdn[8:]) + 1 if last_gdn else 1
        return f'GDN{str(year)}/{str(suffix).zfill(6)}'

    def save(self, *args, **kwargs):
        if not self.gdn:
            # update gdn -> get next unique id
            current_year = datetime.date.today().year
            last_gdn = GoodsDispatchNote.get_last_gdn(current_year)
            next_gdn = GoodsDispatchNote.get_next_gdn(current_year, last_gdn)
            self.gdn = next_gdn
        super(GoodsDispatchNote, self).save(*args, **kwargs)

    def generate_pdf(self):
        context = {'goods_movement_note': self}
        # we have to add print date before generating pdf so that it appear on the pdf
        self.print_date = tz.localize(datetime.datetime.now())
        self.save()
        # generate pdf file
        pdf = Render.render('documents/goods_dispatch_note_pdf.html', context)
        filename = f'{str(self.id)}.pdf'
        self.pdf.save(filename, File(BytesIO(pdf.content)))

    def serialize(self):
        return {
            'id': str(self.id),
            'gdn': self.gdn,
            'date': self.date.strftime('%Y-%m-%d'),
            'print_date': self.print_date.strftime('%Y-%m-%d %H:%M'),
            'customer': self.customer.name,
            'notes': self.notes,
            'pdf_url': self.pdf.url
        }

    def __str__(self):
        return f'{self.gdn} | {self.date} | {self.customer}'

    def get_absolute_url(self):
        return reverse('goods_dispatch_note_detail', args=[str(self.id)])
