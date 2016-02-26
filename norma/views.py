import ipdb
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView
from vanilla.views import GenericView

from compilacao.views import IntegracaoTaView
from crud import build_crud, make_pagination
from materia.models import MateriaLegislativa

from .forms import NormaJuridicaForm, NormaJuridicaPesquisaForm
from .models import (AssuntoNorma, LegislacaoCitada, NormaJuridica,
                     TipoNormaJuridica)

assunto_norma_crud = build_crud(
    AssuntoNorma, 'assunto_norma_juridica', [

        [_('Assunto Norma Jurídica'),
         [('assunto', 6), ('descricao', 6)]],
    ])

tipo_norma_crud = build_crud(
    TipoNormaJuridica, 'tipo_norma_juridica', [

        [_('Tipo Norma Jurídica'),
         [('descricao', 4),
            ('sigla', 4),
            ('equivalente_lexml', 4)]],
    ])


norma_temporario_crud = build_crud(
    NormaJuridica, 'normajuridica', [

        [_('Identificação Básica'),
         [('tipo', 4), ('numero', 4), ('ano', 4)],
            [('data', 4), ('esfera_federacao', 4), ('complemento', 4)],
            [('materia', 12)],
            [('data_publicacao', 3),
             ('veiculo_publicacao', 3),
             ('pagina_inicio_publicacao', 3),
             ('pagina_fim_publicacao', 3)],
            [('texto_integral', 12)],
            [('ementa', 12)],
            [('indexacao', 12)],
            [('observacao', 12)]],
    ])


legislacao_citada_crud = build_crud(
    LegislacaoCitada, '', [

        [_('Legislação Citada'),
         [('tip_norma_FIXME', 4),
            ('num_norma_FIXME', 4),
            ('ano_norma_FIXME', 4)],
            [('disposicoes', 3), ('parte', 3), ('livro', 3), ('titulo', 3)],
            [('capitulo', 3), ('secao', 3), ('subsecao', 3), ('artigo', 3)],
            [('paragrafo', 3), ('inciso', 3), ('alinea', 3), ('item', 3)]],
    ])


class NormaPesquisaView(GenericView):
    template_name = "norma/pesquisa.html"

    def get_success_url(self):
        return reverse('normajuridica:norma_pesquisa')

    def get(self, request, *args, **kwargs):
        form = NormaJuridicaPesquisaForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = NormaJuridicaPesquisaForm(request.POST)

        if form.data['tipo']:
            kwargs['tipo'] = form.data['tipo']
        if form.data['numero']:
            kwargs['numero'] = form.data['numero']
        if form.data['ano']:
            kwargs['ano'] = form.data['ano']
        if form.data['periodo_inicial'] and form.data['periodo_final']:
            kwargs['periodo_inicial'] = form.data['periodo_inicial']
            kwargs['periodo_final'] = form.data['periodo_final']
        if form.data['publicação_inicial'] and form.data['publicação_final']:
            kwargs['publicação_inicial'] = form.data['publicação_inicial']
            kwargs['publicação_final'] = form.data['publicação_final']

        request.session['kwargs'] = kwargs
        return redirect('list_pesquisa_norma')


