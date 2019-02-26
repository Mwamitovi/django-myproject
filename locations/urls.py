# locations/urls.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from locations import views


urlpatterns = [
    url(r'^$', views.LocationListView.as_view(), name='location-list'),
    url(r'^(?P<slug>[^/]+)$', views.LocationDetailView.as_view(), name='location-detail'),
    url(r'^(?P<slug>[^/]+)/popup/$', views.location_detail_popup, name='location-detail-popup'),
]
