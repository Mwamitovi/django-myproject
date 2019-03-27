# bulletin_board/views.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from .models import Bulletin
from .serializers import BulletinSerializer


class RESTBulletinList(generics.ListCreateAPIView):
    queryset = Bulletin.objects.all()
    serializer_class = BulletinSerializer


class RESTBulletinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bulletin.objects.all()
    serializer_class = BulletinSerializer
