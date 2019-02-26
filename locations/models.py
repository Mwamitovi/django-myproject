# locations/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


def upload_to(instance, filename):
    """
    This upload_to() function, sets the path of the uploaded picture
    to be something similar to location/201504/20150424140000.png.
    As you can see, we use the date timestamp as the filename to ensure its uniqueness.
    We pass this function to the *_image field.
    - Instance is a positional argument to help load more than one image
    """
    now = timezone_now()
    """
    os.path.splitext(path) - splits the pathname path into a pair (root, ext) such that 
    root + ext == path, (ext is empty or begins with a period and contains at most one period).
    Leading periods on the basename are ignored; splitext('.js') returns ('.js', '').
    """
    filename_base, filename_ext = os.path.splitext(filename)
    return "location/%s%s" % (now.strftime("%Y%m/%Y%m%d%H%M%S"), filename_ext.lower(), )


@python_2_unicode_compatible
class Location(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(help_text="A short label, generally used in URLs.")
    small_image = models.ImageField(_("Small Image"), upload_to=upload_to, blank=True, null=True,)
    medium_image = models.ImageField(_("Medium Image"), upload_to=upload_to, blank=True, null=True,)
    large_image = models.ImageField(_("Large Image"), upload_to=upload_to, blank=True, null=True,)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.title
