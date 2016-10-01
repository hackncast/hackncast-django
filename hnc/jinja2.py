# -*- coding: utf-8 -*-

import json
import types
import jinja2

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage

from allauth.socialaccount import providers
from allauth.socialaccount.templatetags import socialaccount
from allauth.utils import get_request_param


def get_providers():
    return sorted(socialaccount.get_providers(), key=lambda x: x.id)


@jinja2.contextfunction
def provider_login_url(context, provider_id, **kwargs):
    provider = providers.registry.by_id(provider_id)
    query = kwargs
    request = context['request']
    auth_params = query.get('auth_params', None)
    scope = query.get('scope', None)
    process = query.get('process', None)

    if not scope and 'scope' in query:
        del query['scope']

    if not process and 'process' in query:
        del query['process']

    if not auth_params and 'auth_params' in query:
        del query['auth_params']

    if 'next' not in query:
        _next = get_request_param(request, 'next')
        if _next:
            query['next'] = _next
        elif process == 'redirect':
            query['next'] = request.get_full_path()
    else:
        if not query['next']:
            del query['next']
    return provider.get_login_url(request, **query)


def get_inactive_providers(form, all_providers):
    all_providers_map = {}
    for provider in all_providers:
        all_providers_map[provider.id] = provider

    activer_providers_ids = [account.provider for account in form.accounts]

    inactive_providers = []
    for key in all_providers_map:
        if key not in activer_providers_ids:
            inactive_providers.append(all_providers_map[key])
    return inactive_providers


@jinja2.contextfunction
def get_messages(context, *args, **kwargs):
    msg = messages.get_messages(context['request'])
    return msg


def split(text, slice, delimiter=" "):
    return text.split(delimiter)[slice]


def set_attr(field, **attributes):
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        for key, new_value in attributes.items():
            old_value = attrs.get(key, '')
            attrs[key] = (' '.join([old_value, new_value])).strip()
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


def to_json(value):
    return mark_safe(json.dumps(value))


def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'messages': get_messages,
        'get_providers': get_providers,
        'provider_login_url': provider_login_url,
        'get_inactive_providers': get_inactive_providers,
    })
    env.filters.update({
        'split': split,
        'set_attr': set_attr,
        'json': to_json,
    })
    return env
