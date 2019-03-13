# utils/fields.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django import forms
from django.utils.translation import get_language
from django.utils.translation import string_concat


class MultilingualCharField(models.CharField):
    """
    Customizing the CharField to auto create model fields
    """
    def __init__(self, verbose_name=None, **kwargs):
        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)
        super(MultilingualCharField, self).__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False, virtual_only=False):
        # generate language specific fields dynamically
        # virtual_only is deprecated in django2
        if not cls._meta.abstract:
            for lang_code, lang_name in settings.LANGUAGES:
                if lang_code == settings.LANGUAGE_CODE:
                    _blank = self._blank
                else:
                    _blank = True

                localized_field = models.CharField(
                    string_concat(self.verbose_name, " (%s)" % lang_code),
                    name=self.name,
                    primary_key=self.primary_key,
                    max_length=self.max_length,
                    unique=self.unique,
                    blank=_blank,
                    null=False,  # we ignore the null argument!
                    db_index=self.db_index,
                    rel=self.rel,
                    default=self.default or "",
                    editable=self._editable,
                    serialize=self.serialize,
                    choices=self.choices,
                    help_text=self.help_text,
                    db_column=None,
                    # db_tablespace=self.db_tablespace, supported for Oracle DB
                )

                localized_field.contribute_to_class(cls, "%s_%s" % (name, lang_code),)

        # self.set_attributes_from_name(name)
        # self.model = cls
        # cls._meta.add_field(self, virtual=True)
        # super(MultilingualCharField, self).contribute_to_class(cls, name, virtual_only=True)

        def translated_value(self):
            language = get_language()
            val = self.__dict__.get("%s_%s" % (name, language))
            if not val:
                val = self.__dict__.get("%s_%s" % (name, settings.LANGUAGE_CODE))
            return val

        setattr(cls, name, property(translated_value))


class MultilingualTextField(models.TextField):

    def __init__(self, verbose_name=None, **kwargs):
        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)
        super(MultilingualTextField, self).__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False, virtual_only=False):
        # generate language specific fields dynamically
        if not cls._meta.abstract:
            for lang_code, lang_name in settings.LANGUAGES:
                if lang_code == settings.LANGUAGE_CODE:
                    _blank = self._blank
                else:
                    _blank = True

                localized_field = models.TextField(
                    string_concat(self.verbose_name, " (%s)" % lang_code),
                    name=self.name,
                    primary_key=self.primary_key,
                    max_length=self.max_length,
                    unique=self.unique,
                    blank=_blank,
                    null=False,  # we ignore the null argument!
                    db_index=self.db_index,
                    rel=self.rel,
                    default=self.default or "",
                    editable=self._editable,
                    serialize=self.serialize,
                    choices=self.choices,
                    help_text=self.help_text,
                    db_column=None,
                    # db_tablespace=self.db_tablespace, supported for Oracle DB
                )

                localized_field.contribute_to_class(cls, "%s_%s" % (name, lang_code),)

        # self.set_attributes_from_name(name)
        # self.model = cls
        # cls._meta.add_field(self, virtual=True)
        # super(MultilingualTextField, self).contribute_to_class(cls, name, virtual_only=True)

        def translated_value(self):
            language = get_language()
            val = self.__dict__.get("%s_%s" % (name, language))
            if not val:
                val = self.__dict__.get("%s_%s" % (name, settings.LANGUAGE_CODE))
            return val

        setattr(cls, name, property(translated_value))


class MultipleChoiceTreeField(forms.ModelMultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def label_from_instance(self, obj):
        return obj
