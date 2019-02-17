# search/multilingual_whoosh_backend.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.utils import translation
from haystack.backends.whoosh_backend import \
    WhooshSearchBackend, WhooshSearchQuery, WhooshEngine
from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from django.utils.encoding import python_2_unicode_compatible


# noinspection PyAbstractClass
@python_2_unicode_compatible
class MultilingualWhooshSearchBackend(WhooshSearchBackend):
    def update(self, index, iterable, commit=True, language_specific=False):
        if not language_specific and self.connection_alias == "default":
            current_language = (translation.get_language() or settings.LANGUAGE_CODE)[:2]
            for lang_code, lang_name in settings.LANGUAGES:
                using = "default_%s" % lang_code
                translation.activate(lang_code)
                backend = connections[using].get_backend()
                backend.update(index, iterable, commit, language_specific=True)
                translation.activate(current_language)
        elif language_specific:
            super(MultilingualWhooshSearchBackend, self).update(index, iterable, commit)


@python_2_unicode_compatible
class MultilingualWhooshSearchQuery(WhooshSearchQuery):
    def __init__(self, using=DEFAULT_ALIAS):
        self.lang_code = translation.get_language()# [:2]
        self._using = "default_%s" % self.lang_code
        super(MultilingualWhooshSearchQuery, self).__init__(using)


@python_2_unicode_compatible
class MultilingualWhooshEngine(WhooshEngine):
    backend = MultilingualWhooshSearchBackend
    query = MultilingualWhooshSearchQuery
