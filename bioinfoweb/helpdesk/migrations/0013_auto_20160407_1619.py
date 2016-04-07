# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0012_queue_default_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='request_firstname',
            field=models.CharField(max_length=200, null=True, verbose_name='First Name', blank=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='request_lastname',
            field=models.CharField(max_length=200, null=True, verbose_name='Last Name', blank=True),
        ),
    ]
