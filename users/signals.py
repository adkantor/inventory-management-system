from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from allauth.account.views import PasswordResetView

from .forms import CustomUserCreationForm
from .forms import signup_done


@receiver(signup_done, sender=CustomUserCreationForm)
def send_reset_password_email(sender, instance, **kwargs):

    # First create a post request to pass to the view
    request = HttpRequest()
    request.method = 'POST'

    # add the absolute url to be be included in email
    if settings.DEBUG:
        request.META['HTTP_HOST'] = '127.0.0.1:8000'
    else:
        request.META['HTTP_HOST'] = 'www.mysite.com'

    # pass the post form data
    request.POST = {
        'email': instance.email,
        'csrfmiddlewaretoken': get_token(HttpRequest())
    }

    PasswordResetView.as_view()(request)  # email will be sent!