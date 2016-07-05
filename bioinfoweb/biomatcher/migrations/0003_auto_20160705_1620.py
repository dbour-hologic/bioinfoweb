# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biomatcher', '0002_auto_20160701_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biomatcherfileupload',
            name='biomatcher_filename',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
