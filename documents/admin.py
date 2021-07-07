from django.contrib import admin

from .models import GoodsReceiptNote, GoodsDispatchNote

admin.site.register(GoodsReceiptNote)
admin.site.register(GoodsDispatchNote)