# myapp1/views.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from myapp1.models import Idea


class IdeaListView(ListView):
    model = Idea
    context_object_name = 'idea_list'
    template_name = 'myapp1/idea_list.html'


class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'myapp1/idea_detail.html'
