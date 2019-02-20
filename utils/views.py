# utils/views.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.decorators.cache import cache_control


@cache_control(public=True)
def render_js(request, cache=True, *args, **kwargs):
    response = render(request, *args, **kwargs)
    response["Content-Type"] = "application/javascript; charset=UTF-8"
    if cache:
        now = datetime.utcnow()
        response["Last-Modified"] = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        # cache in the browser for 1 month
        expires = now + timedelta(days=31)
        response["Expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    else:
        response["Pragma"] = "No-Cache"
    return response
