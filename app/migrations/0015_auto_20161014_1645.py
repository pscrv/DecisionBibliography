# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-14 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20161014_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardanalysismodel',
            name='EarliestFive',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AlterField(
            model_name='boardanalysismodel',
            name='Article_TopFive',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='boardanalysismodel',
            name='Cited_TopFive',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='boardanalysismodel',
            name='IPC_TopFive',
            field=models.CharField(default='', max_length=120),
        ),
    ]
