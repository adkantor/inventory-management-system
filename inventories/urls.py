from django.urls import path

from .views import (
    MaterialGroupListView, MaterialGroupDetailView, MaterialGroupCreateView, MaterialGroupUpdateView, MaterialGroupDeleteView, 
    MaterialListView, MaterialDetailView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView,
    TransactionListView, TransactionDetailView, GoodsReceiptCreateView, GoodsDispatchCreateView, TransactionUpdateView, TransactionDeleteView
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
    path('transactions', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<uuid:pk>', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/goods_receipt_new/', GoodsReceiptCreateView.as_view(), name='goods_receipt_new'),
    path('transactions/goods_dispatch_new/', GoodsDispatchCreateView.as_view(), name='goods_dispatch_new'),
    path('transactions/<uuid:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('transactions/<uuid:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]