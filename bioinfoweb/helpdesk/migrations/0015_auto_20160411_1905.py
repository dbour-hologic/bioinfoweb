# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0014_ticket_project_codes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='project_codes',
            new_name='project_code',
        ),
    ]
