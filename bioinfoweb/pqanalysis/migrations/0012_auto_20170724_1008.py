# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0011_auto_20170724_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='limits',
            name='limits_type',
            field=models.CharField(default='fusion', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worklist',
            name='worklist_type',
            field=models.CharField(default='fusion', max_length=1000),
            preserve_default=False,
        ),
    ]
