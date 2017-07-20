# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0003_limits'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worklist',
            options={'verbose_name': 'Worklist', 'verbose_name_plural': 'Worklists'},
        ),
    ]
