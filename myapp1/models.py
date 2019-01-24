
# myapps1/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from utils.models import UrlMixin
from utils.models import CreationModificationMixin
from utils.models import MetaTagsMixin


@python_2_unicode_compatible
class Idea(UrlMixin, CreationModificationMixin, MetaTagsMixin):
	title = models.CharField(_("Title"), max_length=200)
	content = models.TextField(_("Content"))

	class Meta:
		verbose_name = _("Idea")
		verbose_name_plural = _("Ideas")

	def __str__(self):
		return self.title
		
	get_url_path(self):
		return reverse("idea_details", kwargs={ "idea_id": str(self.pk),} )


