from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

import sapl
from materia.models import TipoMateriaLegislativa
from sapl.layout import form_actions

from .models import NormaJuridica


def get_esferas():
    return [('E', 'Estadual'),
            ('F', 'Federal'),
            ('M', 'Municipal')]


class HorizontalRadioRenderer(forms.RadioSelect.renderer):

    def render(self):
        return mark_safe(u' '.join([u'%s ' % w for w in self]))


class NormaJuridicaPesquisaForm(ModelForm):

    periodo_inicial = forms.DateField(label=u'Período Inicial',
                                      input_formats=['%d/%m/%Y'],
                                      required=False,
                                      widget=forms.DateInput(
                                        format='%d/%m/%Y',
                                        attrs={'class': 'dateinput'}))

    periodo_final = forms.DateField(label=u'Período Final',
                                      input_formats=['%d/%m/%Y'],
                                      required=False,
                                      widget=forms.DateInput(
                                        format='%d/%m/%Y',
                                        attrs={'class': 'dateinput'}))

    publicação_inicial = forms.DateField(label=u'Publicação Inicial',
                                         input_formats=['%d/%m/%Y'],
                                         required=False,
                                         widget=forms.DateInput(
                                            format='%d/%m/%Y',
                                            attrs={'class': 'dateinput'}))

    publicação_final = forms.DateField(label=u'Publicação Final',
                                       input_formats=['%d/%m/%Y'],
                                       required=False,
                                       widget=forms.DateInput(
                                            format='%d/%m/%Y',
                                            attrs={'class': 'dateinput'}))

    class Meta:
        model = NormaJuridica
        fields = ['tipo',
                  'numero',
                  'ano',
                  'periodo_inicial',
                  'periodo_final',
                  'publicação_inicial',
                  'publicação_final',]

    def __init__(self, *args, **kwargs):

        row1 = sapl.layout.to_row(
            [('tipo', 12)])

        row2 = sapl.layout.to_row(
            [('numero', 6), ('ano', 6)])

        row3 = sapl.layout.to_row(
            [('periodo_inicial', 6), ('periodo_final', 6)])

        row4 = sapl.layout.to_row(
            [('publicação_inicial', 6), ('publicação_final', 6)])

        self.helper = FormHelper()
        self.helper.layout = Layout(
             Fieldset('Pesquisa Norma Juridica',
                      row1, row2, row3, row4),
             form_actions(save_label='Pesquisar')
        )
        super(NormaJuridicaPesquisaForm, self).__init__(*args, **kwargs)


class NormaJuridicaForm(ModelForm):

    tipo_materia = forms.ModelChoiceField(
        label='Matéria Legislativa',
        required=False,
        queryset=TipoMateriaLegislativa.objects.all(),
        empty_label='Selecione'
    )

    numero_materia = forms.CharField(label='Número', required=False)

    ano_materia = forms.CharField(label='Ano', required=False)

    class Meta:
        model = NormaJuridica
        fields = ['tipo',
                  'numero',
                  'ano',
                  'data',
                  'esfera_federacao',
                  'complemento',
                  'tipo_materia',
                  'numero_materia',
                  'ano_materia',
                  'data_publicacao',
                  'veiculo_publicacao',
                  'pagina_inicio_publicacao',
                  'pagina_fim_publicacao',
                  'ementa',
                  'indexacao',
                  'observacao',
                  'texto_integral',
                  ]

    def __init__(self, *args, **kwargs):

        row1 = sapl.layout.to_row(
            [('tipo', 4), ('numero', 4), ('ano', 4)])

        row2 = sapl.layout.to_row(
            [('data', 4), ('esfera_federacao', 4), ('complemento', 4)])

        row3 = sapl.layout.to_row(
            [('tipo_materia', 4), ('numero_materia', 4), ('ano_materia', 4)])

        row4 = sapl.layout.to_row(
            [('data_publicacao', 3), ('veiculo_publicacao', 3),
             ('pagina_inicio_publicacao', 3), ('pagina_fim_publicacao', 3)])

        row5 = sapl.layout.to_row(
            [('texto_integral', 12)])

        row6 = sapl.layout.to_row(
            [('ementa', 12)])

        row7 = sapl.layout.to_row(
            [('indexacao', 12)])

        row8 = sapl.layout.to_row(
            [('observacao', 12)])

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset('Identificação Básica',
                     row1, row2, row3, row4, row5, row6, row7, row8),
            form_actions()
        )
        super(NormaJuridicaForm, self).__init__(*args, **kwargs)
