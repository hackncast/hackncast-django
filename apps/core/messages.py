#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from django.contrib import messages


def debug(request, message, data):
    messages.debug(
        request,
        message,
        extra_tags=json.dumps(data),
    )


def info(request, message, data):
    messages.info(
        request,
        message,
        extra_tags=json.dumps(data),
    )


def success(request, message, data):
    messages.success(
        request,
        message,
        extra_tags=json.dumps(data),
    )


def warning(request, message, data):
    messages.warning(
        request,
        message,
        extra_tags=json.dumps(data),
    )


def error(request, message, data):
    messages.error(
        request,
        message,
        extra_tags=json.dumps(data),
    )
