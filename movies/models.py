# movies/models.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from utils.models import CreationModificationDateMixin
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey, TreeManyToManyField


RATING_CHOICES = (
    (1, "*"),
    (2, "**"),
    (3, "***"),
    (4, "****"),
    (5, "*****"),
)


@python_2_unicode_compatible
class Genre(models.Model):
    title = models.CharField(_("Title"), max_length=100)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Director(models.Model):
    first_name = models.CharField(_("First name"), max_length=40)
    last_name = models.CharField(_("Last name"), max_length=40)

    def __str__(self):
        return self.first_name + " " + self.last_name


@python_2_unicode_compatible
class Actor(models.Model):
    first_name = models.CharField(_("First name"), max_length=40)
    last_name = models.CharField(_("Last name"), max_length=40)

    def __str__(self):
        return self.first_name + " " + self.last_name


@python_2_unicode_compatible
# class Movie(models.Model):
class Movie(CreationModificationDateMixin):
    title = models.CharField(_("Title"), max_length=255)
    genres = models.ManyToManyField(Genre, blank=True)
    directors = models.ManyToManyField(Director, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    year = models.IntegerField(_("Year Released"), default=2000)
    categories = TreeManyToManyField('Category', verbose_name=_("Categories"))

    def __str__(self):
        return "%s, %s" % (self.title, self.year)

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")


@python_2_unicode_compatible
class Category(MPTTModel, CreationModificationDateMixin):
    parent = TreeForeignKey("self", blank=True, null=True)
    title = models.CharField(_("Title"), max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
