# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-12 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compilacao', '0070_perfilestruturaltextoarticulado_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipotextoarticulado',
            name='perfis',
            field=models.ManyToManyField(blank=True, help_text='\n                    Apenas os perfis selecionados aqui estarão disponíveis\n                    para o editor de Textos Articulados cujo Tipo seja este\n                    em edição.\n                    ', to='compilacao.PerfilEstruturalTextoArticulado', verbose_name='Perfis Estruturais de Textos Articulados'),
        ),
    ]