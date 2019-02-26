# locations/views.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from locations.models import Location


class LocationListView(ListView):
    model = Location
    context_object_name = 'location_list'
    template_name = 'locations/location_list.html'


class LocationDetailView(DetailView):
    model = Location
    template_name = 'locations/location_detail.html'


def location_detail_popup(request, slug):
    location = get_object_or_404(Location, slug=slug)
    return render(request,
                  "locations/location_detail_popup.html",
                  {"location": location}
                  )
