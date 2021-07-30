from django.urls import path

from .views import (
    MaterialGroupListView, MaterialGroupDetailView, MaterialGroupCreateView, MaterialGroupUpdateView, MaterialGroupDeleteView, 
    MaterialListView, MaterialDetailView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView,
    # TransactionListView, TransactionDetailView, TransactionDeleteView, 
    # GoodsReceiptCreateView, GoodsDispatchCreateView, GoodsReceiptUpdateView, GoodsDispatchUpdateView
)

urlpatterns = [
    # Material Groups
    path('material_groups', MaterialGroupListView.as_view(), name='material_group_list'),
    path('material_groups/<uuid:pk>', MaterialGroupDetailView.as_view(), name='material_group_detail'),
    path('material_groups/new/', MaterialGroupCreateView.as_view(), name='material_group_new'),
    path('material_groups/<uuid:pk>/edit/', MaterialGroupUpdateView.as_view(), name='material_group_edit'),
    path('material_groups/<uuid:pk>/delete/', MaterialGroupDeleteView.as_view(), name='material_group_delete'),

    # Materials
    path('materials', MaterialListView.as_view(), name='material_list'),
    path('materials/<uuid:pk>', MaterialDetailView.as_view(), name='material_detail'),
    path('materials/new/', MaterialCreateView.as_view(), name='material_new'),
    path('materials/<uuid:pk>/edit/', MaterialUpdateView.as_view(), name='material_edit'),
    path('materials/<uuid:pk>/delete/', MaterialDeleteView.as_view(), name='material_delete'),

    # Transactions
    # path('transactions', TransactionListView.as_view(), name='transaction_list'),
    # path('transactions/<uuid:pk>', TransactionDetailView.as_view(), name='transaction_detail'),
    # path('transactions/goods_receipts/new/', GoodsReceiptCreateView.as_view(), name='goods_receipt_new'),
    # path('transactions/goods_dispatches/new/', GoodsDispatchCreateView.as_view(), name='goods_dispatch_new'),
    # path('transactions/goods_receipts/<uuid:pk>/edit/', GoodsReceiptUpdateView.as_view(), name='goods_receipt_edit'),
    # path('transactions/goods_dispatches/<uuid:pk>/edit/', GoodsDispatchUpdateView.as_view(), name='goods_dispatch_edit'),
    # path('transactions/<uuid:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]