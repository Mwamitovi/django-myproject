from django.contrib import admin
from .models import Category, Idea, Like


admin.site.register(Category)
admin.site.register(Idea)
admin.site.register(Like)