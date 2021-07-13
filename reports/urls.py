from django.urls import path

from .views import (TransactionsView, get_transactions)

urlpatterns = [
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    # API routes
    path('transactions/get', get_transactions, name='get_transactions'), 
]