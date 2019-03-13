# movies/forms.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from utils.fields import MultipleChoiceTreeField
from mptt.forms import TreeNodeChoiceField
from .models import Movie, Genre, Director, Category, Actor, RATING_CHOICES


class MovieFilterForm(forms.Form):
	genre = forms.ModelChoiceField(
		label=_("Genre"), required=False, queryset=Genre.objects.all(),
	)
	director = forms.ModelChoiceField(
		label=_("Director"), required=False, queryset=Director.objects.all(),
	)
	actor = forms.ModelChoiceField(
		label=_("Actor"), required=False, queryset=Actor.objects.all(),
	)
	rating = forms.ChoiceField(
		label=_("Rating"), required=False, choices=RATING_CHOICES,
	)
	category = TreeNodeChoiceField(
		label=_("Category"), required=False, queryset=Category.objects.all(),
		level_indicator=mark_safe("&nbsp;&nbsp;&nbsp;&nbsp;"),
	)


class MovieForm(forms.ModelForm):
	categories = MultipleChoiceTreeField(
		label=_("Categories"), required=False, queryset=Category.objects.all(),
	)

	class Meta:
		model = Movie

	def __init__(self, *args, **kwargs):
		super(MovieForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_action = ""
		self.helper.form_method = "POST"
		self.helper.layout = layout.Layout(
			layout.Field("title"),
			layout.Field(
				"categories",
				template="utils/checkbox_select_multiple_tree.html"
			),
			bootstrap.FormActions(
				layout.Submit("submit", _("Save")),
			)
		)
