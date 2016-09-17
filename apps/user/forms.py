#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms

from allauth.account import forms as ac_forms
from captcha.fields import ReCaptchaField


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
