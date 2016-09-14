# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pqanalysis.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CombineResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('combine_file_name', models.CharField(max_length=100)),
                ('combine_file_dir', models.FileField(max_length=1000, upload_to=b'pqcombined')),
                ('date_uploaded', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PqAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analysis_id', models.CharField(max_length=100)),
                ('file_name', models.CharField(max_length=100)),
                ('attachment', models.FileField(max_length=1000, upload_to=pqanalysis.models.upload_to)),
                ('submitter', models.CharField(max_length=100)),
                ('date_submitted', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PqResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pq_file_name', models.CharField(max_length=100)),
                ('file_dir', models.FileField(max_length=1000, upload_to=None)),
                ('pqresults', models.ForeignKey(to='pqanalysis.PqAttachment')),
            ],
        ),
        migrations.CreateModel(
            name='Worklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to=b'worklist')),
                ('slug', models.SlugField(blank=True)),
                ('upload_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
