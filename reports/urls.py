from django.urls import path

from .views import (TransactionsView, get_transactions, get_material_groups, get_materials)

urlpatterns = [
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    # API routes
    path('get-transactions/', get_transactions, name='get_transactions'), 
    path('get-material-groups/', get_material_groups, name='get_material_groups'), 
    path('get-materials/<str:material_group_id>', get_materials, name='get_materials'), 
]