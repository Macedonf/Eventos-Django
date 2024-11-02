from django.shortcuts import render, get_object_or_404

from events.models import Evento


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