# myapp1/urls.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from myapp1 import views


urlpatterns = [
    url(r'ideas/', views.IdeaListView.as_view(), name='idea_list'),
    url(r'idea/(?P<pk>\d+)$', views.IdeaDetailView.as_view(), name='idea-detail'),
]
