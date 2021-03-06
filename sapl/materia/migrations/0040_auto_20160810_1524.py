# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-10 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materia', '0039_auto_20160808_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposicao',
            name='documento',
        ),
        migrations.AddField(
            model_name='proposicao',
            name='documento_gerado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='materia.DocumentoAcessorio'),
        ),
        migrations.AddField(
            model_name='proposicao',
            name='materia_gerada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materia_gerada', to='materia.MateriaLegislativa'),
        ),
        migrations.AlterField(
            model_name='proposicao',
            name='materia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materia_vinculada', to='materia.MateriaLegislativa', verbose_name='Matéria'),
        ),
    ]
