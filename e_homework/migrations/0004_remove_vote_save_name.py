# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 03:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('e_homework', '0003_vote_save_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='save_name',
        ),
    ]
