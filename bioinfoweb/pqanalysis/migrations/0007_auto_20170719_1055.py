# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0006_auto_20170719_1054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='limits',
            options={'verbose_name': 'limit', 'verbose_name_plural': 'limits'},
        ),
    ]
