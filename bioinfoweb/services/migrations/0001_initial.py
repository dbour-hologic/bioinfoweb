# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='msaeaccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_first_name', models.CharField(max_length=100)),
                ('user_last_name', models.CharField(max_length=100)),
                ('user_email', models.CharField(max_length=100)),
                ('user_network_name', models.CharField(unique=True, max_length=100)),
                ('user_title', models.CharField(max_length=100)),
                ('user_location', models.CharField(blank=True, max_length=100, null=True, choices=[(b'GCD1', b'GCD1'), (b'GCD2', b'GCD2'), (b'Other', b'Other')])),
                ('user_alt_location', models.CharField(max_length=100, null=True, blank=True)),
                ('request_type', models.CharField(max_length=100, choices=[(b'New Account', b'New Account'), (b'Remove Existing Account', b'Remove Existing Account')])),
                ('request_date', models.DateField(auto_now_add=True)),
                ('date_required', models.DateField()),
                ('user_status', models.CharField(max_length=100, choices=[(b'Full Time', b'Full Time'), (b'Temporary', b'Temporary'), (b'Consultant', b'Consultant')])),
                ('user_contract_date', models.DateField(null=True, blank=True)),
                ('phone_extension', models.CharField(max_length=100)),
                ('department_name', models.CharField(max_length=100)),
                ('supervisor_name', models.CharField(max_length=100)),
                ('supervisor_email', models.CharField(max_length=100)),
                ('employee_electronic_sig', models.CharField(default=b'', max_length=100)),
                ('employee_tos_agree', models.BooleanField(choices=[(True, b'Agree')])),
                ('employee_date_signed', models.DateField(auto_now_add=True)),
                ('supervisor_electronic_sig', models.CharField(default=b'', max_length=100)),
                ('supervisor_signed', models.BooleanField()),
                ('date_approved', models.DateField(null=True, blank=True)),
                ('approver_name', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'verbose_name': 'MSAE Request',
            },
        ),
    ]