class PesquisaNormaListView(ListView):
    template_name = 'norma/list_pesquisa.html'
    model = NormaJuridica
    paginate_by = 10

    def get_queryset(self):
        kwargs = self.request.session['kwargs']

        if 'periodo_inicial' and 'publicacao_inicial' in kwargs:
            ##### FALTA OS OUTROS CAMPOS QUE ESTIVEREM NO KWARGS
            periodo_inicial = datetime.strptime(
                kwargs['periodo_inicial'],
                '%d/%m/%Y').strftime('%Y-%m-%d')
            periodo_final = datetime.strptime(
                kwargs['periodo_final'],
                '%d/%m/%Y').strftime('%Y-%m-%d')
            publicação_inicial = datetime.strptime(
                kwargs['publicação_inicial'],
                '%d/%m/%Y').strftime('%Y-%m-%d')
            publicação_final = datetime.strptime(
                kwargs['publicação_final'],
                '%d/%m/%Y').strftime('%Y-%m-%d')

            normas = NormaJuridica.objects.filter(
                data__range=(periodo_inicial, periodo_final),
                data_publicacao__range=(publicação_inicial, publicação_final))
        elif 'periodo_inicial' in kwargs:
            ##### FALTA OS OUTROS CAMPOS QUE ESTIVEREM NO KWARGS
            inicial = datetime.strptime(kwargs['periodo_inicial'],
                                        '%d/%m/%Y').strftime('%Y-%m-%d')
            final = datetime.strptime(kwargs['periodo_inicial'],
                                        '%d/%m/%Y').strftime('%Y-%m-%d')

            normas = NormaJuridica.objects.filter(data__range=(inicial, final))
        elif 'publicação_inicial' in kwargs:
            ##### FALTA OS OUTROS CAMPOS QUE ESTIVEREM NO KWARGS
            inicial = datetime.strptime(kwargs['publicação_inicial'],
                                        '%d/%m/%Y').strftime('%Y-%m-%d')
            final = datetime.strptime(kwargs['publicação_final'],
                                        '%d/%m/%Y').strftime('%Y-%m-%d')

            normas = NormaJuridica.objects.filter(data_publicacao__range=(
                                                    inicial, final))
        else:
            ##### FALTA OS CAMPOS DE DATA
            normas = NormaJuridica.objects.filter(
                **kwargs).order_by('-ano', '-numero')
        return normas

    def get_context_data(self, **kwargs):
        context = super(PesquisaNormaListView, self).get_context_data(
            **kwargs)

        paginator = context['paginator']
        page_obj = context['page_obj']

        context['page_range'] = make_pagination(
            page_obj.number, paginator.num_pages)
        return context


class NormaIncluirView(CreateView):
    template_name = "norma/normajuridica_incluir.html"
    form_class = NormaJuridicaForm

    def get_success_url(self):
        return reverse('normajuridica:list')

    def get(self, request, *args, **kwargs):
        form = NormaJuridicaForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            norma = form.save(commit=False)

            if form.cleaned_data['tipo_materia']:
                try:
                    materia = MateriaLegislativa.objects.get(
                        tipo_id=form.cleaned_data['tipo_materia'],
                        numero=form.cleaned_data['numero_materia'],
                        ano=form.cleaned_data['ano_materia'])
                except ObjectDoesNotExist:
                    msg = 'Matéria adicionada não existe!'
                    messages.add_message(request, messages.INFO, msg)
                    return self.render_to_response({'form': form})
                else:
                    norma.materia = materia
            norma.timestamp = datetime.now()
            norma.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({'form': form})


class NormaEditView(CreateView):
    template_name = "norma/normajuridica_incluir.html"
    form_class = NormaJuridicaForm

    def get(self, request, *args, **kwargs):
        norma = NormaJuridica.objects.get(id=self.kwargs['pk'])
        form = NormaJuridicaForm(instance=norma)
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        norma = NormaJuridica.objects.get(id=self.kwargs['pk'])
        form = NormaJuridicaForm(instance=norma, data=request.POST)

        if form.is_valid():
            if form.data['tipo_materia']:
                try:
                    materia = MateriaLegislativa.objects.get(
                        tipo_id=form.data['tipo_materia'],
                        numero=form.data['numero_materia'],
                        ano=form.data['ano_materia'])
                except ObjectDoesNotExist:
                    msg = 'Matéria adicionada não existe!'
                    messages.add_message(request, messages.INFO, msg)
                    return self.render_to_response({'form': form})
                else:
                    norma.materia = materia
            norma = form.save(commit=False)
            norma.timestamp = datetime.now()
            norma.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({'form': form})

    def get_success_url(self):
        return reverse('normajuridica:list')


class NormaTaView(IntegracaoTaView):
    model = NormaJuridica
    model_type_foreignkey = TipoNormaJuridica
