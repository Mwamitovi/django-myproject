# movies/cms_app.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from movies.views import MovieListView


@apphook_pool.register # register the app
class MoviesApphook(CMSApp):
    app_name = "movies"
    name = _("Movies")

    def get_urls(self, page=None, language=None, **kwargs):
        # return ["movies.urls"]
        return [
            url(r'^$', MovieListView.as_view(), name="movie_list"),
        ]


# apphook_pool.register(MoviesApphook)
