# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-20 19:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DecisionsPlus', '0002_auto_20170220_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citationsupplementmodel',
            old_name='CitedCases_NotInDB',
            new_name='CitedCases_notInDB',
        ),
    ]
