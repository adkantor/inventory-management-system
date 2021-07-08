from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Vendor, Customer


# Vendors

class VendorListView(ListView):
    model = Vendor
    context_object_name = 'vendor_list'
    template_name = 'partners/vendor_list.html'
    ordering = ['name']

class VendorDetailView(DetailView):
    model = Vendor
    context_object_name = 'vendor'
    template_name = 'partners/vendor_detail.html'

class VendorCreateView(CreateView):
    model = Vendor
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/vendor_new.html'

class VendorUpdateView(UpdateView):
    model = Vendor
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/vendor_edit.html'

class VendorDeleteView(DeleteView):
    model = Vendor
    template_name = 'partners/vendor_delete.html'
    success_url = reverse_lazy('vendor_list')


# Customers

class CustomerListView(ListView):
    model = Customer
    context_object_name = 'customer_list'
    template_name = 'partners/customer_list.html'
    ordering = ['name']
    
class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'partners/customer_detail.html'

class CustomerCreateView(CreateView):
    model = Customer
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/customer_new.html'

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/customer_edit.html'

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'partners/customer_delete.html'
    success_url = reverse_lazy('customer_list')