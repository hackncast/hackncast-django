from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

from allauth.account.views import PasswordResetView, SignupView

from apps.core import messages
from .. import forms


class CustomSignupView(SignupView):
    form_class = forms.CustomAllauthSignupForm


class CustomPasswordResetView(PasswordResetView):
    form_class = forms.CustomAllauthResetPasswordForm


class PersonalInfoView(FormView):
    template_name = "user/profile.jinja"
    form_class = forms.PersonalInfoForm
    success_url = reverse_lazy('user:profile')

    def get_form_kwargs(self):
        if self.request.POST:
            return {'data': self.request.POST or None}
        return {'instance': self.request.user}

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        data['city_id'] = data.pop('city')
        data['region_id'] = data.pop('region')
        data['country_id'] = data.pop('country')
        self.request.user.update(**data)
        self.request.user.save()
        messages.success(self.request, "Perfil atualizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Desculpe, este formulário contém erros!")
        return super().form_invalid(form)
