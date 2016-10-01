#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms

from allauth.account import forms as ac_forms
from captcha.fields import ReCaptchaField

from . import models


class CustomAllauthSignupForm(ac_forms.SignupForm):
    captcha = ReCaptchaField()
    first_name = forms.CharField()

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user


class CustomAllauthResetPasswordForm(ac_forms.ResetPasswordForm):
    captcha = ReCaptchaField()


class PersonalInfoForm(forms.ModelForm):
    pais = forms.ChoiceField(
        label="País", choices=[("", "País")],
    )
    estado = forms.ChoiceField(
        label="Estado", choices=[("", "Estado")],
    )
    cidade = forms.ChoiceField(
        label="Cidade", choices=[("", "Cidade")],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        not_required_fields = self.fields.copy()
        not_required_fields.pop('first_name')
        for fieldname in not_required_fields:
            self.fields[fieldname].required = False
        self.fields['schooling'].empty_label = "Escolha uma escolaridade..."

    class Meta:
        model = models.HNCUser
        fields = [
            'first_name', 'last_name', 'birthdate', 'country', 'region',
            'city', 'sex', 'schooling', 'profession', 'occupation',
        ]
