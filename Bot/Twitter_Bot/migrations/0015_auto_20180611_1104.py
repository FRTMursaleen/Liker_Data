# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-11 11:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Twitter_Bot', '0014_auto_20180611_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts_data',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]