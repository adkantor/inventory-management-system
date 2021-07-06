from django.urls import path

from .views import (
    GoodsReceiptNoteCreateView, GoodsReceiptNoteListView, GoodsReceiptNoteDetailView
)

urlpatterns = [
    # Goods Receipt Notes
    path('goods_receipt_notes/', GoodsReceiptNoteListView.as_view(), name='goods_receipt_note_list'),
    path('goods_receipt_notes/<uuid:pk>', GoodsReceiptNoteDetailView.as_view(), name='goods_receipt_note_detail'),
    path('goods_receipt_notes/new/', GoodsReceiptNoteCreateView.as_view(), name='goods_receipt_note_new'),
    # path('goods_receipt_notes/<uuid:pk>/edit/', MaterialGroupUpdateView.as_view(), name='goods_receipt_note_edit'),
    # path('goods_receipt_notes/<uuid:pk>/delete/', MaterialGroupDeleteView.as_view(), name='goods_receipt_note_delete'),

]