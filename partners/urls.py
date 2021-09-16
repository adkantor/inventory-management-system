from django.urls import path

from .views import (
    VendorListView, VendorDetailView, VendorCreateView, VendorUpdateView, VendorDeleteView, 
    CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,
)

urlpatterns = [
    # Vendors
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/<uuid:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('vendors/new/', VendorCreateView.as_view(), name='vendor_new'),
    path('vendors/<uuid:pk>/edit/', VendorUpdateView.as_view(), name='vendor_edit'),
    path('vendors/<uuid:pk>/delete/', VendorDeleteView.as_view(), name='vendor_delete'),
    
    # Customers
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/new/', CustomerCreateView.as_view(), name='customer_new'),
    path('customers/<uuid:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('customers/<uuid:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
]