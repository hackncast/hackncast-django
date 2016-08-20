# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('apps.core.urls')),
    url(r'^user/', include('apps.user.urls')),
]
