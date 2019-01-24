
# utils/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
# import urlparse
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.template.defaultfilters import escape
from django.utils.safestring import mark_safe


class UrlMixin(models.Model):
	"""
	A replacement for get_absolute_url()
	Models extending this mixin should have either get_url or get_url_path implemented.
	"""
	class Meta:
		abstract = True
	
	
	def get_url(self):
		if hasattr(self.get_url_path, "dont_recurse"):
			raise NotImplementedError
		try:
			path = self.get_url_path()
		except NotImplementedError:
			raise
		website_url = getattr(
			settings, "DEFAULT_WEBSITE_URL",
			"http://127.0.0.1:8000"
		)
		return website_url + path		
	get_url.dont_recurse = True
	
	
	def get_url_path(self):
		if hasattr(self.get_url, "dont_recurse"):
			raise NotImplementedError
		try:
			url = self.get_url()
		except NotImplementedError:
			raise
		# bits = urlparse.urlparse(url)
		# return urlparse.urlunparse(("", "") + bits[2:])
		bits = urlparse(url)
        return urlunparse(("", "") + bits[2:])
	get_url_path.dont_recurse = True
	
	
	def get_absolute_url(self):
		return self.get_url_path()


		
class CreationModificationDateMixin(models.Model):
	"""
	Abstract base class with a creation and modification date and time
	"""
	created = models.DateTimeField(_("creation date and time"),	editable=False,	)
	modified = models.DateTimeField(_("modification date and time"), null=True,	editable=False,	)
	
	def save(self, *args, **kwargs):
		if not self.pk:
			self.created = timezone_now()
		else:
			# To ensure that we have a creation data always, we add this one
		if not self.created:
			self.created = timezone_now()
			self.modified = timezone_now()
			super(CreationModificationDateMixin, self).save(*args, **kwargs)
		save.alters_data = True
		
	class Meta:
		abstract = True
		

		
class MetaTagsMixin(models.Model):
	"""
	Abstract base class for meta tags in the <head> section
	"""
	meta_keywords = models.CharField(_("Keywords"),	max_length=255,	blank=True,	help_text=_("Separate keywords by comma."),	)
	meta_description = models.CharField(_("Description"), max_length=255, blank=True, )
	meta_author = models.CharField(_("Author"),	max_length=255,	blank=True,	)
	meta_copyright = models.CharField(_("Copyright"), max_length=255, blank=True, )
	
	class Meta:
		abstract = True
		
		def get_meta_keywords(self):
			tag = ""
			if self.meta_keywords:
				tag = '<meta name="keywords" content="%s" />\n' % escape(self.meta_keywords)
			return mark_safe(tag)
			
		def get_meta_description(self):
			tag = ""
			if self.meta_description:
				tag = '<meta name="description" content="%s" />\n' % escape(self.meta_description)
			return mark_safe(tag)
			
		def get_meta_author(self):
			tag = ""
			if self.meta_author:
				tag = '<meta name="author" content="%s" />\n' % escape(self.meta_author)
			return mark_safe(tag)
			
		def get_meta_copyright(self):
			tag = ""
			if self.meta_copyright:
				tag = '<meta name="copyright" content="%s" />\n' % escape(self.meta_copyright)
			return mark_safe(tag)
			
		def get_meta_tags(self):
			return mark_safe("".join((
					self.get_meta_keywords(),
					self.get_meta_description(),
					self.get_meta_author(),
					self.get_meta_copyright(),
				))
			)
	
	
	
	
	
	