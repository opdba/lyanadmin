# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 02:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20170906_0158'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewAssetApprovalZone',
        ),
    ]
