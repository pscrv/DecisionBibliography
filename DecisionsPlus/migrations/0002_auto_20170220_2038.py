# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-20 19:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DecisionsPlus', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citationsupplementmodel',
            old_name='TextCited_NotInDB',
            new_name='TextCited_notInDB',
        ),
    ]
