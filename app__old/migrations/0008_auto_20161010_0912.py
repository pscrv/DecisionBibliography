# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 07:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_decisionbibliographymodel_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decisionbibliographymodel',
            name='LinkDE',
        ),
        migrations.RemoveField(
            model_name='decisionbibliographymodel',
            name='LinkEN',
        ),
        migrations.RemoveField(
            model_name='decisionbibliographymodel',
            name='LinkFR',
        ),
    ]