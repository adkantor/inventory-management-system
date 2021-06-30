from django.urls import path

from .views import (
    MaterialGroupListView, 
    MaterialGroupDetailView, 
    MaterialListView, 
    MaterialDetailView,
    TransactionListView,
    TransactionDetailView)

urlpatterns = [
    path('material_groups', MaterialGroupListView.as_view(), name='material_group_list'),
    path('material_groups/<uuid:pk>', MaterialGroupDetailView.as_view(), name='material_group_detail'),
    path('materials', MaterialListView.as_view(), name='material_list'),
    path('materials/<uuid:pk>', MaterialDetailView.as_view(), name='material_detail'),
    path('transactions', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<uuid:pk>', TransactionDetailView.as_view(), name='transaction_detail'),
]