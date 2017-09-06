# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 02:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_delete_newassetapprovalzone'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contract',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='asset',
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='disk',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='networkdevice',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='networkdevice',
            name='firmware',
        ),
        migrations.RemoveField(
            model_name='nic',
            name='asset',
        ),
        migrations.AlterUniqueTogether(
            name='raidadaptor',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='raidadaptor',
            name='asset',
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='ram',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='linkman',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='manufactory',
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('server', '\u670d\u52a1\u5668'), ('switch', '\u4ea4\u6362\u673a'), ('router', '\u8def\u7531\u5668'), ('firewall', '\u9632\u706b\u5899'), ('others', '\u5176\u4ed6\u7c7b')], default='server', max_length=64),
        ),
        migrations.DeleteModel(
            name='CPU',
        ),
        migrations.DeleteModel(
            name='Disk',
        ),
        migrations.DeleteModel(
            name='Linkman',
        ),
        migrations.DeleteModel(
            name='Manufactory',
        ),
        migrations.DeleteModel(
            name='NetworkDevice',
        ),
        migrations.DeleteModel(
            name='NIC',
        ),
        migrations.DeleteModel(
            name='RaidAdaptor',
        ),
        migrations.DeleteModel(
            name='RAM',
        ),
        migrations.DeleteModel(
            name='Software',
        ),
    ]