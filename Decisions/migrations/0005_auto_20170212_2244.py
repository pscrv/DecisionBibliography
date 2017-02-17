# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-12 21:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Decisions', '0004_auto_20170208_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='NullSupplementaryModel',
            fields=[
                ('decisionsupplementarymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Decisions.DecisionSupplementaryModel')),
            ],
            bases=('Decisions.decisionsupplementarymodel',),
        ),
        migrations.RemoveField(
            model_name='decisionsupplementarymodel',
            name='CitedCasesInDBNotFoundInTexts',
        ),
        migrations.RemoveField(
            model_name='decisionsupplementarymodel',
            name='CitedCasesNotFoundInDB',
        ),
        migrations.RemoveField(
            model_name='decisionsupplementarymodel',
            name='ExtraCasesExtractedFromTexts',
        ),
        migrations.AddField(
            model_name='decisionsupplementarymodel',
            name='CasesExtractedFromTexts_InDB',
            field=models.CharField(default='', max_length=700),
        ),
        migrations.AddField(
            model_name='decisionsupplementarymodel',
            name='CasesExtractedFromTexts_NotInDB',
            field=models.CharField(default='', max_length=700),
        ),
        migrations.AddField(
            model_name='decisionsupplementarymodel',
            name='CitedCases_InDB_NotInTexts',
            field=models.CharField(default='', max_length=700),
        ),
        migrations.AddField(
            model_name='decisionsupplementarymodel',
            name='CitedCases_NotInDB',
            field=models.CharField(default='', max_length=700),
        ),
    ]