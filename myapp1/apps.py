# myapp1/apps.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Myapp1AppConfig(AppConfig):
    name = "myapp1"
    verbose_name = _("Myapp1")

    def ready(self):
        from . import signals