from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from allauth.account.views import SignupView
from allauth.exceptions import ImmediateHttpResponse
from allauth.account import signals

from .forms import UserCreationForm, UserChangeForm

class EmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.can_view_all_users')
    model = get_user_model()
    context_object_name = 'employee_list'
    template_name = 'users/employee_list.html'
    ordering = ['last_name']

class EmployeeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('users.can_view_all_users')
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_detail.html'


# class EmployeeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = get_user_model()
#     context_object_name = 'employee'
#     template_name = 'users/employee_detail.html'

#     def test_func(self):
#         can_view_all_users = self.request.user.has_perm('users.can_view_all_users')
#         can_view_itself_only = (
#             self.request.user.has_perm('users.can_view_itself_only')
#             and self.request.user.pk == self.kwargs['pk']
#         )
        
#         return can_view_all_users or can_view_itself_only

class EmployeeProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SignupView):
    permission_required = ('users.can_add_user')
    success_url = reverse_lazy('employee_list')
    
    def form_valid(self, form):
        # override method to prevent logging in as the newly created user
        self.user = form.save(self.request)
        try:
            signals.user_signed_up.send(
                sender=self.user.__class__,
                request=self.request,
                user=self.user, 
                **{}
            )            
            return HttpResponseRedirect(self.get_success_url())

        except ImmediateHttpResponse as e:
            return e.response


class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_edit.html'
    fields = ('first_name', 'last_name', 'profile_picture')

    def get_form(self, form_class=None):
        form = super(EmployeeUpdateView, self).get_form(form_class)
        return form

    def get_success_url(self):
        if self.request.user.pk == self.kwargs['pk']:
            return reverse_lazy('profile')
        return reverse_lazy('employee_list')

    def test_func(self):
        can_update_all_users = self.request.user.has_perm('users.can_view_all_users')
        can_update_itself = ( self.request.user.pk == self.kwargs['pk'] )        
        return can_update_all_users or can_update_itself


class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_delete.html'
    success_url = reverse_lazy('employee_list')

    def test_func(self):
        can_delete_all_users = self.request.user.has_perm('users.can_delete_all_users')
        is_another_user = ( self.request.user.pk != self.kwargs['pk'] )
        return can_delete_all_users and is_another_user
