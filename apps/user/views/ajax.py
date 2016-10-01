import json

from django.http import Http404
from django.http import HttpResponse
from django.views.generic import View

from apps.core import models


class BaseAJAXQueryView(View):
    query_arg = 'query'
    required_query_args = []
    model = None

    def parse_query_args(self, request):
        args = {}
        args[self.query_arg] = request.GET.get(self.query_arg, None)
        for key in self.required_query_args:
            value = request.GET.get(key, None)
            if value is None:
                raise Http404

            try:
                value = int(value)
            except ValueError:
                raise Http404

            args[key] = value
        return args

    def get_queryset(self, query_args):
        return self.model.objects

    def main_filter(self, queryset, value):
        raise NotImplemented

    def queryset_to_dict(self, queryset):
        raise NotImplemented

    def get(self, request, *args, **kwawrgs):
        query_args = self.parse_query_args(request)
        queryset = self.get_queryset(query_args)
        queryset = self.main_filter(queryset, query_args[self.query_arg])
        objects = self.queryset_to_dict(queryset)
        return HttpResponse(json.dumps({
            'success': True,
            'results': objects
        }), content_type='application/json')


class GenericLocationAJAXQueryView(BaseAJAXQueryView):
    def main_filter(self, queryset, value):
        if value:
            queryset = queryset.filter(name_pt__icontains=value)
        return queryset

    def queryset_to_dict(self, queryset):
        objects = queryset.values('id', 'name_pt')
        objects = [({
            "name": o['name_pt'],
            "text": o['name_pt'],
            "value": o['id'],
        }) for o in objects]
        return objects


class CountryQueryView(GenericLocationAJAXQueryView):
    model = models.Country


class RegionQueryView(GenericLocationAJAXQueryView):
    model = models.Region
    required_query_args = ['country']

    def get_queryset(self, query_args):
        return self.model.objects.filter(country_id=query_args['country'])


class CityQueryView(GenericLocationAJAXQueryView):
    model = models.City
    required_query_args = ['region']

    def get_queryset(self, query_args):
        return self.model.objects.filter(region_id=query_args['region'])


class ProfessionQueryView(BaseAJAXQueryView):
    model = models.Profession

    def main_filter(self, queryset, value):
        if value:
            queryset = queryset.filter(name__icontains=value)
        return queryset

    def queryset_to_dict(self, queryset):
        objects = queryset.values('id', 'name')
        objects = [({
            "name": o['name'],
            "text": o['name'],
            "value": o['id'],
        }) for o in objects]
        return objects
