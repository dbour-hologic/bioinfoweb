# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20160413_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msaeaccess',
            name='employee_tos_agree',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='msaeaccess',
            name='supervisor_signed',
            field=models.BooleanField(default=False),
        ),
    ]
