from django.contrib import admin
from events.models import Evento, Participante

# Registro do modelo evento no admin
admin.site.register(Evento)
admin.site.register(Participante)