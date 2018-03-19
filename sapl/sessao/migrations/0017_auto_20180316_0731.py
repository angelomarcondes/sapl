# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-16 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import sapl.sessao.models


class Migration(migrations.Migration):

    dependencies = [
        ('sessao', '0016_auto_20180131_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='orador',
            name='upload_anexo',
            field=models.FileField(blank=True, null=True, upload_to=sapl.sessao.models.anexo_upload_path, verbose_name='Anexo do Orador'),
        ),
        migrations.AddField(
            model_name='oradorexpediente',
            name='upload_anexo',
            field=models.FileField(blank=True, null=True, upload_to=sapl.sessao.models.anexo_upload_path, verbose_name='Anexo do Orador'),
        ),
    ]