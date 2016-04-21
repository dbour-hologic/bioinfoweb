# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gparchives', '0004_auto_20160420_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='document',
            field=models.FileField(max_length=2000, upload_to=b'archives'),
        ),
    ]
