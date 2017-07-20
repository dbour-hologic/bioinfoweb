# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0005_auto_20170719_1053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='limits',
            options={'verbose_name': 'limits', 'verbose_name_plural': 'limits'},
        ),
        migrations.AlterModelOptions(
            name='worklist',
            options={'verbose_name': 'worklist', 'verbose_name_plural': 'worklists'},
        ),
    ]
