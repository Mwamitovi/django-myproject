# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-01-22 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('imported', 'Imported'), ('draft', 'Draft'), ('published', 'Published'), ('not_listed', 'Not Listed'), ('expired', 'Expired')], max_length=20, verbose_name='Status')),
            ],
        ),
    ]
