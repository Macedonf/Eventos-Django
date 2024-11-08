
from datetime import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from events.models import Evento, Participante
from forms import ParticipanteForm


#Pagina principal
def index(request):
    return render(request, 'events/index.html')


#listar eventos
@login_required
def list_events(request):
    eventos = Evento.objects.filter(organizador=request.user)
    return render(request, 'events/list_events.html', {'eventos': eventos})

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
def excluir_participante(request, evento_id, participante_id):
    evento = get_object_or_404(Evento, id=evento_id)
    participante = get_object_or_404(Participante, id=participante_id, evento_associado=evento)

    if request.method == 'POST':
        participante.delete()
        return redirect('list_participantes', evento_id=evento.id)


    return render(request, 'events/excluir_participante.html', {'participante': participante, 'evento': evento})


@login_required
def list_participantes(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    participantes = Participante.objects.filter(evento_associado=evento)
    return render(request, 'events/participantes_list.html', {'participantes': participantes, 'evento' : evento})


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
