# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-17 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessao', '0017_bancada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancada',
            name='data_criacao',
            field=models.DateField(blank=True, null=True, verbose_name='Data Criação'),
        ),
        migrations.AlterField(
            model_name='bancada',
            name='data_extincao',
            field=models.DateField(blank=True, null=True, verbose_name='Data Extinção'),
        ),
        migrations.AlterField(
            model_name='bancada',
            name='partido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parlamentares.Partido', verbose_name='Partido'),
        ),
    ]
