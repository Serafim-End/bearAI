# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by Django 1.9.6 on 2016-11-11 16:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('intent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_obligatory', models.BooleanField()),
                ('name', models.CharField(max_length=150)),
                ('intent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intent.Intent')),
            ],
        ),
        migrations.CreateModel(
            name='ParameterData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slots.Parameter')),
            ],
        ),
    ]