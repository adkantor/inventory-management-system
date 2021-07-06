import datetime

import uuid
from django.db import models
from django.urls import reverse

from partners.models import Vendor, Customer

def get_deleted_vendor():
    return Vendor.objects.get_or_create(name='deleted')[0].id

class GoodsReceiptNote(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    grn = models.CharField(max_length=11, blank=True) # format: yyyy/xxxxxx
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
        return GoodsReceiptNote.objects.filter(grn__startswith=year_string).order_by('grn').last()

    @staticmethod
    def get_next_grn(year, last_grn):
        suffix = int(last_grn.grn[5:]) + 1 if last_grn else 1
        return f'{str(year)}/{str(suffix).zfill(6)}'

    def save(self, *args, **kwargs):
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