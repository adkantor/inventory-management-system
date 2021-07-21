from django.urls import path

from .views import (
    TransactionsView, SummaryView, 
    get_transactions, get_summary, get_material_groups, get_materials
)

urlpatterns = [
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('summary/', SummaryView.as_view(), name='summary'),
    # API routes
    path('get-transactions/', get_transactions, name='get_transactions'),
    path('get-summary/', get_summary, name='get_summary'), 
    path('get-material-groups/', get_material_groups, name='get_material_groups'), 
    path('get-materials/<str:material_group_id>', get_materials, name='get_materials'), 
]