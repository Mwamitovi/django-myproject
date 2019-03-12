# movies/admin.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt_tree_editor.admin import TreeEditor
from .models import Actor, Director, Genre, Movie, Category


admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Movie)


# Extending django-mptt-admin
# class CategoryAdmin(DjangoMpttAdmin):
#     list_display = ["title", "created", "modified"]
#     list_filter = ["created"]


# Extending django-mptt-tree-editor
class CategoryAdmin(TreeEditor):
    list_display = ["indented_short_title", "actions_column", "created", "modified"]
    list_filter = ["created"]


admin.site.register(Category, CategoryAdmin)
