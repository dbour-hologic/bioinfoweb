# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0017_auto_20160411_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='project_code_alt',
            field=models.CharField(default='', max_length=400, null=True, help_text='Please indicate which project this is for', blank=True),
        ),
    ]
