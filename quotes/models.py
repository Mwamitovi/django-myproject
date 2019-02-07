# quotes/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.core.urlresolvers import reverse, NoReverseMatch
from PIL import Image
from utils.models import UrlMixin


THUMBNAIL_SIZE = getattr(settings, "QUOTES_THUMBNAIL_SIZE", (50, 50))


def upload_to(instance, filename):
    """
    This upload_to() function, sets the path of the uploaded picture
    to be something similar to quotes/2015/04/20150424140000.png.
    As you can see, we use the date timestamp as the filename to ensure its uniqueness.
    We pass this function to the picture image field.
    """
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return "quotes/%s%s" % (now.strftime("%Y/%m/%Y%m%d%H%M%S"), filename_ext.lower(), )


@python_2_unicode_compatible
# class InspirationalQuote(models.Model):
class InspirationalQuote(UrlMixin):
    """
    We use the file storage API (to save different image formats) instead of directly juggling the filesystem,
    as we could then exchange the default storage with Amazon S3 buckets or other
    storage services and the methods will still work.
    """
    author = models.CharField(_("Author"), max_length=200)
    quote = models.TextField(_("Quote"))
    picture = models.ImageField(_("Picture"), upload_to=upload_to, blank=True, null=True, )
    language = models.CharField(_("Language"), max_length=2, blank=True, choices=settings.LANGUAGES)

    class Meta:
        verbose_name = _("Inspirational Quote")
        verbose_name_plural = _("Inspirational Quotes")

    def __str__(self):
        return self.quote

    def save(self, *args, **kwargs):
        super(InspirationalQuote, self).save(*args, **kwargs)
        # generate thumbnail picture version
        self.create_thumbnail()

    def create_thumbnail(self):
        if not self.picture:
            return ""
        file_path = self.picture.name
        filename_base, filename_ext = os.path.splitext(file_path)
        thumbnail_file_path = "%s_thumbnail.jpg" % filename_base
        if storage.exists(thumbnail_file_path):
            # if thumbnail version exists, return its url path
            return "exists"
        try:
            # resize the original image and return URL path of the thumbnail version
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            width, height = image.size

            if width > height:
                delta = width - height
                left = int(delta/2)
                upper = 0
                right = height + left
                lower = height
            else:
                delta = height - width
                left = 0
                upper = int(delta/2)
                right = width
                lower = width + upper

            image = image.crop((left, upper, right, lower))
            image = image.resize(THUMBNAIL_SIZE, Image.ANTIALIAS)

            f_mob = storage.open(thumbnail_file_path, "w")
            image.save(f_mob, "JPEG")
            f_mob.close()
            return "success"
        except storage.DoesNotExist:
            return "error"

    def get_thumbnail_picture_url(self):
        if not self.picture:
            return ""
        file_path = self.picture.name
        filename_base, filename_ext = os.path.splitext(file_path)
        thumbnail_file_path = "%s_thumbnail.jpg" % filename_base
        if storage.exists(thumbnail_file_path):
            # if thumbnail version exists, return its URL path
            return storage.url(thumbnail_file_path)
        # return original as a fallback
        return self.picture.url

    def get_url_path(self):
        try:
            return reverse("quote_detail", kwargs={"id": self.pk})
        except NoReverseMatch:
            return ""

    def title(self):
        return self.quote
