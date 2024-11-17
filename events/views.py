import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.utils.html import strip_tags
from events.models import Evento, Participante
from forms import ParticipanteForm, PesquisaForm
from event_manager.utils import enviar_email
from django.template.loader import render_to_string



def index(request):
    evento_id = Evento.objects.first().id if Evento.objects.exists() else None
    return render(request, 'events/index.html', {'evento_id': evento_id})


@login_required
def list_events(request):
    eventos = Evento.objects.filter(organizador=request.user)
    return render(request, 'events/list_events.html', {'eventos': eventos})


@login_required
def relatorio_eventos(request, evento_id):
    try:
        evento = get_object_or_404(Evento, id=evento_id, organizador=request.user)
        participantes = Participante.objects.filter(evento_associado=evento)

        total_inscritos = participantes.count()
        total_pagantes = participantes.filter(ingresso='PAGO').count()
        total_nao_pagantes = participantes.filter(ingresso='NAO_PAGO').count()
        total_pago = participantes.filter(ingresso='PAGO').aggregate(total_pago=Sum('valor_ingresso'))['total_pago'] or 0

        relatorio = {
            'total_inscritos': total_inscritos,
            'total_pagantes': total_pagantes,
            'total_nao_pagantes': total_nao_pagantes,
            'total_pago': total_pago,
        }

        return render(request, 'events/relatorio_evento.html', {'evento': evento, 'relatorio': relatorio})
    except Evento.DoesNotExist:
        messages.error(request, 'Evento não encontrado ou você não tem permissão para acessar.')
        return redirect('list_events')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from events.models import Evento, Participante

from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Evento, Participante


@login_required
def relatorio_geral(request):
    eventos = Evento.objects.filter(organizador=request.user)

    # Inicializar os totais
    total_pagantes = 0
    total_nao_pagantes = 0
    total_pago = 0
    total_nao_pago = 0

    eventos_data = []

    for evento in eventos:
        pagantes_count = evento.participante_set.filter(ingresso='PAGO').count()
        nao_pagantes_count = evento.participante_set.filter(ingresso='NAO_PAGO').count()

        # Calcular total pago e total não pago
        total_pago_evento = evento.participante_set.filter(ingresso='PAGO').aggregate(Sum('valor_ingresso'))[
                                'valor_ingresso__sum'] or 0
        total_nao_pago_evento = evento.participante_set.filter(ingresso='NAO_PAGO').aggregate(Sum('valor_ingresso'))[
                                    'valor_ingresso__sum'] or 0

        total_pagantes += pagantes_count
        total_nao_pagantes += nao_pagantes_count
        total_pago += total_pago_evento
        total_nao_pago += total_nao_pago_evento

        eventos_data.append({
            'evento': evento,
            'pagantes_count': pagantes_count,
            'nao_pagantes_count': nao_pagantes_count,
            'total_pago_evento': total_pago_evento,
            'total_nao_pago_evento': total_nao_pago_evento,
        })

    contexto = {
        'eventos_data': eventos_data,
        'total_pagantes': total_pagantes,
        'total_nao_pagantes': total_nao_pagantes,
        'total_pago': total_pago,
        'total_nao_pago': total_nao_pago,
    }

    return render(request, 'events/relatorio_geral.html', contexto)


from django.http import HttpResponse
import csv
from .models import Evento

def exportar_relatorio_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_geral.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['Evento', 'Participante', 'nome_evento', 'data_inicio', 'nome', 'ingresso'])

    eventos = Evento.objects.all()


    for evento in eventos:

        participantes = evento.participante_set.all()


        for participante in participantes:
            writer.writerow([
                evento.nome_evento,
                participante.nome,
                evento.nome_evento,
                evento.data_inicio,
                participante.nome,
                participante.ingresso,
            ])

    return response




@login_required
def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'events/evento_detalhado.html', {'evento': evento})


@login_required
def adicionar_participante(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.evento_associado = evento
            participante.data_inscricao = timezone.now()
            participante.save()
            return redirect('list_participantes', evento_id=evento.id)
    else:
        form = ParticipanteForm()
    return render(request, 'events/form_participante.html', {'form': form, 'title': 'Inscrever-se no Evento'})

@login_required
def editar_participante(request, evento_id, participante_id):
    evento = get_object_or_404(Evento, id=evento_id)
    participante = get_object_or_404(Participante, id=participante_id, evento_associado=evento)

    if request.method == 'POST':
        form = ParticipanteForm(request.POST, instance=participante)
        if form.is_valid():
            form.save()
            return redirect('list_participantes', evento_id=evento.id)
    else:
        form = ParticipanteForm(instance=participante)

    return render(request, 'events/form_participante.html', {'form': form, 'title': 'Editar Participante'})


@login_required
def excluir_participante(request, evento_id, participante_id, mensagem_html=None):
    evento = get_object_or_404(Evento, id=evento_id)
    participante = get_object_or_404(Participante, id=participante_id, evento_associado=evento)

    if request.method == 'POST':
        participante.delete()

        email = participante.email
        assunto = ' Confirmação de Cancelamento de Inscrição no Evento'

        mensagem_html = render_to_string('events/email_cancelamento.html', {
            'participante': participante,  # Passando o participante correto
            'evento': evento,  # Passando o evento correto
            'email': email,})

        envia_email (email, assunto, mensagem_html)

        messages.success(request, "A inscrição foi cancelada e o e-mail de confirmação foi enviado.")

        return redirect('list_participantes', evento_id=evento.id)


    return render(request, 'events/excluir_participante.html', {'participante': participante, 'evento': evento})


@login_required
def list_participantes(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    participantes = Participante.objects.filter(evento_associado=evento)
    return render(request, 'events/participantes_list.html', {'participantes': participantes, 'evento' : evento})

@login_required
def ingresso_pago(request, participante_id):
    participante=get_object_or_404(Participante,id=participante_id)

    if participante.ingresso == 'NAO_PAGO':
        participante.ingresso = 'PAGO'
    else:
         participante.ingresso = 'NAO_PAGO'

    participante.save()

    return redirect('list_participantes', evento_id=participante.evento_associado.id)



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def envia_email(email, assunto, mensagem_html):
    plain_message = strip_tags(mensagem_html)
    enviar_email(
        destinatario=email,
        assunto=assunto,
        mensagem=plain_message,
        mensagem_html=mensagem_html
    )


from django.db.models import Q

def pesquisa_eventos(request):
    form = PesquisaForm(request.GET or None)
    inscricoes = Participante.objects.all()  # Buscar todas as inscrições inicialmente

    if form.is_valid():
        evento = form.cleaned_data.get("evento")
        data_inicio = form.cleaned_data.get("data_inicio")
        data_fim = form.cleaned_data.get("data_fim")

        # Filtro por evento
        if evento:
            inscricoes = inscricoes.filter(evento_associado__nome_evento__icontains=evento)

        # Filtro por data de inscrição
        if data_inicio:
            inscricoes = inscricoes.filter(data_inscricao__gte=data_inicio)
        if data_fim:
            inscricoes = inscricoes.filter(data_inscricao__lte=data_fim)

    context = {"form": form, "inscricoes": inscricoes}
    return render(request, "events/pesquisa.html", context)
