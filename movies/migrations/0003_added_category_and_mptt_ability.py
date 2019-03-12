# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-12 08:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_year_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False, verbose_name='creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='modification date and time')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['tree_id', 'lft'],
            },
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'verbose_name': 'Movie', 'verbose_name_plural': 'Movies'},
        ),
        migrations.AddField(
            model_name='movie',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='creation date and time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='modified',
            field=models.DateTimeField(editable=False, null=True, verbose_name='modification date and time'),
        ),
        migrations.AddField(
            model_name='movie',
            name='categories',
            field=mptt.fields.TreeManyToManyField(to='movies.Category', verbose_name='Categories'),
        ),
    ]