# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_decisiontextmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='decisiontextmodel',
            name='HasSplitText',
            field=models.BooleanField(default=False),
        ),
    ]
