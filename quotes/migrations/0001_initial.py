# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-01-31 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import quotes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InspirationalQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200, verbose_name='Author')),
                ('quote', models.TextField(verbose_name='Quote')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=quotes.models.upload_to, verbose_name='Picture')),
                ('language', models.CharField(blank=True, choices=[('en', 'English'), ('de', 'Deutsch'), ('fr', 'Français'), ('sw', 'Swahili')], max_length=2, verbose_name='Language')),
            ],
            options={
                'verbose_name': 'Inspirational Quote',
                'verbose_name_plural': 'Inspirational Quotes',
            },
        ),
    ]
