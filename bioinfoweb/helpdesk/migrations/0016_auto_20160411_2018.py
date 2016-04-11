# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0015_auto_20160411_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='project_code',
            field=models.CharField(default='Other', help_text='Please select your project code, if "Other", please specify', max_length=400, choices=[('JOHN', 'JACOBS')]),
        ),
    ]
