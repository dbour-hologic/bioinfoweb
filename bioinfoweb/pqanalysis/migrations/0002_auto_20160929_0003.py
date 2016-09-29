# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklist',
            name='filename',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='slug',
            field=models.SlugField(max_length=1000, blank=True),
        ),
    ]
