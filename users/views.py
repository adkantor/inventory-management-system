from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import UserCreationForm, UserChangeForm

class EmployeeListView(ListView):
    model = get_user_model()
    context_object_name = 'employee_list'
    template_name = 'users/employee_list.html'
    ordering = ['last_name']

class EmployeeDetailView(DetailView):
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_detail.html'

class EmployeeCreateView(CreateView):
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_new.html'
    fields = ('first_name', 'last_name', 'username', 'email', 'profile_picture')
    success_url = reverse_lazy('employee_list')

    def get_form(self, form_class=None):
        form = super(EmployeeCreateView, self).get_form(form_class)
        form.fields['email'].required = True
        return form


class EmployeeUpdateView(UpdateView):
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_edit.html'
    fields = ('first_name', 'last_name', 'username', 'email', 'profile_picture')
    success_url = reverse_lazy('employee_list')

    def get_form(self, form_class=None):
        form = super(EmployeeUpdateView, self).get_form(form_class)
        form.fields['email'].required = True
        return form

class EmployeeDeleteView(DeleteView):
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_delete.html'
    success_url = reverse_lazy('employee_list')
