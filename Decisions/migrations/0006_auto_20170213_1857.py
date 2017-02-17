# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-13 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Decisions', '0005_auto_20170212_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decisionsupplementarymodel',
            name='Bibliography',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bibliography', to='Decisions.DecisionBibliographyModel'),
        ),
        migrations.AlterField(
            model_name='decisionsupplementarymodel',
            name='CitingCases',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CitingCases', to='Decisions.DecisionBibliographyModel'),
        ),
    ]
