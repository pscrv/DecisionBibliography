# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-08 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Decisions', '0003_decisionsupplementarymodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='decisionsupplementarymodel',
            old_name='CitedCasesNotFoundInTexts',
            new_name='CitedCasesInDBNotFoundInTexts',
        ),
        migrations.AddField(
            model_name='decisionsupplementarymodel',
            name='CitedCasesNotFoundInDB',
            field=models.CharField(default='', max_length=700),
        ),
    ]
