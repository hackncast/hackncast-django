# -*- coding: utf-8 -*-

import jinja2

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.storage import staticfiles_storage


@jinja2.contextfunction
def get_messages(context, *args, **kwargs):
    return messages.get_messages(context['request'])

def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'messages': get_messages,
    })
    })
    return env
