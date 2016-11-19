# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by Django 1.9.6 on 2016-11-11 16:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agent', '0001_initial'),
        ('developer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='developer.Developer'),
        ),
    ]
