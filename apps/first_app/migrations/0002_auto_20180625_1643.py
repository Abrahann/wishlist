# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-25 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='wish',
            name='item_id',
        ),
        migrations.AddField(
            model_name='wish',
            name='name',
            field=models.CharField(default=11, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=35),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
