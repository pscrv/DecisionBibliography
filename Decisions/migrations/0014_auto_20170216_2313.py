# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-16 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Decisions', '0013_auto_20170215_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decisionsupplementarymodel',
            name='CitingCases_Bibliography',
        ),
        migrations.AddField(
            model_name='decisionsupplementarymodel',
            name='CitingCases_Bibliography',
            field=models.CharField(default='', max_length=700),
        ),
        migrations.RemoveField(
            model_name='decisionsupplementarymodel',
            name='CitingCases_Text',
        ),
        migrations.AddField(
            model_name='decisionsupplementarymodel',
            name='CitingCases_Text',
            field=models.CharField(default='', max_length=700),
        ),
    ]
