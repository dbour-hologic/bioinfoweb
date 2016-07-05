# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import biomatcher.validators


class Migration(migrations.Migration):

    dependencies = [
        ('biomatcher', '0003_auto_20160705_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biomatcherfileupload',
            name='biomatcher_fileupload',
            field=models.FileField(upload_to=b'biomatcher/database', validators=[biomatcher.validators.validate_file_extension]),
        ),
    ]
