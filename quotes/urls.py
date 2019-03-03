# quotes/urls.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from quotes import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<quote_id>\d+)/download/$',
        views.download_quote_picture,
        name="download_quote_picture"
        ),
    url(r"^ajax-upload/$",
        views.ajax_uploader,
        name="ajax_uploader"
        ),
]
