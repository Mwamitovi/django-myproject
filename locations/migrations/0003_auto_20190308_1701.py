# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-08 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_more_fields_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='street_address',
            field=models.CharField(blank=True, max_length=255, verbose_name='street address'),
        ),
    ]