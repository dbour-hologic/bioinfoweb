# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0012_auto_20170724_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunRecovery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=1000)),
                ('file', models.FileField(upload_to=b'recovery')),
                ('slug', models.SlugField(max_length=1000, blank=True)),
                ('upload_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'recovery',
                'verbose_name_plural': 'recovery',
            },
        ),
    ]
