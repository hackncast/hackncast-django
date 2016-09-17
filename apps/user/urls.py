# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup/$', views.CustomSignupView.as_view(), name="account_signup"),
    url(r"^password/reset/$", views.CustomPasswordResetView.as_view(),
        name="account_reset_password"),
    url(r'^profile/$', views.UserProfileView.as_view(), name="profile"),
]
