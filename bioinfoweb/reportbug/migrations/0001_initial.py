# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportBug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bug_reporter_name', models.CharField(max_length=100)),
                ('bug_title', models.CharField(max_length=100)),
                ('bug_description', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Bug Report',
            },
        ),
    ]
