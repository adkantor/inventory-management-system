from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

from django import forms
from allauth.account.forms import SignupForm

from django.dispatch import Signal
signup_done = Signal()



class CustomUserCreationForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    profile_picture = forms.ImageField(required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # remove password fields as we start with password reset
        self.fields.pop('password1')
        self.fields.pop('password2')

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        # send signal to reset password
        signup_done.send(sender=self.__class__, instance=user)
        return user        

    def custom_signup(self, request, user):
        # need to override: 
        # allauth looks for ACCOUNT_SIGNUP_FORM_CLASS in settings but
        # we use ACCOUNT_FORMS therefore allauth would use
        # _DummyCustomSignupForm instead CustomUserCreationForm
        custom_form = self
        if hasattr(custom_form, "signup") and callable(custom_form.signup):
            custom_form.signup(request, user)

    def signup(self, request, user):
        # save supplementary fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        e = self.cleaned_data['email']
        user.username = e.split(sep='@')[0]
        user.profile_picture = self.cleaned_data['profile_picture']
        g = Group.objects.get(name=self.cleaned_data['group'])
        user.groups.add(g)
        user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'profile_picture',)