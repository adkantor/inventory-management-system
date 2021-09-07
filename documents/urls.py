from django.urls import path

from .views import (
    GoodsReceiptNoteListView, GoodsReceiptNoteDetailView, GoodsReceiptNoteCreateView, GoodsReceiptNoteUpdateView, GoodsReceiptNoteDeleteView,
    GoodsDispatchNoteListView, GoodsDispatchNoteDetailView, GoodsDispatchNoteCreateView, GoodsDispatchNoteUpdateView, GoodsDispatchNoteDeleteView,
    goods_receipt_note_display_pdf, goods_receipt_note_generate_pdf, goods_dispatch_note_display_pdf, goods_dispatch_note_generate_pdf
)

urlpatterns = [
    # Goods Receipt Notes
    path('goods_receipt_notes/', GoodsReceiptNoteListView.as_view(), name='goods_receipt_note_list'),
    path('goods_receipt_notes/<uuid:pk>', GoodsReceiptNoteDetailView.as_view(), name='goods_receipt_note_detail'),
    path('goods_receipt_notes/new/', GoodsReceiptNoteCreateView.as_view(), name='goods_receipt_note_new'),
    path('goods_receipt_notes/<uuid:pk>/edit/', GoodsReceiptNoteUpdateView.as_view(), name='goods_receipt_note_edit'),
    path('goods_receipt_notes/<uuid:pk>/delete/', GoodsReceiptNoteDeleteView.as_view(), name='goods_receipt_note_delete'),
    path('goods_receipt_notes/<uuid:pk>/pdf/', goods_receipt_note_display_pdf, name='goods_receipt_note_pdf'),
    path('goods_receipt_notes/generate/<uuid:pk>', goods_receipt_note_generate_pdf, name='goods_receipt_note_generate'),
    # Goods Dispatch Notes
    path('goods_dispatch_notes/', GoodsDispatchNoteListView.as_view(), name='goods_dispatch_note_list'),
    path('goods_dispatch_notes/<uuid:pk>', GoodsDispatchNoteDetailView.as_view(), name='goods_dispatch_note_detail'),
    path('goods_dispatch_notes/new/', GoodsDispatchNoteCreateView.as_view(), name='goods_dispatch_note_new'),
    path('goods_dispatch_notes/<uuid:pk>/edit/', GoodsDispatchNoteUpdateView.as_view(), name='goods_dispatch_note_edit'),
    path('goods_dispatch_notes/<uuid:pk>/delete/', GoodsDispatchNoteDeleteView.as_view(), name='goods_dispatch_note_delete'),
    path('goods_dispatch_notes/<uuid:pk>/pdf/', goods_dispatch_note_display_pdf, name='goods_dispatch_note_pdf'),
    path('goods_dispatch_notes/generate/<uuid:pk>', goods_dispatch_note_generate_pdf, name='goods_dispatch_note_generate'),
]