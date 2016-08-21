# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^', include('apps.core.urls')),
    url(r'^login/$',
        RedirectView.as_view(url=reverse_lazy('account_login'))),
    url(r'^logout/$',
        RedirectView.as_view(url=reverse_lazy('account_logout'))),
    url(r'^signup/$',
        RedirectView.as_view(url=reverse_lazy('account_signup'))),
    url(r'^user/', include('apps.user.urls')),
]
