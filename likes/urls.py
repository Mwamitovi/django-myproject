# likes/urls.py
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from likes import views


urlpatterns = [
    url(r"^(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/$",
        views.json_set_like,
        name="json_set_like"
        ),
]
