from datetime import timezone
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from events.models import Evento, Participante
from forms import ParticipanteForm


#Pagina principal
def index(request):
    return render(request, 'events/index.html')


#listar eventos

def list_events(request):
    eventos = Evento.objects.all()
    return render(request, 'events/list_events.html', {'eventos': eventos})

def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'events/evento_detalhado.html', {'evento': evento})


def adicionar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)  # Não salva ainda
            participante.data_inscricao = timezone.now()  # Define a data de inscrição
            participante.save()  # Agora salva o participante
            return redirect('list_participantes')
    else:
        form = ParticipanteForm()
    return render(request, 'events/form_participante.html', {'form': form, 'title': 'Inscrever-se no Evento'})



def list_participantes(request):
    participantes = Participante.objects.all()
    return render(request, 'events/participantes_list.html', {'participantes': participantes})
