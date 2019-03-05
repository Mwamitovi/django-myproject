# utils/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
# from django.utils.six.moves.urllib import parse, urlparse, urlunparse
from six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.utils.safestring import mark_safe
# from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.conf import settings
from django.core.exceptions import FieldError
from django.template.defaultfilters import escape


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
    created = models.DateTimeField(_("creation date and time"), editable=False, )
    modified = models.DateTimeField(_("modification date and time"), null=True, editable=False, )

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
    meta_keywords = models.CharField(_("Keywords"), max_length=255, blank=True,
                                     help_text=_("Separate keywords by comma."), )
    meta_description = models.CharField(_("Description"), max_length=255, blank=True, )
    meta_author = models.CharField(_("Author"), max_length=255, blank=True, )
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


def object_relation_mixin_factory(
        prefix=None,
        prefix_verbose=None,
        add_related_name=False,
        limit_content_type_choices_to=None,
        limit_object_choices_to=None,
        is_required=False,
):
    """
    returns a mixin class for generic foreign keys using
    "Content type" and "object Id" with dynamic field names.
    This function is just a class generator with Parameters:
    prefix:
        a prefix, which is added in front of the fields
    prefix_verbose :
        a verbose name of the prefix, used	to generate a title for the field
        column of the content object in the Admin.
    add_related_name :
        a boolean value indicating, that a related name for the generated
        content type foreign key should be added. This value should be true,
        if you use more than one ObjectRelationMixin in your model.
    The model fields are created like this:
        <prefix>_content_type : Field name for the "content type"
        <prefix>_object_id : Field name for the "object Id"
        <prefix>_content_object : Field name for the "content object"
    """
    if limit_content_type_choices_to is None:
        limit_content_type_choices_to = {}
    if limit_object_choices_to is None:
        limit_object_choices_to = {}

    p = ""
    if prefix:
        p = "%s_" % prefix

    content_type_field = "%scontent_type" % p
    object_id_field = "%sobject_id" % p
    content_object_field = "%scontent_object" % p

    class TheClass(models.Model):

        class Meta:
            abstract = True

    if add_related_name:
        if not prefix:
            raise FieldError(
                "if add_related_name is set to True, prefix must be given"
            )
        related_name = prefix
    else:
        related_name = None

    optional = not is_required

    ct_verbose_name = (
        _("%s's type (model)") % prefix_verbose
        if prefix_verbose
        else _("Related object's type (model)")
    )

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=ct_verbose_name,
        related_name=related_name,
        blank=optional,
        null=optional,
        help_text=_("Please select the type (model) for the relation, you want to build."),
        limit_choices_to=limit_content_type_choices_to,
    )

    fk_verbose_name = (prefix_verbose or _("Related	object"))

    object_id = models.CharField(
        fk_verbose_name,
        blank=optional,
        null=False,
        max_length=255,
        default="",  # for south migrations
        help_text=_("Please enter the ID of the related object."),
    )

    object_id.limit_choices_to = limit_object_choices_to
    # can be retrieved by,
    # MyModel._meta.get_field("object_id").limit_choices_to

    content_object = fields.GenericForeignKey(
        ct_field=content_type_field,
        fk_field=object_id_field,
    )

    TheClass.add_to_class(content_type_field, content_type)
    TheClass.add_to_class(object_id_field, object_id)
    TheClass.add_to_class(content_object_field, content_object)

    return TheClass
