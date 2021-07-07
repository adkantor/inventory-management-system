import datetime

import uuid
from django.db import models
from django.urls import reverse

from partners.models import Vendor, Customer

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

    def __str__(self):
        return f'{self.gdn} | {self.date} | {self.customer}'

    def get_absolute_url(self):
        return reverse('goods_dispatch_note_detail', args=[str(self.id)])