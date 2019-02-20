# locations/views.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from locations.models import Location


class LocationListView(ListView):
    model = Location
    context_object_name = 'location_list'
    template_name = 'locations.html'


class LocationDetailView(DetailView):
    model = Location
    template_name = 'location/location_detail.html'
