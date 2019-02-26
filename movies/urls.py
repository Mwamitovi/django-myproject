# movies/urls.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from .views import MovieListView


urlpatterns = (
    url(r'^$', MovieListView.as_view(), name="movie_list"),
)
