from django.shortcuts import render

from events.models import Evento


#Pagina principal
def index(request):
    return render(request, 'events/index.html')



