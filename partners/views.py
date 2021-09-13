from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .models import Vendor, Customer


# Vendors

class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    context_object_name = 'partner_list'
    template_name = 'partners/partner_list.html'
    ordering = ['name']

class VendorDetailView(LoginRequiredMixin, DetailView):
    model = Vendor
    context_object_name = 'partner'
    template_name = 'partners/partner_detail.html'

class VendorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'partners.add_vendor'
    model = Vendor
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_new.html'

class VendorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'partners.change_vendor'
    model = Vendor
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_edit.html'

class VendorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'partners.delete_vendor'
    model = Vendor
    context_object_name = 'partner'
    template_name = 'partners/partner_delete.html'
    success_url = reverse_lazy('vendor_list')


# Customers

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'partner_list'
    template_name = 'partners/partner_list.html'
    ordering = ['name']
    
class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    context_object_name = 'partner'
    template_name = 'partners/partner_detail.html'

class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'partners.add_customer'
    model = Customer
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_new.html'

class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'partners.change_customer'
    model = Customer
    context_object_name = 'partner'
    fields = ('name', 'country', 'postcode', 'city', 'address', 'tax_number', 'is_private_person', 
              'contact_name', 'contact_phone', 'contact_email',)
    template_name = 'partners/partner_edit.html'

class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'partners.delete_customer'
    model = Customer
    context_object_name = 'partner'
    template_name = 'partners/partner_delete.html'
    success_url = reverse_lazy('customer_list')