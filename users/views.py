from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from allauth.exceptions import ImmediateHttpResponse
from allauth.account import signals

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


class EmployeeProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class EmployeeCreateView(LoginRequiredMixin, SignupView):
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

    def get_success_url(self):
        if self.request.user.pk == self.kwargs['pk']:
            return reverse_lazy('profile')
        return reverse_lazy('employee_list')
    model = get_user_model()
    context_object_name = 'employee'
    template_name = 'users/employee_delete.html'
    success_url = reverse_lazy('employee_list')
