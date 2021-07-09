from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Vendor, Customer


# Vendors

class VendorListView(ListView):
    model = Vendor
    context_object_name = 'partner_list'
    template_name = 'partners/partner_list.html'
    ordering = ['name']

class VendorDetailView(DetailView):
    model = Vendor
    context_object_name = 'partner'
    template_name = 'partners/partner_detail.html'

class VendorCreateView(CreateView):
    model = Vendor
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_new.html'

class VendorUpdateView(UpdateView):
    model = Vendor
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_edit.html'

class VendorDeleteView(DeleteView):
    model = Vendor
    context_object_name = 'partner'
    template_name = 'partners/partner_delete.html'
    success_url = reverse_lazy('vendor_list')


# Customers

class CustomerListView(ListView):
    model = Customer
    context_object_name = 'partner_list'
    template_name = 'partners/partner_list.html'
    ordering = ['name']
    
class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = 'partner'
    template_name = 'partners/partner_detail.html'

class CustomerCreateView(CreateView):
    model = Customer
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_new.html'

class CustomerUpdateView(UpdateView):
    model = Customer
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_edit.html'

class CustomerDeleteView(DeleteView):
    model = Customer
    context_object_name = 'partner'
    template_name = 'partners/partner_delete.html'
    success_url = reverse_lazy('customer_list')