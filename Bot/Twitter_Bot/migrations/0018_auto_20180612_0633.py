# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-12 06:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Twitter_Bot', '0017_auto_20180611_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts_data',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
