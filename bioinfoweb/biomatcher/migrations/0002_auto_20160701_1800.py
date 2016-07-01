# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biomatcher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biomatcherfileupload',
            name='biomatcher_filename',
            field=models.CharField(unique=True, max_length=1000),
        ),
    ]
