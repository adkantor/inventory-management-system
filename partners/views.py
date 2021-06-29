from django.views.generic import ListView, DetailView
from .models import Vendor, Customer

class VendorListView(ListView):
    model = Vendor
    context_object_name = 'vendor_list'
    template_name = 'partners/vendor_list.html'


class VendorDetailView(DetailView):
    model = Vendor
    context_object_name = 'vendor'
    template_name = 'partners/vendor_detail.html'


class CustomerListView(ListView):
    model = Customer
    context_object_name = 'customer_list'
    template_name = 'partners/customer_list.html'


class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'partners/customer_detail.html'