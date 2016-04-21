# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gparchives', '0003_auto_20160420_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='author',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='documents',
            name='citation',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='documents',
            name='keywords',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='documents',
            name='title',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
