# myapps1/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from utils.models import UrlMixin, CreationModificationDateMixin, MetaTagsMixin, object_relation_mixin_factory
from utils.fields import MultilingualCharField
from utils.fields import MultilingualTextField


@python_2_unicode_compatible
class Category(models.Model):
	title = models.CharField(_("Title"), max_length=200 )
	
	def __str__(self):
		return self.title



@python_2_unicode_compatible
class Idea(UrlMixin, CreationModificationDateMixin, MetaTagsMixin):
	# title = models.CharField(_("Title"), max_length=200)
	title = MultilingualCharField(_("Title"), max_length=200,)
	# content = models.TextField(_("Content"))
	description = MultilingualTextField(_("Description"), blank=True,)
	categories = models.ManyToManyField(Category, verbose_name=_("Categories"), blank=True, related_name="ideas", )

	class Meta:
		verbose_name = _("Idea")
		verbose_name_plural = _("Ideas")

	def __str__(self):
		return self.title

	def get_url_path(self):
		return reverse("idea_details", kwargs={ "idea_id": str(self.pk),} )



FavoriteObjectMixin = object_relation_mixin_factory(is_required=True,)



OwnerMixin = object_relation_mixin_factory(
	prefix="owner",
	prefix_verbose=_("Owner"),
	add_related_name=True,
	limit_content_type_choices_to={ 'model__in': ('user', 'institution') },
	is_required=True,
)



@python_2_unicode_compatible
class Like(FavoriteObjectMixin, OwnerMixin):
	class Meta:
		verbose_name = _("Like")
		verbose_name_plural = _("Likes")

	def __str__(self):
		return _("%(owner)s likes %(obj)s") % { "owner": self.owner_content_object, "obj": self.content_object, }


