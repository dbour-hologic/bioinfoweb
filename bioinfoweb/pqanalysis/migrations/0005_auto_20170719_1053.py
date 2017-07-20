# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0004_auto_20170719_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='limits',
            options={'verbose_name': 'Limits', 'verbose_name_plural': 'Limits'},
        ),
    ]
