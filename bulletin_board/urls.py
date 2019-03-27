# bulletin_board/urls.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import *
from .feeds import BulletinFeed
# from bulletin_board import views


# urlpatterns = [
#     url(r"^$", "bulletin_list", name="bulletin_list"),
#     url(r"^(?P<bulletin_id>[0-9]+)/$", "bulletin_detail", name="bulletin_detail"),
#     url(r"^rss/$", BulletinFeed(), name="bulletin_rss"),
# ]
