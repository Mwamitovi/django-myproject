# quotes/forms.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import InspirationalQuote


class InspirationalQuoteForm(forms.ModelForm):
	class Meta:
		model = InspirationalQuote
		fields = ["author", "quote", "picture", "language"]