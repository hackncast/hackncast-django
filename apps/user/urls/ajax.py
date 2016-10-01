# -*- coding: utf-8 -*-

from django.conf.urls import url

from ..views import ajax

urlpatterns = [
    url(r'^country/$', ajax.CountryQueryView.as_view(), name="ajax-contry"),
    url(r'^region/$', ajax.RegionQueryView.as_view(), name="ajax-region"),
    url(r'^city/$', ajax.CityQueryView.as_view(), name="ajax-city"),
    url(r'^profession/$', ajax.ProfessionQueryView.as_view(), name="ajax-profession"),
]
