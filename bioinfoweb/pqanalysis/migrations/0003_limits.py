# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0002_auto_20160929_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Limits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=1000)),
                ('file', models.FileField(upload_to=b'limits')),
                ('slug', models.SlugField(max_length=1000, blank=True)),
                ('upload_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
