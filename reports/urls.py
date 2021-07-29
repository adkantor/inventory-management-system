from django.urls import path

from .views import (
    DashboardView, TransactionsView, SummaryView, 
    get_stock_levels, get_weekly_sales_and_purchases, get_summary_sales_and_purchases, get_user_statuses,
    get_summary, get_transactions, get_material_groups, get_materials
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('summary/', SummaryView.as_view(), name='summary'),
    # API routes
    path('get-stock-levels/', get_stock_levels, name='get_stock_levels'), 
    path('get-weekly-financials/', get_weekly_sales_and_purchases, name='get_weekly_financials'), 
    path('get-summary-financials/', get_summary_sales_and_purchases, name='get_summary_financials'), 
    path('get-user-statuses/', get_user_statuses, name='get_user_statuses'), 
    path('get-summary/', get_summary, name='get_summary'), 
    path('get-transactions/', get_transactions, name='get_transactions'),    
    path('get-material-groups/', get_material_groups, name='get_material_groups'), 
    path('get-materials/<str:material_group_id>', get_materials, name='get_materials'), 
]