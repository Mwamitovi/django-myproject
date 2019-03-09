# movies/urls.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from django.shortcuts import redirect
from movies.views import MovieListView


urlpatterns = (
    url(r'^$', MovieListView.as_view(), name="movie_list"),
    # url(r"^$", lambda request: redirect("featured_movie_list")),
    url(r"^editors-picks/$",
        "movie_list", {"featured": True},
        name='featured_movie_list'
        ),
    url(r"^commercial/$",
        "movie_list", {"commercial": True},
        name="commercial_movie_list"
        ),
    url(r"^independent/$",
        "movie_list", {"independent": True},
        name="independent_movie_list"
        ),
    url(r"^(?P<slug>[^/]+)/$",
        "movie_detail",
        name="movie_detail"
        ),
    )
