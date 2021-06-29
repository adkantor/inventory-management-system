from django.urls import path

from .views import VendorListView, VendorDetailView, CustomerListView, CustomerDetailView

urlpatterns = [
    path('vendors', VendorListView.as_view(), name='vendor_list'),
    path('vendors/<uuid:pk>', VendorDetailView.as_view(), name='vendor_detail'),
    path('customers', CustomerListView.as_view(), name='customer_list'),
    path('customers/<uuid:pk>', CustomerDetailView.as_view(), name='customer_detail'),
]