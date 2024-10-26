from django.shortcuts import render

from events.models import Evento


#Pagina principal
def index(request):
    return render(request, 'events/index.html')


#listar eventos

def list_events(request):
    eventos = Evento.objects.all()
    return render(request, 'events/list_events.html', {'eventos': eventos})
