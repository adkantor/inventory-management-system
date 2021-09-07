from django.contrib import admin

from .models import GoodsReceiptNote, GoodsDispatchNote


class GoodsReceiptNoteAdmin(admin.ModelAdmin):
    list_display = ['grn', 'date', 'vendor']
    ordering = ['-grn']

class GoodsDispatchNoteAdmin(admin.ModelAdmin):
    list_display = ['gdn', 'date', 'customer']
    ordering = ['-gdn']

admin.site.register(GoodsReceiptNote, GoodsReceiptNoteAdmin)
admin.site.register(GoodsDispatchNote, GoodsDispatchNoteAdmin)