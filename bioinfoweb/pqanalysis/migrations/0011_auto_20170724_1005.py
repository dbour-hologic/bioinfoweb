# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0010_auto_20170720_1113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='limits',
            name='limits_type',
        ),
        migrations.RemoveField(
            model_name='worklist',
            name='worklist_type',
        ),
    ]
