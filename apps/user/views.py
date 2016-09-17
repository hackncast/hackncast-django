from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy

from allauth.account.views import PasswordResetView, SignupView

from . import models
from . import forms


class CustomSignupView(SignupView):
    form_class = forms.CustomAllauthSignupForm


class CustomPasswordResetView(PasswordResetView):
    form_class = forms.CustomAllauthResetPasswordForm


