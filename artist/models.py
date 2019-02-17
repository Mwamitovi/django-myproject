# artists/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


STATUS_CHOICES = (
    ("draft", _("Draft")),
    ("published", _("Published"))
)


@python_2_unicode_compatible
class ArtistManager(models.Manager):
    def random_published(self):
        return self.filter(status="published").order_by("?")


@python_2_unicode_compatible
class Artist(models.Model):
    # ...
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES)
    custom_manager = ArtistManager()
