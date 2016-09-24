# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_decisiontextmodel_hassplittext'),
    ]

    operations = [
        migrations.AddField(
            model_name='decisiontextmodel',
            name='Language',
            field=models.CharField(choices=[('DE', 'DE'), ('EN', 'EN'), ('FR', 'FR')], default='', max_length=2),
        ),
    ]